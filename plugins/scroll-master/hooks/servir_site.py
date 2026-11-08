#!/usr/bin/env python3
"""
Controla o servidor local do site de um projeto Scroll Master (só biblioteca padrão).

Comandos:
  garantir  usado pelo hook PostToolUse: lê o evento do stdin e, se o arquivo alterado for do projeto,
            sobe o servidor caso ele não esteja rodando (a recarga do navegador é automática)
  iniciar   sobe o servidor manualmente e mostra o endereço
  status    mostra se o servidor está rodando
  parar     para o servidor
  sair      usado pelo hook SessionEnd: para o servidor se "parar_ao_sair" for true

Só age em projetos que têm a pasta .scroll-master/ na raiz.
Configuração em .scroll-master/config.json (site_dir, porta, host, servidor_auto, abrir_navegador, parar_ao_sair).
"""
import json
import os
import signal
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PADRAO = {"site_dir": ".scroll-master/05-site", "porta": 4321, "host": "127.0.0.1",
          "servidor_auto": True, "abrir_navegador": True, "parar_ao_sair": True}


def ler_evento():
    if sys.stdin is None or sys.stdin.isatty():
        return {}
    try:
        bruto = sys.stdin.read()
        return json.loads(bruto) if bruto.strip() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def achar_projeto(evento):
    candidatos = [os.environ.get("CLAUDE_PROJECT_DIR"), evento.get("cwd"), os.getcwd()]
    for c in filter(None, candidatos):
        p = Path(c).resolve()
        for pasta in [p, *p.parents]:
            if (pasta / ".scroll-master").is_dir():
                return pasta
    return None


def config(raiz):
    cfg = dict(PADRAO)
    arquivo = raiz / ".scroll-master" / "config.json"
    if arquivo.exists():
        try:
            cfg.update(json.loads(arquivo.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            pass
    return cfg


def porta_ocupada(host, porta):
    alvo = "127.0.0.1" if host in ("0.0.0.0", "") else host
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex((alvo, porta)) == 0


def processo_vivo(pid):
    if not pid:
        return False
    if os.name == "nt":
        saida = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True).stdout
        return str(pid) in saida
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def arquivo_estado(raiz):
    return raiz / ".scroll-master" / ".servidor.json"


def estado_atual(raiz):
    arq = arquivo_estado(raiz)
    if not arq.exists():
        return None
    try:
        e = json.loads(arq.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if processo_vivo(e.get("pid")) and porta_ocupada(e.get("host", "127.0.0.1"), e.get("porta", 0)):
        return e
    arq.unlink(missing_ok=True)
    return None


def tipo_site(site):
    pkg = site / "package.json"
    if pkg.exists():
        try:
            scripts = json.loads(pkg.read_text(encoding="utf-8")).get("scripts", {})
        except json.JSONDecodeError:
            scripts = {}
        if "dev" in scripts:
            return "npm"
    if (site / "index.html").exists():
        return "estatico"
    return None


def iniciar(raiz, cfg, abrir):
    site = (raiz / cfg["site_dir"]).resolve()
    tipo = tipo_site(site) if site.is_dir() else None
    if not tipo:
        return None, None  # ainda não há site para servir: fica em silêncio
    if tipo == "npm" and not (site / "node_modules").is_dir():
        return None, f"Projeto com package.json em {cfg['site_dir']} sem node_modules: rode `npm install` nessa pasta para o servidor local subir."

    host, porta = cfg["host"], int(cfg["porta"])
    while porta_ocupada(host, porta) and porta < int(cfg["porta"]) + 20:
        porta += 1

    if tipo == "npm":
        cmd = ["npm", "run", "dev", "--", "--port", str(porta), "--host", host]
        espera = 15
    else:
        cmd = [sys.executable, str(AQUI / "servidor_local.py"), str(site), host, str(porta)]
        espera = 4

    log = open(raiz / ".scroll-master" / ".servidor.log", "a", encoding="utf-8")
    opcoes = {"cwd": str(site), "stdout": log, "stderr": subprocess.STDOUT, "stdin": subprocess.DEVNULL}
    if os.name == "nt":
        opcoes["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | getattr(subprocess, "DETACHED_PROCESS", 0)
        if tipo == "npm":
            cmd = ["cmd", "/c", *cmd]
    else:
        opcoes["start_new_session"] = True
    proc = subprocess.Popen(cmd, **opcoes)

    limite = time.time() + espera
    while time.time() < limite and not porta_ocupada(host, porta):
        if proc.poll() is not None:
            return None, f"O servidor local não subiu (veja .scroll-master/.servidor.log)."
        time.sleep(0.25)

    url = f"http://{'localhost' if host in ('127.0.0.1', '0.0.0.0') else host}:{porta}/"
    arquivo_estado(raiz).write_text(json.dumps({"pid": proc.pid, "porta": porta, "host": host,
                                                "tipo": tipo, "url": url}), encoding="utf-8")
    if abrir and cfg.get("abrir_navegador") and os.environ.get("CLAUDE_CODE_REMOTE") != "true":
        try:
            webbrowser.open(url)
        except Exception:
            pass
    recarga = "recarrega sozinho a cada mudança, mantendo a posição do scroll" if tipo == "estatico" \
        else "a recarga é a do próprio framework"
    return url, f"Site local do Scroll Master rodando em {url} ({recarga}). Avise o usuário do endereço."


def parar(raiz):
    e = estado_atual(raiz)
    arquivo_estado(raiz).unlink(missing_ok=True)
    if not e:
        return False
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(e["pid"]), "/T", "/F"], capture_output=True)
        else:
            os.killpg(e["pid"], signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        pass
    return True


def arquivo_relevante(raiz, cfg, evento):
    caminho = (evento.get("tool_input") or {}).get("file_path") or (evento.get("tool_input") or {}).get("path")
    if not caminho:
        return True
    p = Path(caminho)
    p = (raiz / p).resolve() if not p.is_absolute() else p.resolve()
    pastas = [(raiz / ".scroll-master").resolve(), (raiz / cfg["site_dir"]).resolve()]
    return any(p == pasta or pasta in p.parents for pasta in pastas)


def contexto(msg):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}},
                     ensure_ascii=False))


def main():
    comando = sys.argv[1] if len(sys.argv) > 1 else "garantir"
    evento = ler_evento() if comando in ("garantir", "sair") else {}
    raiz = achar_projeto(evento)
    if not raiz:
        if comando in ("garantir", "sair"):
            return  # não é um projeto Scroll Master: o hook não faz nada
        sys.exit("Nenhuma pasta .scroll-master encontrada a partir daqui.")
    cfg = config(raiz)

    if comando == "garantir":
        if not cfg.get("servidor_auto") or not arquivo_relevante(raiz, cfg, evento) or estado_atual(raiz):
            return
        url, msg = iniciar(raiz, cfg, abrir=True)
        if not msg:
            return
        avisado = raiz / ".scroll-master" / ".servidor-aviso"
        if url or not avisado.exists() or avisado.read_text(encoding="utf-8") != msg:
            contexto(msg)  # avisos repetidos (ex.: falta npm install) só aparecem uma vez
            if not url:
                avisado.write_text(msg, encoding="utf-8")
    elif comando == "iniciar":
        e = estado_atual(raiz)
        if e:
            print(f"Já está rodando em {e['url']}")
            return
        url, msg = iniciar(raiz, cfg, abrir=True)
        print(msg or f"Ainda não há site em {cfg['site_dir']} (falta index.html ou package.json).")
        sys.exit(0 if url else 1)
    elif comando == "status":
        e = estado_atual(raiz)
        print(f"Rodando em {e['url']} (pid {e['pid']}, {e['tipo']})" if e else "Parado.")
    elif comando == "parar":
        print("Servidor parado." if parar(raiz) else "Não havia servidor rodando.")
    elif comando == "sair":
        if cfg.get("parar_ao_sair"):
            parar(raiz)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as erro:  # um hook nunca deve atrapalhar o trabalho
        print(f"Scroll Master (servidor local): {erro}", file=sys.stderr)
        sys.exit(0)
