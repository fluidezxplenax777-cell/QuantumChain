import os
import json
import time
import hashlib
import random
from datetime import datetime

# --- CONFIGURAÇÃO ---
PASTA_PROJETO = "QuantumChain"
ARQUIVO_DB = os.path.join(PASTA_PROJETO, "chain_db.json")

# Garante que a pasta existe
if not os.path.exists(PASTA_PROJETO):
    os.makedirs(PASTA_PROJETO)

# --- FUNÇÕES CORE ---

def carregar_chain():
    if not os.path.exists(ARQUIVO_DB):
        return []
    try:
        with open(ARQUIVO_DB, "r") as f:
            return json.load(f)
    except:
        return []

def salvar_chain(chain):
    with open(ARQUIVO_DB, "w") as f:
        json.dump(chain, f, indent=4)
    print(f"\n[💾] Dados salvos em {ARQUIVO_DB}!")

def calcular_hash(bloco):
    bloco_string = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(bloco_string).hexdigest()

def gerar_id_anonimo():
    # Gera um ID único baseado em entropia do sistema (sem nome real)
    salt = str(time.time()) + str(random.randint(0, 100000))
    return "0xNODE_" + hashlib.sha256(salt.encode()).hexdigest()[:8]

def minerar_bloco(dados):
    chain = carregar_chain()
    
    # Pega o hash do ultimo bloco
    last_hash = "0"
    index = 1
    if len(chain) > 0:
        last_block = chain[-1]
        last_hash = calcular_hash(last_block)
        index = last_block['index'] + 1

    # CRIAÇÃO DO BLOCO (Agora Anônimo)
    novo_bloco = {
        "index": index,
        "timestamp": str(datetime.now()),
        "dados": dados,
        "previous_hash": last_hash,
        "criador": gerar_id_anonimo() # <--- AQUI ESTÁ A MUDANÇA
    }

    print("\n[⛏️] Minerando bloco no Submundo...")
    time.sleep(1) 
    
    chain.append(novo_bloco)
    salvar_chain(chain)
    print(f"[✅] BLOCO #{index} ADICIONADO (ID: {novo_bloco['criador']})")

def ver_chain():
    chain = carregar_chain()
    if not chain:
        print("\n[!] Blockchain vazia.")
        return
    
    print(f"\n--- 🔗 BLOCKCHAIN ACTIVE ZERO ({len(chain)} Blocos) ---")
    for bloco in chain:
        print(f"[{bloco['index']}] {bloco['timestamp']} | Criador: {bloco['criador']}")
        print(f"    Dado: {bloco['dados']}")
        print("---")

# --- MENU PRINCIPAL ---

def menu():
    while True:
        os.system('clear')
        print("\n=== 🕵️ ACTIVE ZERO: MODO FANTASMA ===")
        print("1. 📝 Minerar Novo Bloco (Anônimo)")
        print("2. 👁️ Ver Blockchain")
        print("3. ❌ Sair")
        
        escolha = input("\n>>> Escolha: ")

        if escolha == '1':
            dado = input("\nDigite o dado para gravar: ")
            minerar_bloco(dado)
            input("\n[ENTER] para voltar...")
        elif escolha == '2':
            ver_chain()
            input("\n[ENTER] para voltar...")
        elif escolha == '3':
            print("Saindo...")
            break

if __name__ == "__main__":
    menu()

