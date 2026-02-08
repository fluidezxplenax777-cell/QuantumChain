from blockchain import Blockchain
from block import Block
import time

print("\n--- INICIANDO REDE QUANTUMCHAIN (MODO TESTE) ---")
qc_net = Blockchain()

print("Minerando Bloco 1 (Dados: Projeto Ressonancia)...")
qc_net.add_block(Block(1, "", time.time(), {"projeto": "RessonanciaLabs", "status": "Vivo"}))

print("Minerando Bloco 2 (Dados: Projeto Submundo)...")
qc_net.add_block(Block(2, "", time.time(), {"projeto": "SubmundoStudios", "status": "Kira 7 Criado"}))

print(f"\n[ESTADO DA REDE]: {qc_net}")

# VERIFICAÇÃO DE INTEGRIDADE
print("\nVerificando integridade da corrente...")
if qc_net.is_chain_valid():
    print("✅ [SUCESSO] A Blockchain é válida e íntegra.")
else:
    print("❌ [ERRO] A Blockchain foi corrompida!")

# SIMULAÇÃO DE ATAQUE HACKER
print("\n--- ⚠️  SIMULANDO ATAQUE HACKER ---")
print("Alterando dados do Bloco 1 na força bruta...")
qc_net.chain[1].data = {"projeto": "RessonanciaLabs", "status": "HACKEADO POR TERCEIROS"}

print("Verificando integridade pós-ataque...")
if qc_net.is_chain_valid():
    print("❌ [FALHA] O sistema não detectou o ataque.")
else:
    print("🛡️ [DEFESA ATIVA] O sistema detectou a alteração! A corrente é INVÁLIDA.")
