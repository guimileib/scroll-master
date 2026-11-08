#!/usr/bin/env python3
"""
Servidor local do Scroll Master (só biblioteca padrão).

- Serve a pasta do site sem cache.
- Injeta nas páginas HTML um script que recarrega a página quando qualquer arquivo do site muda,
  voltando para a mesma posição do scroll.
- Responde a requisições parciais (Range), necessárias para vídeo no Safari e para controlar
  vídeo pelo scroll.

Uso: python3 servidor_local.py <pasta-do-site> <host> <porta>
"""
import mimetypes
import os
import re
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROTA_VERSAO = "/__scroll-master/versao"
IGNORAR = {"node_modules", ".git", ".astro", ".cache"}
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("video/webm", ".webm")
mimetypes.add_type("video/mp4", ".mp4")

SCRIPT_RECARGA = """
<script>
/* Scroll Master: recarga automática (só no servidor local) */
(() => {
  const CHAVE = "__scroll_master_y";
  const y = sessionStorage.getItem(CHAVE);
  if (y !== null) {
    sessionStorage.removeItem(CHAVE);
    history.scrollRestoration = "manual";
    addEventListener("load", () => setTimeout(() => scrollTo(0, Number(y)), 350));
  }
  let versao = null;
  setInterval(async () => {
    try {
      const r = await fetch("%s", { cache: "no-store" });
      const v = await r.text();
      if (versao !== null && v !== versao) {
        sessionStorage.setItem(CHAVE, String(scrollY));
        location.reload();
      }
      versao = v;
    } catch (e) { /* servidor parado: tenta de novo no próximo ciclo */ }
  }, 1000);
})();
</script>
""" % ROTA_VERSAO


def versao(raiz):
    maior = 0.0
    for pasta, subpastas, arquivos in os.walk(raiz):
        subpastas[:] = [s for s in subpastas if s not in IGNORAR and not s.startswith(".")]
        for a in arquivos:
            try:
                maior = max(maior, os.path.getmtime(os.path.join(pasta, a)))
            except OSError:
                pass
    return f"{maior:.3f}"


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, formato, *args):
        sys.stderr.write("%s %s\n" % (self.log_date_time_string(), formato % args))

    def do_GET(self):
        rota = self.path.split("?", 1)[0].split("#", 1)[0]
        if rota == ROTA_VERSAO:
            corpo = versao(self.directory).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)
            return

        caminho = self.translate_path(self.path)
        if os.path.isdir(caminho):
            if not rota.endswith("/"):
                return super().do_GET()  # redireciona para a barra final
            caminho = os.path.join(caminho, "index.html")
        if not os.path.isfile(caminho):
            return super().do_GET()

        if caminho.endswith((".html", ".htm")):
            return self.servir_html(caminho)
        if self.headers.get("Range"):
            return self.servir_parcial(caminho)
        return super().do_GET()

    def servir_html(self, caminho):
        with open(caminho, "rb") as f:
            html = f.read().decode("utf-8", errors="replace")
        i = html.lower().rfind("</body>")
        html = html[:i] + SCRIPT_RECARGA + html[i:] if i != -1 else html + SCRIPT_RECARGA
        corpo = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def servir_parcial(self, caminho):
        tamanho = os.path.getsize(caminho)
        m = re.match(r"bytes=(\d*)-(\d*)$", self.headers.get("Range", "").strip())
        if not m or (m.group(1) == "" and m.group(2) == ""):
            return super().do_GET()
        if m.group(1) == "":
            inicio, fim = max(0, tamanho - int(m.group(2))), tamanho - 1
        else:
            inicio = int(m.group(1))
            fim = min(int(m.group(2)), tamanho - 1) if m.group(2) else tamanho - 1
        if inicio >= tamanho or inicio > fim:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{tamanho}")
            self.end_headers()
            return
        comprimento = fim - inicio + 1
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(caminho))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {inicio}-{fim}/{tamanho}")
        self.send_header("Content-Length", str(comprimento))
        self.end_headers()
        with open(caminho, "rb") as f:
            f.seek(inicio)
            restante = comprimento
            try:
                while restante > 0:
                    bloco = f.read(min(256 * 1024, restante))
                    if not bloco:
                        break
                    self.wfile.write(bloco)
                    restante -= len(bloco)
            except (BrokenPipeError, ConnectionResetError):
                pass  # o navegador cancelou a requisição (normal com vídeo)


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    pasta, host, porta = sys.argv[1], sys.argv[2], int(sys.argv[3])
    servidor = ThreadingHTTPServer((host, porta), partial(Handler, directory=pasta))
    print(f"Servindo {pasta} em http://{host}:{porta}", flush=True)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
