from colorama import Fore, Style
from datetime import datetime

from .historico import Historico


class Conta:
    def __init__(self, numero: str, cliente: Cliente):
        """
        Inicializa um objeto Conta com saldo inicial zero, número da conta, agência fixa "0001", cliente associado e histórico vazio.

        Args:
        - numero (str): Número da conta.
        - cliente (Cliente): Cliente associado à conta.
        """
        self._saldo = 0  # Saldo inicialmente zerado
        self._numero = numero  # Número da conta
        self._agencia = "0001"  # Agência fixa
        self._cliente = cliente  # Cliente associado à conta
        self._historico = Historico()  # Histórico de transações associado à conta

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: str) -> 'Conta':
        """
        Cria uma nova instância de Conta utilizando o método de classe.

        Args:
        - cliente (Cliente): Cliente associado à conta.
        - numero (str): Número da conta.

        Returns:
        - Conta: Nova instância de Conta criada.
        """
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        """
        Retorna o saldo atual da conta.

        Returns:
        - float: Saldo atual da conta.
        """
        return self._saldo

    @property
    def numero(self) -> str:
        """
        Retorna o número da conta.

        Returns:
        - str: Número da conta.
        """
        return self._numero

    @property
    def agencia(self) -> str:
        """
        Retorna a agência da conta.

        Returns:
        - str: Agência da conta.
        """
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        """
        Retorna o cliente associado à conta.

        Returns:
        - Cliente: Cliente associado à conta.
        """
        return self._cliente

    @property
    def historico(self) -> Historico:
        """
        Retorna o histórico de transações da conta.

        Returns:
        - Historico: Histórico de transações da conta.
        """
        return self._historico

    def sacar(self, valor: float) -> bool:
        """
        Realiza um saque na conta, verificando se o valor não excede o saldo disponível e se é um valor positivo.

        Args:
        - valor (float): Valor a ser sacado.

        Returns:
        - bool: True se o saque for bem sucedido, False caso contrário.
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
        Realiza um depósito na conta, verificando se o valor é positivo.

        Args:
        - valor (float): Valor a ser depositado.

        Returns:
        - bool: True se o depósito for bem sucedido, False caso contrário.
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
