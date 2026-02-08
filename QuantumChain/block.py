import hashlib
import time
import json

class Block:
    def __init__(self, index, previous_hash, timestamp, data, validator_id="Genesis"):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data  # Aqui entram os "Insights" do QuantumCore, não apenas moedas
        self.validator_id = validator_id # ID do QuantumCore que validou (PoI)
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # O hash deve considerar o conteúdo complexo (dados de IA)
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "validator_id": self.validator_id,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        # Simulação de PoW (Proof of Work) temporária até implementarmos o PoI completo
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        # Em breve: Substituir isso por "validate_intelligence()"
        print(f"Bloco minerado: {self.hash}")

    def __repr__(self):
        return f"Block(Index: {self.index}, Hash: {self.hash[:10]}...)"
