from models.pessoa_fisica import PessoaFisica
from models.conta_corrente import ContaCorrente
from models.transacao import Saque
from utils.helpers import recuperar_conta_cliente
from datetime import datetime
from colorama import Fore, Style
from typing import List

# Caminho dos arquivos de contas e clientes
contas_arquivotxt: str = "/home/valentinavps/POO/SistemaBancario/contas.txt"
clientes_arquivotxt: str = "/home/valentinavps/POO/SistemaBancario/clientes.txt"

class Operacoes:
    def __init__(self, clientes_arquivo: str) -> None:
        self.clientes_arquivo: str = clientes_arquivo
        self.clientes: list = self.ler_clientes_arquivo()

    # Lê os clientes do arquivo e os armazena em uma lista de dicionários.
    def ler_clientes_arquivo(self) -> List[dict]:
        clientes = []
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
            print(Fore.RED + f"Arquivo {self.clientes_arquivo} não encontrado.")
        return clientes

    # Filtra os clientes pelo CPF informado.
    def filtrar_cliente(self, cpf_informado: str) -> dict:
        for cliente in self.clientes:
            if cliente.get('cpf') == cpf_informado:
                return cliente
        return None

    def criar_cliente(self) -> None:
        while True:
            cpf = input("Informe o CPF (somente números): ")
            if not cpf.isdigit() or len(cpf) != 11:
                print(Fore.RED + "\n❌❌❌ CPF inválido ❌❌❌")
                print(Style.RESET_ALL)
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
            file.write(f"nome:{cliente.nome}|cpf:{cpf}|senha:{cliente.senha} \n")

        print(Fore.GREEN + f"\n✅✅✅ Cliente criado com sucesso! {data_hora} ✅✅✅")

    def criar_conta(self, contas: List[ContaCorrente], numero_conta: str) -> None:
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print(Fore.RED + "\n❌❌❌ Cliente não encontrado, fluxo de criação de conta encerrado! ❌❌❌")
            print(Style.RESET_ALL)
            return
        
        senha = input("Informe a senha: ")
        if cliente.get('senha') != senha:
            print(Fore.RED + "\n❌❌❌ Senha incorreta! ❌❌❌")
            print(Style.RESET_ALL)
            return

        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        
        # Adicionando a conta ao cliente (simulação, ajuste conforme seu modelo)
        if 'contas' not in cliente:
            cliente['contas'] = []
        cliente['contas'].append(numero_conta)

        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open("log.txt", "a") as file:
            file.write(f"Nova conta criada para o cliente {cliente['nome']} | Conta: {numero_conta} | ({data_hora})\n")
        with open(contas_arquivotxt, "a") as file:
            file.write(f"Cliente: {cliente['nome']}| Conta: {numero_conta} \n")

        print(Fore.GREEN + f"\n✅✅✅ Conta criada com sucesso! {data_hora} ✅✅✅")
        print(Style.RESET_ALL)

    def sacar(self) -> None:
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
            print(Style.RESET_ALL)
            return

        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)

        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return

        cliente.realizar_transacao(conta, transacao)

    def exibir_extrato(self, conta: ContaCorrente) -> None:
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print(Fore.RED + "\n❌❌❌ Cliente não encontrado! ❌❌❌")
            print(Style.RESET_ALL)
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

# Exemplo de uso:
if __name__ == "__main__":
    operacoes = Operacoes(clientes_arquivotxt)
    operacoes.criar_cliente()
    numero_conta = "12345-6"  # Exemplo de número de conta
    contas = []  # Lista de contas, deve ser substituída pela implementação real
    operacoes.criar_conta(contas, numero_conta)
