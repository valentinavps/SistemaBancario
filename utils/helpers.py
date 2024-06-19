from colorama import Fore, Style

# Caminhos dos arquivos de clientes e contas
clientes_arquivotxt: str = "/home/valentinavps/POO/SistemaBancario/clientes.txt"
contas_arquivo: str = "/home/valentinavps/POO/SistemaBancario/contas.txt"

# Classe Helpers para manipulação de clientes


class Helpers:
    def __init__(self, clientes_arquivo: str) -> None:
        """
        Inicializa um objeto Helpers com o caminho do arquivo de clientes.

        Args:
        - clientes_arquivo (str): Caminho do arquivo de clientes.
        """
        self.clientes_arquivo: str = clientes_arquivo
        self.clientes: list = self.ler_clientes_arquivo()

    def ler_clientes_arquivo(self) -> list:
        """
        Lê os clientes do arquivo e os armazena em uma lista de dicionários.

        Returns:
        - list: Lista de dicionários contendo os dados dos clientes.
        """
        clientes: list = []
        try:
            with open(self.clientes_arquivo, 'r') as file:
                for linha in file:
                    partes: list = linha.strip().split('|')
                    cliente: dict = {}
                    for parte in partes:
                        chave, valor = parte.split(':')
                        cliente[chave] = valor
                    clientes.append(cliente)
        except FileNotFoundError:
            print(f"Arquivo {self.clientes_arquivo} não encontrado.")
        return clientes

    def filtrar_cliente(self, cpf_informado: str) -> bool:
        """
        Filtra os clientes pelo CPF informado.

        Args:
        - cpf_informado (str): CPF do cliente a ser filtrado.

        Returns:
        - bool: True se o cliente for encontrado, False caso contrário.
        """
        for cliente in self.clientes:
            if cliente.get('cpf') == cpf_informado:
                return True
        return False

# Função comentada para recuperar a conta do cliente
# def recuperar_conta_cliente(cliente):
#     if not cliente.contas:
#         print(Fore.YELLOW + "\n❗❗❗ Cliente não possui conta! ❗❗❗")
#         print(Style.RESET_ALL)  # Resetando a cor
#         return
#     return cliente.contas[0]  # FIXME: não permite cliente escolher a conta
