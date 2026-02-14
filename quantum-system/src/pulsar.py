import time
import json
import os
import hashlib
import random
from datetime import datetime

# CONFIGURAÇÃO DE CAMINHO ABSOLUTO (CRUCIAL)
DATA_DIR = "/data/data/com.termux/files/home/quantum-system/data"
DATA_FILE = os.path.join(DATA_DIR, "genesis.json")

# GARANTIR QUE A PASTA EXISTE
os.makedirs(DATA_DIR, exist_ok=True)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    # FORÇA A GRAVAÇÃO IMEDIATA NO DISCO (FLUSH)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
        f.flush()
        os.fsync(f.fileno())

def mine():
    print("🦅 PULSAR 3.0 - SISTEMA SINCRONIZADO")
    
    while True:
        # 1. Carregar o estado atual
        data = load_data()
        
        # 2. Recuperar saldo antigo ou começar do zero
        current_balance = data.get("balance", 0.0)
        
        # 3. Minerar (Simulação de esforço)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp.split(' ')[1]}] ⚙️  Forjando bloco...")
        time.sleep(3) # Tempo de mineração
        
        # 4. Gerar Hash e Recompensa
        entropy = str(random.getrandbits(256))
        block_hash = hashlib.sha256(entropy.encode()).hexdigest()
        reward = 1.00
        
        # 5. Atualizar Carteira
        new_balance = current_balance + reward
        
        # 6. O PULO DO GATO: SALVAR COM AS CHAVES CERTAS
        data["balance"] = new_balance  # O Site procura por "balance"
        data["hash"] = block_hash
        data["timestamp"] = timestamp
        data["node_id"] = "SAMSUNG_A15_MINER"
        data["entropy_source"] = "ACTIVE_ZERO_PROTOCOL"
        
        save_data(data)
        
        print(f"✅ SUCESSO! Hash: {block_hash[:15]}...")
        print(f"💰 SALDO ATUALIZADO: {new_balance:.2f} RC")
        print("-" * 40)
        
        # Aguardar próximo ciclo
        time.sleep(5)

if __name__ == "__main__":
    mine()
