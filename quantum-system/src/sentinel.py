import time
import json
import os
import requests
import subprocess

# TENTA PEGAR AS CHAVES DO AMBIENTE
TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("TG_ID")
DATA_FILE = "/data/data/com.termux/files/home/quantum-system/data/genesis.json"
LOG_FILE = "/data/data/com.termux/files/home/quantum-system/logs/tunnel.log"

# SE NÃO ACHAR NO AMBIENTE, TENTA LER DO ARQUIVO DE BOOT (Fallback)
if not TOKEN or not CHAT_ID:
    try:
        with open("/data/data/com.termux/files/home/.termux/boot/start_quantum.sh", "r") as f:
            content = f.read()
            import re
            token_match = re.search(r'export TG_TOKEN="(.*?)"', content)
            id_match = re.search(r'export TG_ID="(.*?)"', content)
            if token_match: TOKEN = token_match.group(1)
            if id_match: CHAT_ID = id_match.group(1)
    except:
        pass

if not TOKEN or not CHAT_ID:
    print("❌ ERRO: Não achei seu Token ou ID. Verifique o start_quantum.sh")
    exit()

URL_BASE = f"https://api.telegram.org/bot{TOKEN}/"

def send_msg(texto):
    url = URL_BASE + f"sendMessage?chat_id={CHAT_ID}&text={texto}&parse_mode=Markdown"
    try: requests.get(url)
    except: pass

def get_updates(offset):
    url = URL_BASE + f"getUpdates?offset={offset}&timeout=10"
    try:
        return requests.get(url, timeout=15).json()
    except:
        return None

def main():
    print(f"🦅 SENTINELA LIGADO! (ID: {CHAT_ID})")
    print("⏳ Aguardando comandos no Telegram...")
    send_msg("🦅 *REINICIADO*: Estou ouvindo. Digite `/status`")
    
    offset = 0
    while True:
        updates = get_updates(offset)
        if updates and "result" in updates:
            for item in updates["result"]:
                try:
                    update_id = item["update_id"]
                    if "message" in item and "text" in item["message"]:
                        texto = item["message"]["text"].lower().strip()
                        print(f"📩 MENSAGEM RECEBIDA: {texto}")
                        
                        if texto == "/status":
                            # Ler Saldo
                            try:
                                with open(DATA_FILE, "r") as f:
                                    d = json.load(f)
                                    msg = f"💰 *SALDO:* `{d.get('balance',0):.2f} RC`\n🔌 *Hash:* `{d.get('hash','?')[:8]}...`"
                            except: msg = "⚠️ Erro ao ler cofre."
                            send_msg(msg)
                            print("✅ Resposta enviada.")

                    offset = update_id + 1
                except Exception as e:
                    print(f"Erro: {e}")
        time.sleep(2)

if __name__ == "__main__":
    main()
