from utils.menu import menu
from models.pessoa_fisica import PessoaFisica
from models.transacao import Saque, Deposito
from colorama import Fore, Style
import logging

# Configurações do logger para escrever em um arquivo .txt
logging.basicConfig(
    filename="/home/valentinavps/POO/SistemaBancario/log.txt",  # Nome do arquivo de log
    filemode="a",  # Modo de abertura do arquivo (append)
    level=logging.INFO,  # Nível de log (informação)
    format="%(asctime)s - %(message)s",  # Formato das mensagens de log
    datefmt="%d-%m-%Y %H:%M:%S",  # Formato da data e hora
)


def main() -> None:
    
    pessoa = PessoaFisica(nome="Vava", data_nascimento="20/08/2002", cpf="88888888888", endereco="lala", senha="123")
    saque = Saque()
    deposito = Deposito()

    while True:
        opcao: str = menu()  # Exibe o menu e obtém a opção escolhida pelo usuário

        if opcao == "d":
            deposito.deposito()  # Chama a função para realizar um depósito
        elif opcao == "s":
            saque.sacar()  # Chama a função para realizar um saque
        elif opcao == "nu":
            pessoa.criar_cliente()  # Chama a função para criar um novo cliente
        elif opcao == "nc":
            pessoa.criar_conta()  # Chama a função para criar uma nova conta
        elif opcao == "q":
            break  # Sai do loop e encerra o programa
        else:
            print(
                Fore.RED + "\n❌❌❌ Operação inválida, por favor selecione novamente a operação desejada. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor

if __name__ == "__main__":
    main()
