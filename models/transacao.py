from abc import ABC, abstractmethod  # Importa módulos para definir classes abstratas
from colorama import Fore, Style  # Importa cores para console
from datetime import datetime  # Importa módulo para manipulação de data/hora
from models.pessoa_fisica import PessoaFisica  # Importa a classe PessoaFisica do módulo models

# Define o caminho do arquivo de clientes
clientes_arquivotxt = "/home/valentinavps/POO/SistemaBancario/clientes.txt"

# Classe abstrata Transacao, serve como base para outras classes de transações
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        pass

    # Método abstrato para registrar a transação (comentado)
    # @abstractmethod
    # def registrar(self, conta: object) -> None:
    #     pass

# Classe Saque que herda de Transacao e implementa os métodos abstratos
class Saque(Transacao):
    def __init__(self) -> None:
        self._valor: float = 0.0  # Inicializa o valor do saque como zero

    @property
    def valor(self) -> float:
        return self._valor  # Retorna o valor do saque

    # Método para realizar um saque
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

        saldo = float(cliente.get('saldo', 0))  # Obtém o saldo atual do cliente
        self._valor = float(input("Informe o valor do saque: "))  # Solicita o valor do saque ao usuário

        # Validações do saque
        if self._valor < 0:
            print(Fore.RED + "\n❌❌❌ Valor Inválido! ❌❌❌")
            print(Style.RESET_ALL)
        elif self._valor > saldo:
            print(Fore.RED + "\n❌❌❌ Saldo insuficiente! ❌❌❌")
            print(Style.RESET_ALL)
        else:
            saldo -= self._valor  # Deduz o valor do saque do saldo do cliente
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
        self._valor: float = 0.0  # Inicializa o valor do depósito como zero

    @property
    def valor(self) -> float:
        return self._valor  # Retorna o valor do depósito

    # Método para realizar um depósito
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

        self._valor = float(input("Informe o valor do depósito: "))  # Solicita o valor do depósito ao usuário

        # Validações do depósito
        if self._valor < 0:
            print(Fore.RED + "\n❌❌❌ Valor Inválido! ❌❌❌")
            print(Style.RESET_ALL)
        else:
            saldo = float(cliente.get('saldo', 0))  # Obtém o saldo atual do cliente
            saldo += self._valor  # Adiciona o valor do depósito ao saldo do cliente
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
