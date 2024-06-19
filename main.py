from colorama import Fore, Style
from utils.menu import menu
from models.operacoes import Operacoes
import logging
from utils.helpers import ler_clientes_arquivo, filtrar_cliente_txt

# Configurações do logger para escrever em um arquivo .txt
logging.basicConfig(
    filename="/home/valentinavps/POO/SistemaBancario/log.txt",  # Nome do arquivo de log
    filemode="a",  # Modo de abertura do arquivo (append)
    level=logging.INFO,  # Nível de log (informação)
    format="%(asctime)s - %(message)s",  # Formato das mensagens de log
    datefmt="%d-%m-%Y %H:%M:%S",  # Formato da data e hora
)


def main() -> None:

    clientes: list = []  # Lista para armazenar clientes
    contas: list = []  # Lista para armazenar contas

    while True:
        opcao: str = menu()  # Exibe o menu e obtém a opção escolhida pelo usuário

        # if opcao == "d":
        #     Operacoes.depositar(clientes)  # Chama a função para realizar um depósito
        if opcao == "s":
            Operacoes.sacar(clientes)  # Chama a função para realizar um saque
        elif opcao == "e":
            Operacoes.exibir_extrato(clientes)  # Chama a função para exibir o extrato
        elif opcao == "nu":
            # Chama a função para criar um novo cliente
            Operacoes.criar_cliente()
        elif opcao == "nc":
            # Define o número da nova conta
            numero_conta: int = len(contas) + 1
            # Chama a função para criar uma nova conta
            Operacoes.criar_conta(numero_conta, clientes, contas)
        # elif opcao == "lc":
        #     Operacoes.listar_contas(contas)  # Chama a função para listar todas as contas
        elif opcao == "q":
            break  # Sai do loop e encerra o programa
        else:
            print(
                Fore.RED + "\n❌❌❌ Operação inválida, por favor selecione novamente a operação desejada. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor


if __name__ == "__main__":
    main()  # Executa a função principal
