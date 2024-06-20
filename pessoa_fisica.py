from colorama import Fore, Style
from typing import List
from models.conta import Conta
from datetime import datetime
import random

clientes_arquivotxt = "/home/valentinavps/POO/SistemaBancario/clientes.txt"
contas_arquivotxt = "/home/valentinavps/POO/SistemaBancario/contas.txt"

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
    
     # Lê os clientes do arquivo e os armazena em uma lista de dicionários.
    def ler_clientes_arquivo(self):
        clientes = []
        try:
            with open(clientes_arquivotxt, 'r') as file:
                for linha in file:
                    partes = linha.strip().split('|')
                    cliente = {}
                    for parte in partes:
                        chave, valor = parte.split(':')
                        cliente[chave] = valor
                    clientes.append(cliente)
        except FileNotFoundError:
            print(Fore.RED + f"Arquivo {clientes_arquivotxt} não encontrado.")
        return clientes
       

    # Filtra os clientes pelo CPF informado.
    def filtrar_cliente(self, cpf_informado: str) -> bool:
        if not self.clientes:
            self.ler_clientes_arquivo()
        
        for cliente in self.clientes:
            if cliente.get('cpf') == cpf_informado:
                return True  # Se encontrar o cliente com o CPF informado, retorna True
        
        return False  # Se não encontrar nenhum cliente com o CPF informado, retorna False

    def criar_cliente(self):
        while True:
            cpf = input("Informe o CPF (somente números): ")
            if not cpf.isdigit() or len(cpf) != 11:
                print(Fore.RED + "\n❌❌❌ CPF inválido ❌❌❌")
                continue

            cliente = self.filtrar_cliente(cpf)
            if cliente:
                print(Fore.YELLOW + "\n❗❗❗ Já existe cliente com esse CPF! ❗❗❗")
                return
            break

        while True:
            nome = input("Informe o nome completo: ")
            if all(x.isalpha() or x.isspace() for x in nome):  # Allows spaces in the name
                break
            else:
                print("\n❌❌❌ Nome inválido! Informe apenas letras. ❌❌❌")

        while True:
            data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
            try:
                data_nascimento_dt = datetime.strptime(data_nascimento, "%d/%m/%Y")
                break
            except ValueError:
                print(Fore.RED + "\n❌❌❌ Formato de data inválido! Por favor, digite no formato dd/mm/aaaa. ❌❌❌")

        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        data_nascimento_formatada = data_nascimento_dt.strftime("%d-%m-%Y")
        senha = input("Informe sua senha: ")

        cliente = PessoaFisica(
            nome=nome, data_nascimento=data_nascimento_formatada, cpf=cpf, endereco=endereco, senha=senha
        )

        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open("log.txt", "a") as file:
            file.write(f"Cliente criado: {nome} | CPF: {cpf} | ({data_hora})\n")
        with open(clientes_arquivotxt, "a") as file:
            file.write(f"nome:{cliente.nome}|cpf:{cpf}|endereco:{endereco}|senha:{cliente.senha} \n")

        print(Fore.GREEN + f"\n✅✅✅ Cliente criado com sucesso! {data_hora} ✅✅✅")

        return cliente


    def criar_conta(self) -> None:
        # while True:
        cpf= input("Informe o CPF (somente números): ")
        if not cpf.isdigit() or len(cpf) != 11:
            print(Fore.RED + "\n❌❌❌ CPF inválido ❌❌❌")
        # else:
        #     cliente = self.filtrar_cliente(cpf)
        #     print(self.filtrar_cliente(cpf))
            # if not cliente:
            #     print(Fore.YELLOW + "\n❗❗❗ Nao existe cliente com esse CPF! ❗❗❗")
            #     return
            # break

        # while True:
        #     senha = input("Informe sua senha: ")
        #     autenticacao = self.filtrar_cliente(senha)
        #     if not autenticacao:
        #         print(Fore.RED + "\n❌❌❌ Senha incorreta ❌❌❌")
        #         return
        #     break
        
        numero =  random.randint(10000000, 99999999)
        conta = Conta(numero=numero)

        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open("log.txt", "a") as file:
            file.write(f"Conta criada: Conta: {numero}|cpf: {cpf}| ({data_hora})\n")
        with open(contas_arquivotxt, "a") as file:
            file.write(f"conta:{conta.numero}|cpf:{cpf}")

        print(Fore.GREEN + f"\n✅✅✅ Conta criada com sucesso! {data_hora} ✅✅✅")


if __name__ == "__main__":
    # # Criando uma instância da classe PessoaFisica
    pessoa = PessoaFisica(nome="Vava", data_nascimento="20/08/2002", cpf="88888888888", endereco="lala", senha="123")

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

      # Testando o método criar_conta()
    print("\nTestando criar_conta():")
    pessoa.criar_conta()



