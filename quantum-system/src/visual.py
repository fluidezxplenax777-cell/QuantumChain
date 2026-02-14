import http.server
import socketserver
import json
import os
import datetime

# CONFIGURAÇÃO DE CAMINHO ABSOLUTO (GPS DO ARQUIVO)
# Isso garante que o site ache o arquivo não importa como iniciou
DATA_FILE = "/data/data/com.termux/files/home/quantum-system/data/genesis.json"
PORT = 8080

class MonitorHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Tenta ler o arquivo do cofre
            status_color = "red"
            status_text = "OFFLINE 🔴"
            balance = "0.00 RC"
            last_hash = "NENHUM BLOCO ENCONTRADO"
            node_id = "DESCONHECIDO"
            timestamp = "N/A"
            entropy = "N/A"

            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, "r") as f:
                        data = json.load(f)
                        status_color = "#00ff00" # Verde Hacker
                        status_text = "ONLINE 🟢 (MINERANDO)"
                        balance = f"{data.get('balance', 0):.2f} RC"
                        last_hash = data.get('hash', 'N/A')
                        node_id = data.get('node_id', 'SAMSUNG_A15_NODE')
                        timestamp = data.get('timestamp', 'N/A')
                        entropy = data.get('entropy_source', 'SISTEMA')
                except Exception as e:
                    last_hash = f"ERRO DE LEITURA: {str(e)}"

            # O HTML DO SITE (FRONTEND)
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>QUANTUMCHAIN MONITOR</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <meta http-equiv="refresh" content="5"> <style>
                    body {{ background-color: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 20px; }}
                    .card {{ border: 1px solid #30363d; padding: 20px; border-radius: 6px; margin-bottom: 20px; background: #161b22; }}
                    h1 {{ color: #58a6ff; font-size: 1.5em; border-bottom: 1px solid #30363d; padding-bottom: 10px; }}
                    .status {{ font-size: 1.2em; font-weight: bold; color: {status_color}; margin: 15px 0; }}
                    .balance {{ font-size: 2.5em; color: #fff; text-shadow: 0 0 10px {status_color}; margin: 20px 0; }}
                    .hash {{ word-break: break-all; color: #8b949e; font-size: 0.8em; background: #0d1117; padding: 10px; border-radius: 4px; }}
                    .footer {{ font-size: 0.7em; color: #484f58; margin-top: 40px; text-align: center; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>QUANTUMCHAIN <span style="font-size:0.6em; color: #8b949e;">ALPHA 1.0</span></h1>
                    <div class="status">{status_text}</div>
                    
                    <div style="font-size: 0.9em; color: #8b949e;">SALDO ACUMULADO</div>
                    <div class="balance">{balance}</div>
                    
                    <div style="font-size: 0.9em; color: #8b949e;">ÚLTIMO HASH (PROOF OF REALITY)</div>
                    <div class="hash">{last_hash}</div>
                    
                    <br>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8em; color: #8b949e;">
                        <span>FONTE: {entropy}</span>
                        <span>{timestamp}</span>
                    </div>
                </div>
                
                <div class="footer">
                    RESSONÂNCIA LABS • ACTIVE ZERO PROTOCOL • MESQUITA/RJ<br>
                    ID: {node_id}
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404)

# INICIALIZAÇÃO DO SERVIDOR
if __name__ == "__main__":
    # Previne erro de porta presa ao reiniciar rápido
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(('0.0.0.0', PORT), MonitorHandler)
    print(f"📡 MONITOR WEB 2.0 ATIVO EM: http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDesligando Monitor...")
        server.server_close()
