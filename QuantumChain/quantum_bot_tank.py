import os
import time
import json
import subprocess
from blockchain import Blockchain

# CONFIGURAÇÃO
REPO_DIR = os.path.expanduser("~/quantum-live")
JSON_FILE = "data.json"
WAKELOCK_CMD = "termux-wake-lock"
UNLOCK_CMD = "termux-wake-unlock"

def acquire_wakelock():
    try:
        subprocess.run([WAKELOCK_CMD], check=True)
        print("⚡ WakeLock Ativo.")
    except Exception as e:
        print(f"⚠️  Falha no WakeLock: {e}")

def release_wakelock():
    try:
        subprocess.run([UNLOCK_CMD])
        print("💤 WakeLock Liberado.")
    except:
        pass

def check_battery():
    # Verifica se bateria > 15% para não matar o cel
    try:
        result = subprocess.run(["termux-battery-status"], capture_output=True, text=True)
        data = json.loads(result.stdout)
        pct = data.get("percentage", 100)
        is_charging = data.get("plugged", "") != "UNPLUGGED"
        
        if pct < 15 and not is_charging:
            print(f"🪫 Bateria Crítica ({pct}%). Encerrando para proteção.")
            return False
        return True
    except:
        return True # Se der erro na leitura, assume que tá ok (Tanque de Guerra)

def git_push_force():
    # A Doutrina da Verdade Única: O Celular Manda.
    os.chdir(REPO_DIR)
    
    # Adiciona, Commita e Força a subida
    subprocess.run(["git", "add", "."], stdout=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", f"Sync {time.strftime('%H:%M')}"], stdout=subprocess.DEVNULL)
    
    # Push Force para evitar Merge Hell
    result = subprocess.run(["git", "push", "--force"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ [{time.strftime('%H:%M')}] DADOS NA NUVEM.")
        return True
    else:
        print(f"❌ Erro Git: {result.stderr.strip()}")
        return False

def run_tank():
    print("--- 🤖 QUANTUM BOT: MODELO TANQUE ---")
    acquire_wakelock()
    
    last_hash = ""
    
    try:
        while True:
            # 1. Checagem de Sobrevivência
            if not check_battery():
                break
                
            # 2. Leitura da Blockchain
            try:
                qc = Blockchain()
                qc.load_chain()
                latest = qc.get_latest_block()
                
                # Só sobe se mudou
                if latest.hash != last_hash:
                    # Gera JSON
                    public_data = {
                        "status": "OPERATIONAL",
                        "updated": time.ctime(),
                        "height": latest.index,
                        "hash": latest.hash,
                        "data": latest.data
                    }
                    
                    with open(os.path.join(REPO_DIR, JSON_FILE), "w") as f:
                        json.dump(public_data, f, indent=4)
                    
                    # Push
                    if git_push_force():
                        last_hash = latest.hash
                else:
                    print(".", end="", flush=True) # Heartbeat
                    
            except Exception as e:
                print(f"⚠️ Erro no Loop: {e}")
            
            # Dorme 5 minutos (300s) para economizar recurso
            time.sleep(300)
            
    except KeyboardInterrupt:
        print("\n🛑 Parando...")
    finally:
        release_wakelock()

if __name__ == "__main__":
    run_tank()
