from colorama import Fore, Style
from typing import List
from models.conta import Conta
# from models.conta_corrente import ContaCorrente
from datetime import datetime
from utils.helpers import recuperar_conta_cliente
import random

# Define os caminhos dos arquivos de clientes, contas e transações
clientes_arquivotxt = "/home/valentinavps/POO/SistemaBancario/clientes.txt"
contas_arquivotxt = "/home/valentinavps/POO/SistemaBancario/contas.txt"


# Define a classe PessoaFisica
class PessoaFisica:
    def __init__(self, nome, data_nascimento, cpf, endereco, senha):
        self.endereco = endereco
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.__senha = senha
        self.clientes = []

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, nova_senha):
        self.__senha = nova_senha

    def __repr__(self):
        return f"PessoaFisica(nome={self.nome}, cpf={self.cpf}, data_nascimento={self.data_nascimento}, endereco={self.endereco})"
    
    # Lê os clientes do arquivo de texto
    def ler_clientes_arquivo(self):
        clientes = []
        try:
            # Abre o arquivo de clientes em modo leitura
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
       
    # Filtra os clientes pelo CPF informado
    def filtrar_cliente(self, cpf_informado: str):
        if not self.clientes:
            self.clientes = self.ler_clientes_arquivo()
        
        for cliente in self.clientes:
            if cliente.get('cpf') == cpf_informado:
                return cliente  # Retorna o cliente se encontrar o CPF informado
        
        return None  # Retorna None se não encontrar nenhum cliente com o CPF informado
    
    def autenticacao(self, cpf_informado,senha_informada: str):
        if not self.clientes:
            self.clientes = self.ler_clientes_arquivo()
        
        for cliente in self.clientes:
            if cliente.get('cpf') == cpf_informado and cliente.get('senha') == senha_informada:
                return cliente  # Retorna o cliente se encontrar o CPF informado
        
        return None  # Retorna None se não encontrar nenhum cliente com o CPF informado

    # Cria um novo cliente
    def criar_cliente(self):
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

        return cliente

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

    #Mostra oextrato da conta do Cliente
    def exibir_extrato(self) -> None:
        cpf = input("Informe o CPF do cliente: ")
        cliente =self.filtrar_cliente(cpf)

        if not cliente:
            print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
            print(Style.RESET_ALL)
            return
        
        senha = input("Informe sua senha: ")
        autenticacao = self.autenticacao(cpf, senha)

        if not autenticacao:
            print(Fore.RED + "\n❌❌❌ Senha Incorreta! ❌❌❌")
            print(Style.RESET_ALL)
            return
        
        saldo_extrato = cliente['saldo']
        
        print(f"{Fore.BLUE}EXTRATO BANCÁRIO")
        print(Style.RESET_ALL)
        print(f"Cliente: {self.nome}")
        print(f"Saldo atual: R$ {saldo_extrato}")
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        
# if __name__ == "__main__":
#     # Criando uma instância da classe PessoaFisica
#     pessoa = PessoaFisica(nome="Vava", data_nascimento="20/08/2002", cpf="88888888888", endereco="lala", senha="123")

    # # Testando o método ler_clientes_arquivo()
    # print("\nTestando ler_clientes_arquivo():")
    # clientes = pessoa.ler_clientes_arquivo()
    # print(clientes)

    # # Testando o método filtrar_cliente()
    # print("\nTestando filtrar_cliente():")
    # cpf_teste = "88888888888"  # Substitua pelo CPF que você quer testar
    # cliente_filtrado = pessoa.filtrar_cliente(cpf_teste)
    # print(cliente_filtrado)

    # # Testando o método criar_cliente()
    # print("\nTestando criar_cliente():")
    # pessoa.criar_cliente()

    # # Testando o método criar_conta()
    # print("\nTestando criar_conta():")
    # pessoa.criar_conta()

    #  # Testando o método deposito()
    # print("\nTestando deposito():")
    # pessoa.deposito()


    # # Testando o método saque()
    # print("\nTestando saque():")
    # pessoa.sacar()




