from colorama import Fore, Style
from datetime import datetime
from typing import Type

from .historico import Historico


class Conta:
    def __init__(self, numero: str):
        """
        Inicializa uma nova conta com o número fornecido.

        Args:
            numero (str): O número da conta.
        """
        self._saldo: float = 0  # Saldo inicialmente zerado
        self._numero: str = numero  # Número da conta
        self._agencia: str = "0001"  # Agência fixa
        # Histórico de transações associado à conta
        self._historico: Historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Type['Cliente'], numero: str) -> 'Conta':
        """
        Cria uma nova conta associada a um cliente.

        Args:
            cliente (Cliente): O cliente associado à conta.
            numero (str): O número da conta.

        Returns:
            Conta: Uma nova instância de Conta.
        """
        return cls(numero)

    @property
    def saldo(self) -> float:
        """
        Retorna o saldo da conta.

        Returns:
            float: O saldo da conta.
        """
        return self._saldo

    @property
    def numero(self) -> str:
        """
        Retorna o número da conta.

        Returns:
            str: O número da conta.
        """
        return self._numero

    @property
    def agencia(self) -> str:
        """
        Retorna a agência da conta.

        Returns:
            str: A agência da conta.
        """
        return self._agencia

    @property
    def historico(self) -> Historico:
        """
        Retorna o histórico de transações da conta.

        Returns:
            Historico: O histórico de transações da conta.
        """
        return self._historico

    def sacar(self, valor: float) -> bool:
        """
        Realiza um saque na conta, se o valor for válido e houver saldo suficiente.

        Args:
            valor (float): O valor a ser sacado.

        Returns:
            bool: True se o saque foi realizado com sucesso, False caso contrário.
        """
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
        print(Fore.GREEN + f"\n✅✅✅ Saque realizado com sucesso! {
              datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ✅✅✅")
        print(Style.RESET_ALL)  # Resetando a cor
        return True

    def depositar(self, valor: float) -> bool:
        """
        Realiza um depósito na conta, se o valor for válido.

        Args:
            valor (float): O valor a ser depositado.

        Returns:
            bool: True se o depósito foi realizado com sucesso, False caso contrário.
        """
        if valor <= 0:
            print(Fore.RED + "\n❌❌❌ Operação falhou! O valor informado é inválido. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        self._saldo += valor
        print(Fore.GREEN + f"\n✅✅✅ Depósito realizado com sucesso! {
              datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ✅✅✅")
        print(Style.RESET_ALL)  # Resetando a cor
        return True
