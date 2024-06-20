from colorama import Fore, Style
from .conta import Conta
from models.transacao import Saque


class ContaCorrente(Conta):
    def __init__(self, numero: str, cliente: Cliente, limite: float = 500, limite_saques: int = 3):
        """
        Inicializa um objeto ContaCorrente com número, cliente associado, limite de saldo negativo e limite de saques.

        Args:
        - numero (str): Número da conta corrente.
        - cliente (Cliente): Cliente associado à conta.
        - limite (float, optional): Limite de saldo negativo permitido. Default é 500.
        - limite_saques (int, optional): Número máximo de saques permitidos. Default é 3.
        """
        super().__init__(numero, cliente)
        self._limite = limite  # Limite de saldo negativo permitido
        self._limite_saques = limite_saques  # Número máximo de saques permitidos

    def sacar(self, valor: float) -> bool:
        """
        Realiza um saque na conta corrente, verificando se o valor não excede o limite de saldo negativo ou o número máximo de saques.

        Args:
        - valor (float): Valor a ser sacado.

        Returns:
        - bool: True se o saque for bem sucedido, False caso contrário.
        """
        numero_saques = sum(
            1
            for transacao in self.historico.transacoes
            if transacao["tipo"] == Saque.__name__
        )
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(
                Fore.RED + "\n❌❌❌ Operação falhou! O valor do saque excede o limite. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        elif excedeu_saques:
            print(
                Fore.RED + "\n❌❌❌ Operação falhou! Número máximo de saques excedido. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        return super().sacar(valor)  # Chama o método sacar da classe Conta (superclasse)

    def __str__(self) -> str:
        """
        Retorna uma representação em string dos detalhes da conta corrente.

        Returns:
        - str: Representação em string dos detalhes da conta corrente.
        """
        return f"""{Fore.WHITE}
    ========== CONTA CORRENTE ==========
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
    {Style.RESET_ALL}"""
