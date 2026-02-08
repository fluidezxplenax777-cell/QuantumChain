from block import Block
import time

print("--- INICIANDO GÊNESE QUANTUMCHAIN ---")

# Criando o Bloco Gênese (O Marco Zero)
genesis_data = "Dados Iniciais: O Início de Tudo"
genesis_block = Block(0, "0", time.time(), genesis_data, validator_id="ActiveZero")

print(f"Bloco Gênese criado: {genesis_block}")
print(f"Hash Gênese: {genesis_block.hash}")

print("\n--- MINERANDO BLOCO 1 (SIMULAÇÃO) ---")
# Criando um bloco real com dados de IA
ai_data = {"insight": "A consciência precede a matéria", "confianca": 0.98}
block1 = Block(1, genesis_block.hash, time.time(), ai_data, validator_id="QuantumCore-Alpha")

print("Minerando...")
block1.mine_block(4) # Dificuldade 4 (vai demorar uns segundos)
print(f"Bloco 1 minerado e selado: {block1}")
