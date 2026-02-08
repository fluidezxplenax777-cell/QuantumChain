import ecdsa
import binascii

class Wallet:
    def __init__(self):
        # Cria o par de chaves usando a Curva Elíptica (SECP256k1 - mesma do Bitcoin)
        self._private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self._public_key = self._private_key.get_verifying_key()

    def sign_transaction(self, data):
        # Assina digitalmente os dados com a chave privada
        # Se os dados mudarem 1 vírgula, a assinatura falha.
        signature = self._private_key.sign(data.encode())
        return binascii.hexlify(signature).decode()

    @property
    def address(self):
        # O endereço público é a versão hexadecimal da chave pública
        pub_key_bytes = self._public_key.to_string()
        return binascii.hexlify(pub_key_bytes).decode()

def verify_signature(public_key_hex, data, signature_hex):
    # Qualquer um na rede pode verificar se a assinatura é válida
    public_key_bytes = binascii.unhexlify(public_key_hex)
    verifying_key = ecdsa.VerifyingKey.from_string(public_key_bytes, curve=ecdsa.SECP256k1)
    try:
        signature_bytes = binascii.unhexlify(signature_hex)
        return verifying_key.verify(signature_bytes, data.encode())
    except ecdsa.BadSignatureError:
        return False

# TESTE RÁPIDO (Se rodar direto)
if __name__ == "__main__":
    print("--- GERANDO IDENTIDADE QUANTUM ---")
    minha_carteira = Wallet()
    print(f"Meu Endereço: {minha_carteira.address[:20]}...")
    
    mensagem = "Aderlan transfere 10 Q-Tokens para ActiveZero"
    assinatura = minha_carteira.sign_transaction(mensagem)
    print(f"Assinatura Digital: {assinatura[:20]}...")
    
    print("\n--- VERIFICANDO AUTENTICIDADE ---")
    is_valid = verify_signature(minha_carteira.address, mensagem, assinatura)
    print(f"Assinatura Válida? {is_valid}")
    
    print("\n--- TENTATIVA DE FALSIFICAÇÃO ---")
    falso = "Aderlan transfere 1000000 Q-Tokens para Hacker"
    is_valid_fake = verify_signature(minha_carteira.address, falso, assinatura)
    print(f"Assinatura Válida para msg falsa? {is_valid_fake}")
