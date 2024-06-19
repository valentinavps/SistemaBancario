from datetime import datetime
from colorama import Fore, Style
from models.conta_corrente import ContaCorrente

from utils.helpers import filtrar_cliente, recuperar_conta_cliente, filtrar_cliente_txt

clientes_arquivo = "/home/valentinavps/POO/SistemaBancario/clientes.txt"
contas_arquivo = "/home/valentinavps/POO/SistemaBancario/contas.txt"

class PessoaFisica:
    def __init__(self, nome, data_nascimento, cpf, endereco, senha):
        self.endereco = endereco
        self.nome = nome
        self.cpf = cpf
        self.__senha =senha

        while True:
            try:
                data_nascimento_dt = datetime.strptime(data_nascimento, "%d-%m-%Y")
                data_atual = datetime.now()
                if data_nascimento_dt > data_atual:
                    raise ValueError("❌ Data de nascimento não pode ser maior que a data atual. ❌")
                else:
                    self.data_nascimento = data_nascimento
                    break
            except ValueError as e:
                print(e)
                data_nascimento = input("Informe uma nova data de nascimento (dd-mm-aaaa): ")
    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, nova_senha):
        self.__senha = nova_senha

    def criar_cliente(clientestxt, clientes_arquivo="clientes.txt"):
        while True:
            cpf = input("Informe o CPF (somente números): ")
            # Verifica se o CPF contém apenas números e tem exatamente 11 dígitos
            if not cpf.isdigit() or len(cpf) != 11:
                print(Fore.RED + "\n❌❌❌ CPF inválido ❌❌❌")
                continue
            
            cliente = filtrar_cliente_txt(cpf, clientestxt)

            if cliente:
                print(Fore.YELLOW + "\n❗❗❗ Já existe cliente com esse CPF! ❗❗❗")
                return
            break

        nome = input("Informe o nome completo: ")

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
        clientestxt.append(cliente)

        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open("log.txt", "a") as file:
            file.write(f"Cliente criado: {nome} | CPF: {cpf} | ({data_hora})\n")
        with open(clientes_arquivo, "a") as file:
            file.write(f"nome:{cliente.nome}|cpf:{cpf}|senha:{cliente.senha} \n")

        print(Fore.GREEN + f"\n✅✅✅ Cliente criado com sucesso! {data_hora} ✅✅✅")

    def criar_conta(numero_conta, clientestxt, contas):
        cpf = input("Informe o CPF do cliente: ")
        cliente = filtrar_cliente_txt(cpf, clientestxt)

        if not cliente:
            print(Fore.RED + "\n❌❌❌ Cliente não encontrado, fluxo de criação de conta encerrado! ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return

        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.contas.append(conta)

        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open("log.txt", "a") as file:
            file.write(f"Nova conta criada para o cliente {cliente.nome} | Conta: {numero_conta} | ({data_hora})\n")
        with open(contas_arquivo, "a") as file:
            file.write(f"Cliente: {cliente.nome}| Conta: {numero_conta} \n")

        print(Fore.GREEN + f"\n✅✅✅ Conta criada com sucesso! {data_hora} ✅✅✅")
        print(Style.RESET_ALL)  # Resetando a cor

    def __repr__(self):
        return f"PessoaFisica(nome={self.nome}, cpf={self.cpf}, data_nascimento={self.data_nascimento}, endereco={self.endereco})"
