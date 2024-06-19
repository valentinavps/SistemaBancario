from datetime import datetime
from colorama import Fore, Style
from models.conta_corrente import ContaCorrente
from utils.helpers import Helpers

from utils.helpers import filtrar_cliente, recuperar_conta_cliente, filtrar_cliente_txt

clientes_arquivotxt = "/home/valentinavps/POO/SistemaBancario/clientes.txt"
contas_arquivotxt = "/home/valentinavps/POO/SistemaBancario/contas.txt"

class PessoaFisica:
    def __init__(self, nome, data_nascimento, cpf, endereco, senha):
        self.endereco = endereco
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.__senha = senha

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, nova_senha):
        self.__senha = nova_senha

    def __repr__(self):
        return f"PessoaFisica(nome={self.nome}, cpf={self.cpf}, data_nascimento={self.data_nascimento}, endereco={self.endereco})"

    # Cria um novo cliente e salva seus dados no arquivo de clientes.txt
    def criar_cliente(self) -> None:
    
        while True:
            cpf_informado: str = input("Informe o CPF (somente números): ")

            # Verifica se o CPF contém apenas números e tem exatamente 11 dígitos
            if not cpf_informado.isdigit() or len(cpf_informado) != 11:
                print(Fore.RED + "\n❌❌❌ CPF inválido ❌❌❌")
                continue

            cliente: bool = Helpers.filtrar_cliente(cpf_informado)

            if cliente:
                print(Fore.YELLOW + "\n❗❗❗ Já existe cliente com esse CPF! ❗❗❗")
                return
            break

        while True:
            nome: str = input("Informe o nome completo: ")
            if nome.isalpha():
                break
            else:
                print("\n❌❌❌ Nome inválido! Informe apenas letras. ❌❌❌")

        while True:
            data_nascimento: str = input(
                "Informe a data de nascimento (dd/mm/aaaa): ")
            try:
                data_nascimento_dt: datetime = datetime.strptime(
                    data_nascimento, "%d/%m/%Y")
                break
            except ValueError:
                print(
                    Fore.RED + "\n❌❌❌ Formato de data inválido! Por favor, digite no formato dd/mm/aaaa. ❌❌❌")

        endereco: str = input(
            "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        data_nascimento_formatada: str = data_nascimento_dt.strftime(
            "%d-%m-%Y")
        senha: str = input("Informe sua senha: ")

        cliente = PessoaFisica(
            nome=nome, data_nascimento=data_nascimento_formatada, cpf=cpf_informado, endereco=endereco, senha=senha
        )

        data_hora: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open("log.txt", "a") as file:
            file.write(f"Cliente criado: {nome} | CPF: {cpf_informado} | ({data_hora})\n")
        with open(clientes_arquivotxt, "a") as file:
            file.write(f"nome:{cliente.nome}|cpf:{cpf_informado}|senha:{cliente.senha} \n")

        print(Fore.GREEN +
              f"\n✅✅✅ Cliente criado com sucesso! {data_hora} ✅✅✅")
