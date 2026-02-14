import json
import os
from cryptography.fernet import Fernet
import base64
import hashlib

def gerar_chave(senha):
    # Transforma sua senha em uma chave de 32 bytes
    sha256 = hashlib.sha256(senha.encode()).digest()
    return base64.urlsafe_b64encode(sha256)

def blindar():
    caminho_identidade = os.path.expanduser("~/quantum-system/keys/identidade_mestra.json")
    if not os.path.exists(caminho_identidade):
        print("❌ Erro: Identidade não encontrada!")
        return

    senha = input("🔐 Defina a SENHA MESTRA para criptografar sua ID: ")
    chave = gerar_chave(senha)
    f = Fernet(chave)

    with open(caminho_identidade, "rb") as file:
        dados = file.read()
    
    dados_cripto = f.encrypt(dados)

    with open(caminho_identidade + ".vault", "wb") as file:
        file.write(dados_cripto)
    
    # Remove a original sem criptografia por segurança
    os.remove(caminho_identidade)
    print("\n✅ IDENTIDADE BLINDADA! Arquivo .vault criado e original removido.")

blindar()
