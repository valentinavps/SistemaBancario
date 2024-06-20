from abc import ABC, abstractmethod
from colorama import Fore, Style
from datetime import datetime
from models.pessoa_fisica import PessoaFisica

# Define os caminhos dos arquivos de clientes e transações
clientes_arquivotxt = "/home/valentinavps/POO/SistemaBancario/clientes.txt"

# Classe abstrata Transacao, que serve como base para outras classes de transações
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        pass

    # @abstractmethod
    # def registrar(self, conta: object) -> None:
    #     pass

# Classe Saque que herda de Transacao e implementa os métodos abstratos
class Saque(Transacao):
    def __init__(self) -> None:
        self._valor: float = 0.0

    @property
    def valor(self) -> float:
        return self._valor

    # def registrar(self, conta: object) -> None:
    #     sucesso_transacao: bool = conta.sacar(self.valor)
    #     if sucesso_transacao:
    #         conta.historico.adicionar_transacao(self, conta)

    # Realiza um saque
    def sacar(self) -> None:
        cpf = input("Informe o CPF do cliente: ")
        cliente = PessoaFisica("nome", "data_nascimento", cpf, "endereco", "senha").filtrar_cliente(cpf)

        if not cliente:
            print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
            print(Style.RESET_ALL)
            return
        
        senha = input("Informe sua senha: ")
        autenticacao = PessoaFisica("nome", "data_nascimento", cpf, "endereco", senha).autenticacao(cpf, senha)

        if not autenticacao:
            print(Fore.RED + "\n❌❌❌ Senha Incorreta! ❌❌❌")
            print(Style.RESET_ALL)
            return

        saldo = float(cliente.get('saldo', 0))  # Pega o saldo do cliente
        self._valor = float(input("Informe o valor do saque: "))
        if self._valor < 0:
            print(Fore.RED + "\n❌❌❌ Valor Inválido! ❌❌❌")
            print(Style.RESET_ALL)
        elif self._valor > saldo:
            print(Fore.RED + "\n❌❌❌ Saldo insuficiente! ❌❌❌")
            print(Style.RESET_ALL)
        else:
            saldo -= self._valor
            cliente['saldo'] = str(saldo)  # Atualiza o saldo no dicionário do cliente

            # Atualiza o saldo no arquivo de clientes
            with open(clientes_arquivotxt, 'r') as file:
                linhas = file.readlines()

            with open(clientes_arquivotxt, 'w') as file:
                for linha in linhas:
                    if linha.startswith(f"cpf:{cpf}"):
                        partes = linha.strip().split('|')
                        for i, parte in enumerate(partes):
                            if parte.startswith('saldo:'):
                                partes[i] = f"saldo:{saldo}"
                        file.write('|'.join(partes) + '\n')
                    else:
                        file.write(linha)

            data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            # Escreve no arquivo de log
            with open("log.txt", "a") as file:
                file.write(f"Transacao Realizada: cpf: {cpf}|saldo: {saldo} ({data_hora})\n")

            print(Fore.GREEN + f"\n✅✅✅ Saque realizado com sucesso! {data_hora} ✅✅✅")
            print(Style.RESET_ALL)

# Classe Deposito que herda de Transacao e implementa os métodos abstratos
class Deposito(Transacao):
    def __init__(self) -> None:
        self._valor: float = 0.0

    @property
    def valor(self) -> float:
        return self._valor

    # def registrar(self, conta: object) -> None:
    #     sucesso_transacao: bool = conta.depositar(self.valor)
    #     if sucesso_transacao:
    #         conta.historico.adicionar_transacao(self, conta)

    # Realiza um depósito
    def deposito(self) -> None:
        cpf = input("Informe o CPF do cliente: ")
        cliente = PessoaFisica("nome", "data_nascimento", cpf, "endereco", "senha").filtrar_cliente(cpf)

        if not cliente:
            print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
            print(Style.RESET_ALL)
            return
        
        senha = input("Informe sua senha: ")
        autenticacao = PessoaFisica("nome", "data_nascimento", cpf, "endereco", senha).autenticacao(cpf, senha)

        if not autenticacao:
            print(Fore.RED + "\n❌❌❌ Senha Incorreta! ❌❌❌")
            print(Style.RESET_ALL)
            return

        self._valor = float(input("Informe o valor do depósito: "))
        if self._valor < 0:
            print(Fore.RED + "\n❌❌❌ Valor Inválido! ❌❌❌")
            print(Style.RESET_ALL)
        else:
            saldo = float(cliente.get('saldo', 0))  # Pega o saldo do cliente
            saldo += self._valor
            cliente['saldo'] = str(saldo)  # Atualiza o saldo no dicionário do cliente

            # Atualiza o saldo no arquivo de clientes
            with open(clientes_arquivotxt, 'r') as file:
                linhas = file.readlines()

            with open(clientes_arquivotxt, 'w') as file:
                for linha in linhas:
                    if linha.startswith(f"cpf:{cpf}"):
                        partes = linha.strip().split('|')
                        for i, parte in enumerate(partes):
                            if parte.startswith('saldo:'):
                                partes[i] = f"saldo:{saldo}"
                        file.write('|'.join(partes) + '\n')
                    else:
                        file.write(linha)

            data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            # Escreve no arquivo de log
            with open("log.txt", "a") as file:
                file.write(f"Depósito Realizado: cpf: {cpf}|saldo: {saldo} ({data_hora})\n")

            print(Fore.GREEN + f"\n✅✅✅ Depósito realizado com sucesso! {data_hora} ✅✅✅")
            print(Style.RESET_ALL)