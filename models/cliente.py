from .historico import Historico
from .conta import Conta
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        conta.historico.adicionar_transacao(transacao, conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def imprimir_contas(self):
        for conta in self.contas:
            print(conta)


