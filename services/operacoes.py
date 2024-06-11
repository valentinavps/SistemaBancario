from models.transacao import Deposito, Saque
from models.conta_corrente import ContaCorrente
from models.pessoa_fisica import PessoaFisica
from utils.helpers import filtrar_cliente, recuperar_conta_cliente
from datetime import datetime
from colorama import Fore, Style

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
        print(Style.RESET_ALL)  # Resetando a cor
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
        print(Style.RESET_ALL)  # Resetando a cor
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
        print(Style.RESET_ALL)  # Resetando a cor
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print(Fore.CYAN + "\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            tipo_transacao = transacao["tipo"]
            texto_formatado = f"\n{tipo_transacao} ({transacao['data']}):\n\tR$ {transacao['valor']:.2f}\n"

            if tipo_transacao == "Saque":
                texto_formatado = f"{Fore.RED}{texto_formatado}{Style.RESET_ALL}"
            elif tipo_transacao == "Deposito":
                texto_formatado = f"{Fore.YELLOW}{texto_formatado}{Style.RESET_ALL}"

            extrato += texto_formatado

    print(extrato)
    print(f"\n{Fore.CYAN}Saldo:\n\tR$ {conta.saldo:.2f}{Style.RESET_ALL}")
    print(Fore.CYAN + "==========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print(Fore.YELLOW + "\n❗❗❗ Já existe cliente com esse CPF! ❗❗❗")
        print(Style.RESET_ALL)  # Resetando a cor
        return

    nome = input("Informe o nome completo: ")

    while True:
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
        try:
            data_nascimento_dt = datetime.strptime(data_nascimento, "%d/%m/%Y")
            break
        except ValueError:
            print(Fore.RED + "\n❌❌❌ Formato de data inválido! Por favor, digite no formato dd/mm/aaaa. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor

    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    data_nascimento_formatada = data_nascimento_dt.strftime("%d-%m-%Y")

    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento_formatada, cpf=cpf, endereco=endereco
    )

    clientes.append(cliente)

    data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open("log.txt", "a") as file:
        file.write(f"Cliente criado: {nome} | CPF: {cpf} | ({data_hora})\n")

    print(Fore.GREEN + f"\n✅✅✅ Cliente criado com sucesso! {data_hora} ✅✅✅")
    print(Style.RESET_ALL)  # Resetando a cor

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

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

    print(Fore.GREEN + f"\n✅✅✅ Conta criada com sucesso! {data_hora} ✅✅✅")
    print(Style.RESET_ALL)  # Resetando a cor

def listar_contas(contas):
    for conta in contas:
        print(Fore.CYAN + "=" * 100)
        print(Fore.YELLOW + str(conta) + Style.RESET_ALL)
