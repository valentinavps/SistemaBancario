from colorama import Fore, Style


clientes_arquivotxt = "/home/valentinavps/POO/SistemaBancario/clientes.txt"
contas_arquivo = "/home/valentinavps/POO/SistemaBancario/contas.txt"


class Helpers ():
    def __init__(self, clientes_arquivo):
        self.clientes_arquivo = clientes_arquivo
        self.clientes = self.ler_clientes_arquivo()

    def ler_clientes_arquivo(self):
        clientes =[]
        try:
           with open(self.clientes_arquivo, 'r') as file:
                for linha in file:
                    partes = linha.strip().split('|')
                    cliente = {}
                    for parte in partes:
                        chave, valor = parte.split(':')
                        cliente[chave] = valor
                    clientes.append(cliente)
        except FileNotFoundError:
            print(f"Arquivo {self.clientes_arquivo} não encontrado.")
        return clientes
 
    
 
    def filtrar_cliente(self, cpf_informado):
        for cliente in self.clientes:
            if cliente.get('cpf') == cpf_informado:
                return True
            else:
                return False



# def recuperar_conta_cliente(cliente):
#     if not cliente.contas:
#         print(Fore.YELLOW + "\n❗❗❗ Cliente não possui conta! ❗❗❗")
#         print(Style.RESET_ALL)  # Resetando a cor
#         return
#     return cliente.contas[0]  # FIXME: não permite cliente escolher a conta



