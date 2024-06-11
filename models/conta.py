from colorama import Fore, Style
from datetime import datetime

from .historico.py import Historico

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print(Fore.RED + "\n❌❌❌ Operação falhou! Você não tem saldo suficiente. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return False
        elif valor <= 0:
            print(Fore.RED + "\n❌❌❌ Operação falhou! O valor informado é inválido. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        self._saldo -= valor
        print(Fore.GREEN + f"\n✅✅✅ Saque realizado com sucesso! {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ✅✅✅")
        print(Style.RESET_ALL)  # Resetando a cor
        return True

    def depositar(self, valor):
        if valor <= 0:
            print(Fore.RED + "\n❌❌❌ Operação falhou! O valor informado é inválido. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        self._saldo += valor
        print(Fore.GREEN + f"\n✅✅✅ Depósito realizado com sucesso! {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ✅✅✅")
        print(Style.RESET_ALL)  # Resetando a cor
        return True
