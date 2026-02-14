import json
import time
import hashlib
import os

# CONFIGURAÇÃO DO COFRE
DATA_DIR = os.path.expanduser("~/quantum-system/data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 1. ENTROPIA
raw_entropy = f"REAL_HW_JITTER_{time.time()}_SAMSUNG_A15_MESQUITA"
block_hash = hashlib.sha256(raw_entropy.encode()).hexdigest()

# 2. BLOCO
genesis_block = {
    "index": 0,
    "timestamp": time.time(),
    "proof": 100,
    "previous_hash": "0" * 64,
    "hash": block_hash,
    "data": {
        "message": "GENESIS BLOCK - RESSONANCIA LABS",
        "location": "BRAZIL_NODE",
        "hardware": "ANDROID_AARCH64"
    }
}

# 3. GRAVAÇÃO
arquivo_final = os.path.join(DATA_DIR, "genesis.json")

with open(arquivo_final, "w") as f:
    json.dump(genesis_block, f, indent=4)

print(f"✅ SUCESSO! Bloco Gênesis forjado.")
print(f"📂 Local: {arquivo_final}")
print(f"🔑 Hash: {block_hash}")
