from blockchain import Blockchain
from block import Block
from wallet import Wallet
from transaction import Transaction
import time
import sys

# Cores para o terminal
CYAN = '\033[96m'; GREEN = '\033[92m'; YELLOW = '\033[93m'; RESET = '\033[0m'

def menu():
    print(f"\n{CYAN}=== QUANTUMCHAIN NODE v1.0 ==={RESET}")
    print("1. Criar Nova Carteira")
    print("2. Minerar Bloco (Registrar Dados)")
    print("3. Ver Blockchain (Inspecionar)")
    print("4. Validar Integridade")
    print("5. Sair")
    return input(f"{YELLOW}Escolha > {RESET}")

def run():
    print("Inicializando QuantumChain...")
    qc = Blockchain()
    current_wallet = None

    while True:
        op = menu()
        
        if op == '1':
            current_wallet = Wallet()
            print(f"\n{GREEN}Carteira Criada!{RESET}")
            print(f"Endereço: {current_wallet.address}")
            print("Guarde sua chave privada (no código ela fica na memória).")

        elif op == '2':
            if not current_wallet:
                print(f"{CYAN}Criando carteira temporária para mineração...{RESET}")
                current_wallet = Wallet()
            
            data_input = input("Digite os dados para gravar no bloco (Ex: Insight IA): ")
            
            # Criação simplificada da transação (Coinbase/Recompensa)
            tx = Transaction("Mining_Reward", current_wallet.address, 10, data=data_input)
            
            print("Minerando...")
            new_block = Block(len(qc.chain), qc.get_latest_block().hash, time.time(), [tx.to_dict()])
            qc.add_block(new_block)
            print(f"{GREEN}Bloco Minerado! Hash: {new_block.hash}{RESET}")

        elif op == '3':
            print("\n--- LIVRO RAZÃO ---")
            for block in qc.chain:
                print(f"[{block.index}] Hash: {block.hash[:15]}... | Dados: {str(block.data)[:50]}...")

        elif op == '4':
            if qc.is_chain_valid():
                print(f"{GREEN}Integridade da Rede: 100% OK{RESET}")
            else:
                print(f"\033[91mALERTA: CORRUPÇÃO DETECTADA NA REDE!{RESET}")

        elif op == '5':
            print("Encerrando nó...")
            sys.exit()

if __name__ == "__main__":
    run()
