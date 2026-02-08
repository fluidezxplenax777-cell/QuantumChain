import time
from wallet import verify_signature

class Transaction:
    def __init__(self, sender_address, recipient_address, amount, data=None):
        self.sender = sender_address
        self.recipient = recipient_address
        self.amount = amount
        self.data = data # Pode ser um insight de IA ou mensagem
        self.timestamp = time.time()
        self.signature = None # Será preenchido após assinar

    def sign_transaction(self, wallet):
        # Garante que só o dono da carteira pode assinar
        if wallet.address != self.sender:
            raise Exception("ERRO: Você não pode assinar transações de outra carteira!")
        
        # Cria o hash do conteúdo para assinar
        content = f"{self.sender}{self.recipient}{self.amount}{self.data}"
        self.signature = wallet.sign_transaction(content)

    def is_valid(self):
        # Se for transação de mineração (recompensa do sistema), não tem remetente
        if self.sender == "Mining_Reward":
            return True

        if not self.signature:
            print("ERRO: Transação sem assinatura!")
            return False

        # Verifica a criptografia
        content = f"{self.sender}{self.recipient}{self.amount}{self.data}"
        return verify_signature(self.sender, content, self.signature)

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "data": self.data,
            "signature": self.signature
        }
