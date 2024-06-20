from colorama import Fore, Style 
from typing import List  
from models.conta import Conta  
from datetime import datetime  
from utils.helpers import recuperar_conta_cliente  
import random  

# Define os caminhos dos arquivos de clientes, contas e transações
clientes_arquivotxt = "/home/valentinavps/POO/SistemaBancario/clientes.txt"
contas_arquivotxt = "/home/valentinavps/POO/SistemaBancario/contas.txt"


# Define a classe PessoaFisica
class PessoaFisica:
    def __init__(self, nome, data_nascimento, cpf, endereco, senha):
        self.endereco = endereco  # Atributo endereço da pessoa física
        self.nome = nome  # Atributo nome da pessoa física
        self.cpf = cpf  # Atributo CPF da pessoa física
        self.data_nascimento = data_nascimento  # Atributo data de nascimento da pessoa física
        self.__senha = senha  # Atributo senha privada da pessoa física (privado)
        self.clientes = []  # Inicializa uma lista vazia de clientes

    @property
    def senha(self):
        return self.__senha  # Retorna a senha privada da pessoa física
    
    @senha.setter
    def senha(self, nova_senha):
        self.__senha = nova_senha  # Altera a senha privada da pessoa física

    def __repr__(self):
        return f"PessoaFisica(nome={self.nome}, cpf={self.cpf}, data_nascimento={self.data_nascimento}, endereco={self.endereco})"
    
    # Lê os clientes do arquivo de texto
    def ler_clientes_arquivo(self):
        clientes = []  # Lista para armazenar os clientes lidos do arquivo
        try:
            # Abre o arquivo de clientes em modo leitura
            with open(clientes_arquivotxt, 'r') as file:
                for linha in file:
                    partes = linha.strip().split('|')  # Divide a linha em partes separadas por '|'
                    cliente = {}  # Dicionário para armazenar os dados do cliente
                    for parte in partes:
                        if ':' in parte:
                            chave, valor = parte.split(':', 1)  # Divide a parte em chave e valor
                            cliente[chave] = valor  # Adiciona chave e valor ao dicionário do cliente
                    clientes.append(cliente)  # Adiciona o cliente à lista de clientes
        except FileNotFoundError:
            print(Fore.RED + f"Arquivo {clientes_arquivotxt} não encontrado.")  # Exibe mensagem se o arquivo não for encontrado
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro: {e}")  # Exibe mensagem se ocorrer um erro inesperado
        return clientes  # Retorna a lista de clientes lidos do arquivo
       
    # Filtra os clientes pelo CPF informado
    def filtrar_cliente(self, cpf_informado: str):
        if not self.clientes:  # Se a lista de clientes estiver vazia
            self.clientes = self.ler_clientes_arquivo()  # Lê os clientes do arquivo

        for cliente in self.clientes:
            if cliente.get('cpf') == cpf_informado:
                return cliente  # Retorna o cliente se encontrar o CPF informado
        
        return None  # Retorna None se não encontrar nenhum cliente com o CPF informado
    
    # Autentica o cliente pelo CPF e senha informados
    def autenticacao(self, cpf_informado, senha_informada: str):
        if not self.clientes:  # Se a lista de clientes estiver vazia
            self.clientes = self.ler_clientes_arquivo()  # Lê os clientes do arquivo

        for cliente in self.clientes:
            if cliente.get('cpf') == cpf_informado and cliente.get('senha') == senha_informada:
                return cliente  # Retorna o cliente se encontrar o CPF e senha informados
        
        return None  # Retorna None se não encontrar nenhum cliente com o CPF e senha informados

    # Cria um novo cliente
    def criar_cliente(self):
        while True:
            cpf = input("Informe o CPF (somente números): ")
            if not cpf.isdigit() or len(cpf) != 11:
                print(Fore.RED + "\n❌❌❌ CPF inválido ❌❌❌")
                print(Style.RESET_ALL)
                continue

            cliente = self.filtrar_cliente(cpf)  # Verifica se já existe cliente com o CPF informado
            if cliente:
                print(Fore.YELLOW + "\n❗❗❗ Já existe cliente com esse CPF! ❗❗❗")
                print(Style.RESET_ALL)
                return
            break

        while True:
            nome = input("Informe o nome completo: ")
            if all(x.isalpha() or x.isspace() for x in nome):  # Verifica se o nome contém apenas letras ou espaços
                break
            else:
                print("\n❌❌❌ Nome inválido! Informe apenas letras. ❌❌❌")
                print(Style.RESET_ALL)

        while True:
            data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
            try:
                data_nascimento_dt = datetime.strptime(data_nascimento, "%d/%m/%Y")
                break
            except ValueError:
                print(Fore.RED + "\n❌❌❌ Formato de data inválido! Por favor, digite no formato dd/mm/aaaa. ❌❌❌")
                print(Style.RESET_ALL)

        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        data_nascimento_formatada = data_nascimento_dt.strftime("%d-%m-%Y")
        senha = input("Informe sua senha: ")
        saldo = 0

        # Cria um novo objeto PessoaFisica
        cliente = PessoaFisica(
            nome=nome, data_nascimento=data_nascimento_formatada, cpf=cpf, endereco=endereco, senha=senha
        )

        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # Escreve no arquivo de log
        with open("log.txt", "a") as file:
            file.write(f"Cliente criado: {nome} | CPF: {cpf} | ({data_hora})\n")
        # Escreve no arquivo de clientes
        with open(clientes_arquivotxt, "a") as file:
            file.write(f"cpf:{cpf}|nome:{cliente.nome}|cpf:{cpf}|endereco:{endereco}|senha:{cliente.senha}|saldo:{saldo} \n")

        print(Fore.GREEN + f"\n✅✅✅ Cliente criado com sucesso! {data_hora} ✅✅✅")
        print(Style.RESET_ALL)

        return cliente  # Retorna o objeto cliente criado

    # Cria uma nova conta
    def criar_conta(self) -> None:
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

        numero = random.randint(10000000, 99999999)  # Gera um número de conta aleatório
        conta = Conta(numero=numero)

        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # Escreve no arquivo de log
        with open("log.txt", "a") as file:
            file.write(f"Conta criada: Conta: {numero}|cpf: {cpf}| ({data_hora})\n")
        # Escreve no arquivo de contas
        with open(contas_arquivotxt, "a") as file:
            file.write(f"conta:{conta.numero}|cpf:{cpf}\n")

        print(Fore.GREEN + f"\n✅✅✅ Conta criada com sucesso! {data_hora} ✅✅✅")
        print(Style.RESET_ALL)

