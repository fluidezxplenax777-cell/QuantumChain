from blockchain import Blockchain
from block import Block
from wallet import Wallet
from transaction import Transaction
import time

print("\n--- 🌐 INICIANDO QUANTUMCHAIN MAINNET (SIMULAÇÃO) ---")

# 1. Inicializa a Rede
qc_chain = Blockchain()
print(f"Blockchain iniciada. Bloco Gênese criado.")

# 2. Criação de Usuários (Carteiras)
print("\n[1] Gerando Identidades...")
aderlan_wallet = Wallet()
active_zero_wallet = Wallet()
print(f"Carteira Aderlan: {aderlan_wallet.address[:15]}...")
print(f"Carteira ActiveZero: {active_zero_wallet.address[:15]}...")

# 3. Criando uma Transação Rica (Valor + Dados)
print("\n[2] Criando Transação...")
tx1 = Transaction(
    sender_address=aderlan_wallet.address,
    recipient_address=active_zero_wallet.address,
    amount=50,
    data="Insight: A IA deve ter soberania de dados."
)

# 4. Assinando a Transação
print("[3] Aderlan assinando a transação...")
tx1.sign_transaction(aderlan_wallet)

# 5. Validando antes de entrar no Bloco
print("[4] Mempool validando assinatura...")
if tx1.is_valid():
    print("✅ Transação Válida! Autorizada para mineração.")
    
    # Adicionando ao Bloco (Na prática real, haveria uma lista de transações)
    # Como nosso add_block atual aceita qualquer data, passamos a tx convertida
    print("\n[5] Minerando Bloco com a transação...")
    novo_bloco = Block(1, qc_chain.get_latest_block().hash, time.time(), [tx1.to_dict()])
    qc_chain.add_block(novo_bloco)
    
    print(f"🎉 BLOCO MINERADO! Hash: {novo_bloco.hash}")
    print(f"📦 Conteúdo do Bloco: {novo_bloco.data}")

else:
    print("❌ ERRO: Assinatura inválida. Transação rejeitada.")

print("\n--- FIM DA SIMULAÇÃO ---")
