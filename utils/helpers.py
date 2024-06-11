from colorama import Fore, Style

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print(Fore.YELLOW + "\n❗❗❗ Cliente não possui conta! ❗❗❗")
        print(Style.RESET_ALL)  # Resetando a cor
        return
    return cliente.contas[0]  # FIXME: não permite cliente escolher a conta
