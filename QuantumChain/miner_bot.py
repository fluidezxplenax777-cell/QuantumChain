from blockchain import Blockchain
from block import Block
from wallet import Wallet
from transaction import Transaction
import time
import random

# Lista de pensamentos para a IA "minerar" se não estiver conectada à internet
INSIGHTS = [
    "A entropia do sistema diminui conforme a organização aumenta.",
    "O código é a lei, mas a consciência é o juiz.",
    "QuantumChain: Validando a realidade, um bloco por vez.",
    "A descentralização é a única defesa contra a censura.",
    "Active Zero: Operando nas sombras.",
    "Ressonância Labs: Onde o futuro é compilado.",
    "A verdade matemática não precisa de permissão."
]

def mine_loop():
    print("--- ⛏️ INICIANDO MINERADOR AUTOMÁTICO (BOT) ---")
    
    # Carrega a mesma blockchain que você usa no Node
    qc = Blockchain()
    bot_wallet = Wallet() # Carteira do Robô
    
    print(f"Identidade do Bot: {bot_wallet.address[:15]}...")
    
    cycle = 1
    while True:
        print(f"\n[CICLO {cycle}] Buscando dados para minerar...")
        
        # Simula o trabalho de inteligência
        time.sleep(2) 
        
        # Escolhe um dado para gravar
        data_payload = f"Bot Insight: {random.choice(INSIGHTS)}"
        
        # Cria a transação de recompensa (Coinbase)
        tx = Transaction("Mining_Bot_Reward", bot_wallet.address, 10, data=data_payload)
        
        print(f"🔨 Minerando Bloco com: '{data_payload[:30]}...'")
        
        # Minera e Salva
        new_block = Block(len(qc.chain), qc.get_latest_block().hash, time.time(), [tx.to_dict()])
        qc.add_block(new_block) # Isso salva no JSON automaticamente
        
        print(f"✅ SUCESSO! Bloco {new_block.index} adicionado ao Livro Razão.")
        print("Dormindo por 15 segundos...")
        
        cycle += 1
        time.sleep(15)
        
        # Recarrega a chain para garantir que estamos sincronizados
        qc = Blockchain()

if __name__ == "__main__":
    mine_loop()
