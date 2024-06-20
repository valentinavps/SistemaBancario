from colorama import Fore, Style
from datetime import datetime
from typing import Type

from .historico import Historico


class Conta:
    def __init__(self, numero: str):
        self._saldo = 0  # Saldo inicialmente zerado
        self._numero = numero  # Número da conta
        self._agencia = "0001"  # Agência fixa
        # self._cliente = cliente  # Cliente associado à conta
        self._historico = Historico()  # Histórico de transações associado à conta

    @classmethod
    def nova_conta(cls, cliente, numero: str) -> 'Conta':
    
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> str:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    # @property
    # def cliente(self):
    #     return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    def sacar(self, valor: float) -> bool:
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

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print(Fore.RED + "\n❌❌❌ Operação falhou! O valor informado é inválido. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        self._saldo += valor
        print(Fore.GREEN + f"\n✅✅✅ Depósito realizado com sucesso! {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ✅✅✅")
        print(Style.RESET_ALL)  # Resetando a cor
        return True
