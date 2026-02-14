import os
import hashlib
import time
import struct

class ChaosEngine:
    """
    Usa o hardware do dispositivo (Samsung A15) para capturar
    entropia física e gerar 'seeds' imprevisíveis.
    """
    def __init__(self):
        self.state = self._harvest_entropy()

    def _harvest_entropy(self):
        # Mistura: Tempo em nanosegundos + Bytes aleatórios do Linux + ID do Processo
        raw_data = f"{time.time_ns()}:{os.urandom(64)}:{os.getpid()}"
        return hashlib.sha3_512(raw_data.encode()).hexdigest()

    def get_quantum_random(self, min_val, max_val):
        """Retorna um número entre min e max usando o caos"""
        self.state = self._harvest_entropy() # Renova a entropia
        
        # Converte Hash (Hex) para Inteiro
        hex_chunk = self.state[:16]
        int_val = int(hex_chunk, 16)
        
        # Normaliza
        span = max_val - min_val + 1
        return min_val + (int_val % span)

if __name__ == "__main__":
    chaos = ChaosEngine()
    print(f"⚛️ [QUANTUM-CORE] Estado de Entropia: {chaos.state[:20]}...")
    print(f"🎲 Dado Quântico (1-100): {chaos.get_quantum_random(1, 100)}")
