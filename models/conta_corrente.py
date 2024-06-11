from colorama import Fore, Style
from .conta import Conta
from models.transacao import Saque


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = sum(
            1
                        for transacao in self.historico.transacoes
            if transacao["tipo"] == Saque.__name__
        )
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(Fore.RED + "\n❌❌❌ Operação falhou! O valor do saque excede o limite. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        elif excedeu_saques:
            print(Fore.RED + "\n❌❌❌ Operação falhou! Número máximo de saques excedido. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""{Fore.WHITE}
    ========== CONTA CORRENTE ==========
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
    {Style.RESET_ALL}"""

