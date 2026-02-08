from blockchain import Blockchain
from block import Block
from wallet import Wallet
from transaction import Transaction
import time
import requests
import json

# ALVOS REAIS (Binance é mais robusta)
ALVOS = [
    {"nome": "API Bitcoin (Binance)", "url": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"},
    {"nome": "Google BR", "url": "https://www.google.com.br"},
    {"nome": "GitHub Status", "url": "https://www.githubstatus.com/api/v2/status.json"}
]

def verificar_alvo(alvo):
    inicio = time.time()
    try:
        response = requests.get(alvo['url'], timeout=10)
        fim = time.time()
        latencia = round((fim - inicio) * 1000, 2)
        
        status = "ONLINE" if response.status_code == 200 else f"ERRO {response.status_code}"
        
        dados_extra = ""
        # Lógica para Binance
        if "Bitcoin" in alvo['nome'] and status == "ONLINE":
            try:
                preco = float(response.json()['price'])
                dados_extra = f" | BTC: ${preco:.2f}"
            except:
                dados_extra = " | Erro ao ler JSON"
            
        return f"[SCOUT REPORT] {alvo['nome']}: {status} em {latencia}ms{dados_extra}"
    except Exception as e:
        return f"[SCOUT FALHA] {alvo['nome']}: {str(e)}"

def run_scout():
    print("--- 🦅 AGENTE BATEDOR v2 (Mira Corrigida) ---")
    qc = Blockchain()
    scout_wallet = Wallet()
    
    cycle = 1
    while True:
        print(f"\n[MISSÃO {cycle}] Selecionando alvo...")
        alvo_atual = ALVOS[cycle % len(ALVOS)]
        
        resultado = verificar_alvo(alvo_atual)
        print(f"👁️  Visão: {resultado}")
        
        tx = Transaction("Service_Payment", scout_wallet.address, 50, data=resultado)
        new_block = Block(len(qc.chain), qc.get_latest_block().hash, time.time(), [tx.to_dict()])
        qc.add_block(new_block)
        
        print(f"✅ PROVA GRAVADA! Bloco {new_block.index}")
        time.sleep(15) # Acelerado para 15s para testarmos logo
        cycle += 1
        qc = Blockchain()

if __name__ == "__main__":
    run_scout()
