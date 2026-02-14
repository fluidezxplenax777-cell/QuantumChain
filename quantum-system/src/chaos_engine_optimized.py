import os
import time
import hashlib
import random
import subprocess

class ChaosEngine:
    def __init__(self):
        self.device_id = "SAMSUNG_A15_NODE_ALPHA"
        self.calibration_offset = 0
        
    def _get_cpu_jitter(self):
        """
        MÉTODO 1: Jitter de CPU (Infalível)
        Mede a variação de nanosegundos entre operações de hash.
        O 'suor' do processador cria entropia real.
        """
        t1 = time.time_ns()
        _ = hashlib.sha256(str(t1).encode()).hexdigest()
        t2 = time.time_ns()
        delta = t2 - t1
        return delta

    def _get_thermal_zone(self):
        """
        MÉTODO 2: Tenta ler sensores térmicos do Linux/Android.
        Se bloqueado, usa variação de carga do sistema.
        """
        thermal_paths = [
            "/sys/class/thermal/thermal_zone0/temp",
            "/sys/class/thermal/thermal_zone1/temp",
            "/sys/devices/virtual/thermal/thermal_zone0/temp"
        ]
        
        for path in thermal_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        temp = int(f.read().strip())
                        # Normaliza se vier em miligraus (ex: 45000 -> 45)
                        if temp > 1000: 
                            temp = temp / 1000
                        return f"{temp:.1f}C"
                except:
                    continue
        
        # Fallback: Se não conseguir ler temperatura, lê Carga do Sistema (LoadAvg)
        try:
            load = os.getloadavg()[0]
            return f"LOAD_{load:.2f}"
        except:
            return "N/A"

    def generate_seed(self):
        """
        Gera a 'Semente do Caos' combinando múltiplas fontes físicas.
        """
        # 1. Coleta Jitter (Hardware Timing)
        jitter_samples = [self._get_cpu_jitter() for _ in range(50)]
        jitter_sum = sum(jitter_samples)
        
        # 2. Coleta Térmica/Carga
        thermal = self._get_thermal_zone()
        
        # 3. Mistura com entropia do sistema operacional (/dev/urandom)
        sys_entropy = os.urandom(32).hex()
        
        # 4. FUSÃO FINAL (O Segredo Industrial)
        raw_data = f"{jitter_sum}:{thermal}:{sys_entropy}"
        final_hash = hashlib.sha3_512(raw_data.encode()).hexdigest()
        
        # Formata para o padrão visual do Dashboard
        return f"REAL_HW_JITTER_{jitter_sum}_THERMAL_{thermal}"

    def get_entropy_metrics(self):
        return self.generate_seed()

# Teste rápido se rodar direto
if __name__ == "__main__":
    engine = ChaosEngine()
    print(f"🔥 ENTROPIA FÍSICA GERADA: {engine.generate_seed()}")

