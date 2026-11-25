#!/usr/bin/env python3
"""
Lê e grava o scroll-master.json: as preferências do usuário que valem para todos os projetos
(modo de geração de imagem e vídeo, onde fica a chave da API, pasta dos padrões colhidos, stack).

O arquivo fica em ~/.scroll-master/scroll-master.json (ou no caminho da variável SCROLL_MASTER_CONFIG).
A chave da API NUNCA é gravada no arquivo: guardamos só o NOME da variável de ambiente onde o
usuário colocou a chave (export no macOS/Linux, setx no Windows). Assim o arquivo pode ser lido,
copiado e mostrado sem vazar segredo.

Uso:
  python3 config_usuario.py caminho                       # mostra onde o arquivo fica
  python3 config_usuario.py iniciar                       # cria com os valores padrão, se não existir
  python3 config_usuario.py mostrar                       # imprime o JSON + se as chaves estão definidas
  python3 config_usuario.py obter geracao.video.modo      # imprime um valor (vazio se não existir)
  python3 config_usuario.py definir geracao.video.modo api
  python3 config_usuario.py definir geracao.video.variavel_chave HIGGSFIELD_API_KEY
  python3 config_usuario.py definir padroes.pasta "~/scroll-master-padroes"
  python3 config_usuario.py chave HIGGSFIELD_API_KEY      # diz se a variável existe (sem mostrar o valor)
  python3 config_usuario.py pendentes                     # lista o que ainda não foi respondido pelo usuário

Valores de "definir" são lidos como JSON quando possível (true, 10, null, ["a"]); senão, como texto.
Sai com código 1 e mensagem clara em caso de erro.
"""
import json
import os
import sys
from datetime import date
from pathlib import Path

# Consoles do Windows usam cp1252 e quebram ao imprimir acentos e símbolos como ✔.
for _fluxo in (sys.stdout, sys.stderr):
    try:
        _fluxo.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

PADRAO = {
    "versao": 1,
    "geracao": {
        "imagem": {"modo": None, "provedor": None, "variavel_chave": None, "modelo": None},
        "video": {"modo": None, "provedor": None, "variavel_chave": None, "modelo": None},
        "teto_creditos_por_projeto": None,
        "confirmar_antes_de_gerar": True,
    },
    "padroes": {"pasta": "~/.scroll-master/padroes", "colhidos": []},
    "preferencias": {"stack": None, "abrir_navegador": True},
    "atualizado_em": None,
}

MODOS = {"manual", "api", "mcp"}

# Campos que o agente precisa perguntar ao usuário na primeira vez em que forem necessários.
PERGUNTAS = {
    "geracao.imagem.modo": "Imagens: você gera à mão (manual), por API com chave em variável de ambiente (api) ou por um conector MCP já ligado ao Claude (mcp)?",
    "geracao.video.modo": "Vídeos: manual, api ou mcp?",
    "preferencias.stack": "Stack padrão dos sites: html (arquivo único) ou astro (Astro + Tailwind)?",
}


def caminho_config():
    return Path(os.environ.get("SCROLL_MASTER_CONFIG", "~/.scroll-master/scroll-master.json")).expanduser()


def mesclar(base, novo):
    """Completa 'novo' com as chaves de 'base' que faltarem (para arquivos de versões antigas)."""
    for k, v in base.items():
        if k not in novo:
            novo[k] = json.loads(json.dumps(v))
        elif isinstance(v, dict) and isinstance(novo[k], dict):
            mesclar(v, novo[k])
    return novo


def ler():
    p = caminho_config()
    if not p.exists():
        return json.loads(json.dumps(PADRAO))
    try:
        return mesclar(PADRAO, json.loads(p.read_text(encoding="utf-8")))
    except json.JSONDecodeError as e:
        sair(f"{p} não é um JSON válido (linha {e.lineno}). Corrija ou apague o arquivo para recriar.")


def gravar(dados):
    p = caminho_config()
    p.parent.mkdir(parents=True, exist_ok=True)
    dados["atualizado_em"] = date.today().isoformat()
    p.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def obter(dados, chave):
    atual = dados
    for parte in chave.split("."):
        if not isinstance(atual, dict) or parte not in atual:
            return None
        atual = atual[parte]
    return atual


def definir(dados, chave, valor):
    partes = chave.split(".")
    atual = dados
    for parte in partes[:-1]:
        if not isinstance(atual.get(parte), dict):
            atual[parte] = {}
        atual = atual[parte]
    atual[partes[-1]] = valor


def interpretar(texto):
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        return texto


def parece_chave(valor):
    """Heurística para recusar uma chave de API colada no lugar do nome da variável."""
    return isinstance(valor, str) and len(valor) > 24 and not valor.replace("_", "").isupper()


def status_chaves(dados):
    linhas = []
    for tipo in ("imagem", "video"):
        var = obter(dados, f"geracao.{tipo}.variavel_chave")
        if var:
            ok = bool(os.environ.get(var))
            linhas.append(f"{tipo}: variável {var} {'definida' if ok else 'NÃO definida nesta sessão'}")
    return linhas


def instrucao_chave(var):
    return (
        f"Defina a chave fora do Claude, no seu terminal:\n"
        f"  macOS/Linux:  export {var}=\"sua-chave\"   (para ficar permanente, coloque a linha no ~/.zshrc ou ~/.bashrc)\n"
        f"  Windows:      setx {var} \"sua-chave\"\n"
        f"Depois feche e abra o Claude Code: variáveis novas só aparecem em sessões novas."
    )


def sair(msg):
    print(f"Erro: {msg}", file=sys.stderr)
    sys.exit(1)


def main(args):
    if not args:
        print(__doc__.strip())
        sys.exit(1)
    cmd, resto = args[0], args[1:]
    if cmd == "caminho":
        print(caminho_config())
    elif cmd == "iniciar":
        p = caminho_config()
        if p.exists():
            print(f"Já existe: {p}")
        else:
            gravar(ler())
            print(f"✔ Criado {p}")
    elif cmd == "mostrar":
        dados = ler()
        print(json.dumps(dados, ensure_ascii=False, indent=2))
        for linha in status_chaves(dados):
            print(f"# {linha}")
        if not caminho_config().exists():
            print("# (arquivo ainda não existe; estes são os valores padrão)")
    elif cmd == "obter":
        if len(resto) != 1:
            sair("uso: obter <chave.pontuada>")
        valor = obter(ler(), resto[0])
        if valor is not None:
            print(valor if isinstance(valor, str) else json.dumps(valor, ensure_ascii=False))
    elif cmd == "definir":
        if len(resto) != 2:
            sair("uso: definir <chave.pontuada> <valor>")
        chave, valor = resto[0], interpretar(resto[1])
        if chave.endswith(".modo") and valor not in MODOS:
            sair(f"modo inválido '{valor}'. Use: {', '.join(sorted(MODOS))}.")
        if chave.endswith("variavel_chave") and parece_chave(valor):
            sair("isso parece a chave em si. Grave só o NOME da variável (ex.: HIGGSFIELD_API_KEY).\n" + instrucao_chave("NOME_DA_VARIAVEL"))
        dados = ler()
        definir(dados, chave, valor)
        gravar(dados)
        print(f"✔ {chave} = {json.dumps(valor, ensure_ascii=False)}  ({caminho_config()})")
        if chave.endswith("variavel_chave") and isinstance(valor, str) and not os.environ.get(valor):
            print(instrucao_chave(valor))
    elif cmd == "chave":
        if len(resto) != 1:
            sair("uso: chave <NOME_DA_VARIAVEL>")
        if os.environ.get(resto[0]):
            print(f"✔ {resto[0]} definida")
        else:
            print(f"✘ {resto[0]} não definida nesta sessão.\n{instrucao_chave(resto[0])}")
            sys.exit(1)
    elif cmd == "pendentes":
        dados = ler()
        faltando = [(k, p) for k, p in PERGUNTAS.items() if obter(dados, k) in (None, "")]
        for tipo, rotulo in (("imagem", "imagens"), ("video", "vídeos")):
            if obter(dados, f"geracao.{tipo}.modo") == "api" and not obter(dados, f"geracao.{tipo}.variavel_chave"):
                faltando.append((f"geracao.{tipo}.variavel_chave", f"Qual o nome da variável de ambiente com a chave da API de {rotulo}? (ex.: HIGGSFIELD_API_KEY)"))
            if obter(dados, f"geracao.{tipo}.modo") in ("api", "mcp") and not obter(dados, f"geracao.{tipo}.provedor"):
                faltando.append((f"geracao.{tipo}.provedor", f"Qual serviço gera os {rotulo}? (ex.: higgsfield, flow)"))
        for k, p in faltando:
            print(f"{k}\t{p}")
    else:
        sair(f"comando desconhecido '{cmd}'. Rode sem argumentos para ver o uso.")


if __name__ == "__main__":
    main(sys.argv[1:])
