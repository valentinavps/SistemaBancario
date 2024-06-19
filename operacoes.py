
from models.pessoa_fisica import PessoaFisica

from utils.helpers import Helpers
from datetime import datetime
from colorama import Fore, Style
from abc import ABC, abstractmethod

contas_arquivo = "/home/valentinavps/POO/SistemaBancario/contas.txt"
clientes_arquivotxt = "/home/valentinavps/POO/SistemaBancario/clientes.txt"



class Operacoes(ABC):
    def __init__(self, lista_clientes, cpf):
        self.lista_clientes = lista_clientes
        self.cpf = cpf

    @abstractmethod
    def operacao(self):
        pass



# class Deposito(Operacoes):

#     def operacao(lista_clientes):
#         cpf = input("Informe o CPF do cliente: ")
#         cliente = Helpers.filtrar_cliente(cpf, clientestxt)

#         if not cliente:
#             print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
#             print(Style.RESET_ALL)  # Resetando a cor
#             return

#         valor = float(input("Informe o valor do depósito: "))
#         transacao = Deposito(valor)

#         conta = recuperar_conta_cliente(cliente)
#         if not conta:
#             return

#         cliente.realizar_transacao(conta, transacao)

class CriarCliente:
    
    def __init__(self, clientes_arquivo):
        self.clientes_arquivotxt = clientes_arquivo
        
    def criar_cliente(self):
        while True:
            cpf_informado = input("Informe o CPF (somente números): ")
            # Verifica se o CPF contém apenas números e tem exatamente 11 dígitos
            if not cpf_informado.isdigit() or len(cpf_informado) != 11:
                print(Fore.RED + "\n❌❌❌ CPF inválido ❌❌❌")
                continue
            
            cliente = Helpers.filtrar_cliente(cpf_informado)

            if cliente:
                print(Fore.YELLOW + "\n❗❗❗ Já existe cliente com esse CPF! ❗❗❗")
                return
            break

        while True:
            nome = input("Informe o nome completo: ")
            if nome.isalpha():
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
            nome=nome, data_nascimento=data_nascimento_formatada, cpf=cpf_informado, endereco=endereco, senha=senha
        )
       

        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open("log.txt", "a") as file:
            file.write(f"Cliente criado: {nome} | CPF: {cpf_informado} | ({data_hora})\n")
        with open(clientes_arquivotxt, "a") as file:
            file.write(f"nome:{cliente.nome}|cpf:{cpf_informado}|senha:{cliente.senha} \n")

        print(Fore.GREEN + f"\n✅✅✅ Cliente criado com sucesso! {data_hora} ✅✅✅")



# def criar_conta(numero_conta, clientestxt, contas):
#     cpf = input("Informe o CPF do cliente: ")
#     cliente = filtrar_cliente_txt(cpf, clientestxt)

#     if not cliente:
#         print(Fore.RED + "\n❌❌❌ Cliente não encontrado, fluxo de criação de conta encerrado! ❌❌❌")
#         print(Style.RESET_ALL)  # Resetando a cor
#         return

#     conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
#     contas.append(conta)
#     cliente.contas.append(conta)

#     data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
#     with open("log.txt", "a") as file:
#         file.write(f"Nova conta criada para o cliente {cliente.nome} | Conta: {numero_conta} | ({data_hora})\n")
#     with open(contas_arquivo, "a") as file:
#         file.write(f"Cliente: {cliente.nome}| Conta: {numero_conta} \n")

#     print(Fore.GREEN + f"\n✅✅✅ Conta criada com sucesso! {data_hora} ✅✅✅")
#     print(Style.RESET_ALL)  # Resetando a cor


# def sacar(clientestxt):
#     cpf = input("Informe o CPF do cliente: ")
#     cliente = filtrar_cliente_txt(cpf, clientestxt)

#     if not cliente:
#         print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
#         print(Style.RESET_ALL)  # Resetando a cor
#         return

#     valor = float(input("Informe o valor do saque: "))
#     transacao = Saque(valor)

#     conta = recuperar_conta_cliente(cliente)
#     if not conta:
#         return

#     cliente.realizar_transacao(conta, transacao)

# def exibir_extrato(clientestxt):
#     cpf = input("Informe o CPF do cliente: ")
#     cliente = filtrar_cliente_txt(cpf, clientestxt)

#     if not cliente:
#         print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
#         print(Style.RESET_ALL)  # Resetando a cor
#         return

#     conta = recuperar_conta_cliente(cliente)
#     if not conta:
#         return

#     print(Fore.CYAN + "\n================ EXTRATO ================")
#     transacoes = conta.historico.transacoes

#     extrato = ""
#     if not transacoes:
#         extrato = "Não foram realizadas movimentações."
#     else:
#         for transacao in transacoes:
#             tipo_transacao = transacao["tipo"]
#             texto_formatado = f"\n{tipo_transacao} ({transacao['data']}):\n\tR$ {transacao['valor']:.2f}\n"

#             if tipo_transacao == "Saque":
#                 texto_formatado = f"{Fore.RED}{texto_formatado}{Style.RESET_ALL}"
#             elif tipo_transacao == "Deposito":
#                 texto_formatado = f"{Fore.YELLOW}{texto_formatado}{Style.RESET_ALL}"

#             extrato += texto_formatado

#     print(extrato)
#     print(f"\n{Fore.CYAN}Saldo:\n\tR$ {conta.saldo:.2f}{Style.RESET_ALL}")
#     print(Fore.CYAN + "==========================================")

# def listar_contas(contas):
#     for conta in contas:
#         print(Fore.CYAN + "=" * 100)
#         print(Fore.YELLOW + str(conta) + Style.RESET_ALL)

cliente = CriarCliente()