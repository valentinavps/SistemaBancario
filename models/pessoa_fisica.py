from colorama import Fore, Style  # Importa módulos necessários
from typing import List
from models.conta import Conta
# from models.conta_corrente import ContaCorrente  # Não utilizado neste trecho de código
from datetime import datetime
# Importa apenas o Saque, talvez devesse importar mais
from models.transacao import Saque
# Importa função específica de helpers
from utils.helpers import recuperar_conta_cliente
import random

# Caminhos para arquivos de dados
clientes_arquivotxt = "/home/valentinavps/POO/SistemaBancario/clientes.txt"
contas_arquivotxt = "/home/valentinavps/POO/SistemaBancario/contas.txt"
transacoes_arquivotxt = "/home/valentinavps/POO/SistemaBancario/transacoes.txt"


class PessoaFisica:
    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str, senha: str):
        """
        Inicializa uma instância de PessoaFisica com atributos básicos.
        """
        self.endereco = endereco  # Tipo: str
        self.nome = nome  # Tipo: str
        self.cpf = cpf  # Tipo: str
        self.data_nascimento = data_nascimento  # Tipo: str
        self.__senha = senha  # Tipo: str (atributo privado)

        self.clientes = []  # Lista vazia para armazenar clientes

    @property
    def senha(self) -> str:
        """
        Getter para retornar a senha (privada).
        """
        return self.__senha

    @senha.setter
    def senha(self, nova_senha: str) -> None:
        """
        Setter para definir uma nova senha (privada).
        """
        self.__senha = nova_senha

    def __repr__(self) -> str:
        """
        Representação da classe PessoaFisica.
        """
        return f"PessoaFisica(nome={self.nome}, cpf={self.cpf}, data_nascimento={self.data_nascimento}, endereco={self.endereco})"

    def ler_clientes_arquivo(self) -> List[dict]:
        """
        Lê os clientes de um arquivo e retorna uma lista de dicionários com os dados dos clientes.
        Retorna uma lista vazia se o arquivo não for encontrado ou ocorrer um erro.
        """
        clientes = []
        try:
            with open(clientes_arquivotxt, 'r') as file:
                for linha in file:
                    partes = linha.strip().split('|')
                    cliente = {}
                    for parte in partes:
                        if ':' in parte:
                            chave, valor = parte.split(':', 1)
                            cliente[chave] = valor
                    clientes.append(cliente)
        except FileNotFoundError:
            print(Fore.RED + f"Arquivo {clientes_arquivotxt} não encontrado.")
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro: {e}")
        return clientes

    def filtrar_cliente(self, cpf_informado: str) -> dict:
        """
        Filtra os clientes pelo CPF informado.
        Retorna um dicionário com os dados do cliente se encontrado, ou None se não encontrado.
        """
        if not self.clientes:
            self.clientes = self.ler_clientes_arquivo()

        for cliente in self.clientes:
            if cliente.get('cpf') == cpf_informado:
                return cliente

        return None

    def criar_cliente(self) -> None:
        """
        Cria um novo cliente com base em informações fornecidas pelo usuário e salva no arquivo de clientes.
        """
        while True:
            cpf = input("Informe o CPF (somente números): ")
            if not cpf.isdigit() or len(cpf) != 11:
                print(Fore.RED + "\n❌❌❌ CPF inválido ❌❌❌")
                print(Style.RESET_ALL)
                continue

            cliente = self.filtrar_cliente(cpf)
            if cliente:
                print(Fore.YELLOW + "\n❗❗❗ Já existe cliente com esse CPF! ❗❗❗")
                print(Style.RESET_ALL)
                return
            break

        while True:
            nome = input("Informe o nome completo: ")
            if all(x.isalpha() or x.isspace() for x in nome):  # Permite espaços no nome
                break
            else:
                print("\n❌❌❌ Nome inválido! Informe apenas letras. ❌❌❌")
                print(Style.RESET_ALL)

        while True:
            data_nascimento = input(
                "Informe a data de nascimento (dd/mm/aaaa): ")
            try:
                data_nascimento_dt = datetime.strptime(
                    data_nascimento, "%d/%m/%Y")
                break
            except ValueError:
                print(
                    Fore.RED + "\n❌❌❌ Formato de data inválido! Por favor, digite no formato dd/mm/aaaa. ❌❌❌")
                print(Style.RESET_ALL)

        endereco = input(
            "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        data_nascimento_formatada = data_nascimento_dt.strftime("%d-%m-%Y")
        senha = input("Informe sua senha: ")
        saldo = 0

        cliente = PessoaFisica(
            nome=nome, data_nascimento=data_nascimento_formatada, cpf=cpf, endereco=endereco, senha=senha
        )

        # Registra o cliente no arquivo de clientes
        with open("log.txt", "a") as file:
            file.write(f"Cliente criado: {nome} | CPF: {
                       cpf} | ({datetime.now().strftime('%d-%m-%Y %H:%M:%S')})\n")
        with open(clientes_arquivotxt, "a") as file:
            file.write(f"nome:{cliente.nome}|cpf:{cpf}|endereco:{
                       endereco}|senha:{cliente.senha}|saldo:{saldo}\n")

        print(Fore.GREEN + f"\n✅✅✅ Cliente criado com sucesso! {
              datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ✅✅✅")
        print(Style.RESET_ALL)

    def criar_conta(self) -> None:
        """
        Cria uma nova conta para um cliente existente, gerando um número aleatório para a conta.
        """
        while True:
            cpf = input("Informe o CPF (somente números): ")
            if not cpf.isdigit() or len(cpf) != 11:
                print(Fore.RED + "\n❌❌❌ CPF inválido ❌❌❌")
                print(Style.RESET_ALL)
            else:
                cliente = self.filtrar_cliente(cpf)
                if not cliente:
                    print(Fore.YELLOW + "\n❗❗❗ Não existe cliente com esse CPF! ❗❗❗")
                    print(Style.RESET_ALL)
                    return
                break

        while True:
            senha = input("Informe sua senha: ")
            if cliente.get('senha') != senha:
                print(Fore.RED + "\n❌❌❌ Senha incorreta ❌❌❌")
                print(Style.RESET_ALL)
                return
            break

        numero = random.randint(10000000, 99999999)
        # Tipo: Conta (supondo que Conta seja uma classe definida em models.conta)
        conta = Conta(numero=numero)

        # Registra a criação da conta no arquivo de contas
        with open("log.txt", "a") as file:
            file.write(f"Conta criada: Conta: {numero}|cpf: {
                       cpf}| ({datetime.now().strftime('%d-%m-%Y %H:%M:%S')})\n")
        with open(contas_arquivotxt, "a") as file:
            file.write(f"conta:{conta.numero}|cpf:{cpf}\n")

        print(Fore.GREEN + f"\n✅✅✅ Conta criada com sucesso! {
              datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ✅✅✅")
        print(Style.RESET_ALL)

    def sacar(self) -> None:
        """
        Realiza um saque na conta de um cliente, atualizando o saldo tanto em memória quanto no arquivo.
        """
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
            print(Style.RESET_ALL)
            return

        # Tipo: float (supondo que saldo seja um valor numérico em string)
        saldo = float(cliente.get('saldo', 0))
        valor = float(input("Informe o valor do saque: "))  # Tipo: float

        if valor < 0:
            print(Fore.RED + "\n❌❌❌ Valor Inválido! ❌❌❌")
            print(Style.RESET_ALL)
        elif valor > saldo:
            print(Fore.RED + "\n❌❌❌ Saldo insuficiente! ❌❌❌")
            print(Style.RESET_ALL)
        else:
            saldo -= valor
            # Atualiza o saldo no dicionário do cliente
            cliente['saldo'] = str(saldo)

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

            # Registra a transação no arquivo de log
            with open("log.txt", "a") as file:
                file.write(f"Transacao Realizada: cpf: {cpf}|saldo: {
                           saldo} ({datetime.now().strftime('%d-%m-%Y %H:%M:%S')})\n")

            print(Fore.GREEN + f"\n✅✅✅ Saque realizado com sucesso! {
                  datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ✅✅✅")
            print(Style.RESET_ALL)

    def deposito(self) -> None:
        """
        Realiza um depósito na conta de um cliente, atualizando o saldo tanto em memória quanto no arquivo.
        """
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
            print(Style.RESET_ALL)
            return

        valor = float(input("Informe o valor do depósito: "))  # Tipo: float

        if valor < 0:
            print(Fore.RED + "\n❌❌❌ Valor Inválido! ❌❌❌")
            print(Style.RESET_ALL)
        else:
            saldo = float(cliente.get('saldo', 0))  # Tipo: float
            saldo += valor
            # Atualiza o saldo no dicionário do cliente
            cliente['saldo'] = str(saldo)

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

            # Registra a transação no arquivo de log
            with open("log.txt", "a") as file:
                file.write(f"Depósito Realizado: cpf: {cpf}|saldo: {
                           saldo} ({datetime.now().strftime('%d-%m-%Y %H:%M:%S')})\n")

            print(Fore.GREEN + f"\n✅✅✅ Depósito realizado com sucesso! {
                  datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ✅✅✅")
            print(Style.RESET_ALL)

    # Método exibir_extrato comentado pois está incompleto e não utilizado no script principal
    # def exibir_extrato(self, conta: ContaCorrente) -> None:
    #     ...

# Código de teste comentado pois foi movido para um arquivo separado ou não utilizado
# if __name__ == "__main__":
#     ...
