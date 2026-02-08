from block import Block
import time
import json
import os

DB_FILE = "QuantumChain/chain_db.json"

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 2
        self.pending_data = []
        
        # Tenta carregar o banco de dados existente
        if os.path.exists(DB_FILE):
            self.load_chain()
        else:
            print("[SISTEMA] Nenhum banco de dados encontrado. Criando Gênese...")
            self.chain = [self.create_genesis_block()]
            self.save_chain()

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis: Active Zero System Online")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.save_chain() # Salva imediatamente após minerar

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash(): return False
            if current.previous_hash != previous.hash: return False
        return True

    def save_chain(self):
        # Converte objetos Block em dicionários para salvar em JSON
        chain_data = []
        for block in self.chain:
            chain_data.append({
                "index": block.index,
                "previous_hash": block.previous_hash,
                "timestamp": block.timestamp,
                "data": block.data,
                "validator_id": block.validator_id,
                "hash": block.hash,
                "nonce": block.nonce
            })
        with open(DB_FILE, "w") as f:
            json.dump(chain_data, f, indent=4)
        print("💾 [DATABASE] Blockchain salva no disco.")

    def load_chain(self):
        print("📂 [DATABASE] Carregando Blockchain do disco...")
        with open(DB_FILE, "r") as f:
            chain_data = json.load(f)
            
        self.chain = []
        for item in chain_data:
            # Reconstrói o objeto Block a partir do JSON
            block = Block(
                item["index"], 
                item["previous_hash"], 
                item["timestamp"], 
                item["data"], 
                item["validator_id"]
            )
            block.hash = item["hash"]
            block.nonce = item["nonce"]
            self.chain.append(block)
        
        print(f"✅ [DATABASE] {len(self.chain)} blocos carregados com sucesso.")
