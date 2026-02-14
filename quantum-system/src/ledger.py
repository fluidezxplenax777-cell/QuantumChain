import sqlite3
import os

DB_PATH = os.path.expanduser("~/quantum-system/data/ledger.db")

def iniciar_banco():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            block_hash TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

def total_creditos():
    if not os.path.exists(DB_PATH): return 0.0
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(amount) FROM credits')
        total = cursor.fetchone()[0]
        conn.close()
        return total if total else 0.0
    except: return 0.0

def adicionar_credito(block_hash, amount=1.0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO credits (block_hash, amount) VALUES (?, ?)', (block_hash, amount))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    iniciar_banco()
    print(f"✅ BANCO ATIVO | Saldo: {total_creditos()} RC")
