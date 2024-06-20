# Sistema Bancário

## Descrição do Projeto

Este projeto consiste em um sistema bancário simples, implementado em Python. Ele permite realizar operações básicas como criar contas, sacar, depositar, e consultar extratos.

## Autores

- [Mariana Villefort](https://github.com/MarianaVRabelo)
- [Maria Clara Ferreira](https://github.com/mariacferreirab)
- [Valentina Perpetuo](https://github.com/valentinavps)

## Requisitos

- Python 3.6 ou superior
- Biblioteca `colorama`

## Instalação

Clone o repositório do projeto:
```bash
git clone https://github.com/valentinavps/SistemaBancario.git
cd SistemaBancario/VersaoOficial
```

## Execução

Para rodar o código, utilize o seguinte comando:
```bash
python main.py
```

## Estrutura do Projeto

- `conta.py`: Define a classe base `Conta` e suas operações.
- `historico.py`: Gerencia o histórico de transações das contas.
- `pessoa_fisica.py`: Define a classe para clientes pessoas físicas.
- `menu.py`: Função para exibição do menu principal do sistema.
- `main.py`: Script principal que gerencia o fluxo do sistema.

## Exemplos de Código

### conta.py

```python
from colorama import Fore, Style
from datetime import datetime
from typing import Type

from .historico import Historico

class Conta:
    def __init__(self, numero: str):
        self._saldo = 0  # Saldo inicialmente zerado
        self._numero = numero  # Número da conta
        self._agencia = "0001"  # Agência fixa
        self._historico = Historico()  # Histórico de transações associado à conta

    @classmethod
    def nova_conta(cls, cliente, numero: str) -> 'Conta':
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> str:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def historico(self) -> Historico:
        return self._historico

    def sacar(self, valor: float) -> bool:
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print(Fore.RED + "\n❌❌❌ Operação falhou! Você não tem saldo suficiente. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return False
        elif valor <= 0:
            print(Fore.RED + "\n❌❌❌ Operação falhou! O valor informado é inválido. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        self._saldo -= valor
        print(Fore.GREEN + f"\n✅✅✅ Saque realizado com sucesso! {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ✅✅✅")
        print(Style.RESET_ALL)  # Resetando a cor
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print(Fore.RED + "\n❌❌❌ Operação falhou! O valor informado é inválido. ❌❌❌")
            print(Style.RESET_ALL)  # Resetando a cor
            return False

        self._saldo += valor
        print(Fore.GREEN + f"\n✅✅✅ Depósito realizado com sucesso! {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ✅✅✅")
        print(Style.RESET_ALL)  # Resetando a cor
        return True
```

### historico.py

```python
import logging
from datetime import datetime
from colorama import Fore, Style

# Configurações do logger para escrever em um arquivo .txt
logging.basicConfig(
    filename="/home/valentinavps/POO/SistemaBancario/log.txt",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)

class Historico:
    def __init__(self):
        """
        Inicializa um objeto Histórico com uma lista vazia de transações.
        """
        self._transacoes = []

    @property
    def transacoes(self):
        """
        Propriedade que retorna a lista de transações.

        Returns:
        - list: Lista de transações.
        """
        return self._transacoes

    def adicionar_transacao(self, transacao, conta):
        """
        Adiciona uma transação ao histórico, registrando-a em um arquivo de log e na lista de transações, 
        se a transação ainda não estiver registrada.

        Args:
        - transacao: Objeto de transação a ser adicionado (deve ter um atributo 'valor').
        - conta: Objeto de conta associado à transação.

        Returns:
        - None
        """
        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # Obtém o nome da classe da transação
        tipo_transacao = transacao.__class__.__name__
        valor_transacao = transacao.valor  # Obtém o valor da transação
        numero_conta = conta.numero  # Obtém o número da conta associada à transação

        # Verifica se a transação já foi registrada para a mesma conta, tipo e valor
        for t in self._transacoes:
            if (t["conta"] == numero_conta
                and t["tipo"] == tipo_transacao
                    and t["valor"] == valor_transacao):
                return  # Se encontrou uma transação idêntica, retorna sem adicionar novamente

        # Registra a transação no arquivo de log
        with open("log.txt", "a") as file:
            file.write(
                f"Conta: {numero_conta} | Tipo: {tipo_transacao} | "
                f"Valor: R$ {valor_transacao:.2f} | ({data_hora})\n"
            )

        # Formata o registro da transação para ser adicionado à lista de transações
        registro_transacao = (
            f"{Fore.CYAN}Conta: {numero_conta} | Tipo: {tipo_transacao} | "
            f"Valor: R$ {valor_transacao:.2f} | ({data_hora})"
            f"{Style.RESET_ALL}"
        )

        # Adiciona a transação à lista de transações do histórico
        self._transacoes.append(
            {
                "conta": numero_conta,
                "tipo": tipo_transacao,
                "valor": valor_transacao,
                "data": data_hora,
                "registro": registro_transacao,
            }
        )
```

### pessoa_fisica.py

```python
from colorama import Fore, Style
from typing import List
from models.conta import Conta
from datetime import datetime
import random

clientes_arquivotxt = "/home/valentinavps/POO/SistemaBancario/clientes.txt"
contas_arquivotxt = "/home/valentinavps/POO/SistemaBancario/contas.txt"
transacoes_arquivotxt = "/home/valentinavps/POO/SistemaBancario/transacoes.txt"

class PessoaFisica:
    def __init__(self, nome, data_nascimento, cpf, endereco, senha):
        self.endereco = endereco
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.__senha = senha
        self.clientes = []

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, nova_senha):
        self.__senha = nova_senha

    def __repr__(self):
        return f"PessoaFisica(nome={self.nome}, cpf={self.cpf}, data_nascimento={self.data_nascimento}, endereco={self.endereco})"
    
    def ler_clientes_arquivo(self):
        clientes = []
        try:
            with open(clientes_arquivotxt, 'r') as file:
                for linha in file:
                    partes = linha.strip().split('|')
                    cliente = {}
                    for parte in partes:
                        if ':' in parte:
                            chave, valor = parte.split(':', 1)
                            cliente[chave] = valor
                    clientes.append(cliente)
        except FileNotFoundError:
            print(Fore.RED + f"Arquivo {clientes_arquivotxt} não encontrado.")
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro: {e}")
        return clientes
       

    # Filtra os clientes pelo CPF informado.
    def filtrar_cliente(self, cpf_informado: str):
        if not self.clientes:
            self.clientes = self.ler_clientes_arquivo()
        
        for cliente in self.clientes:
            if cliente.get('cpf') == cpf_informado:
                return cliente  # Retorna o cliente se encontrar o CPF informado
        
        return None  # Retorna None se não encontrar nenhum cliente com o CPF informado

    def criar_cliente(self):
        while True:
            cpf = input("Informe o CPF

 (somente números): ")
            if not cpf.isdigit() or len(cpf) != 11:
                print(Fore.RED + "CPF inválido. Certifique-se de que contém apenas números e tem 11 dígitos.")
                print(Style.RESET_ALL)  # Resetando a cor
                continue
            
            cliente_existente = self.filtrar_cliente(cpf)
            if cliente_existente:
                print(Fore.RED + "Cliente já existe. Tente novamente com um CPF diferente.")
                print(Style.RESET_ALL)  # Resetando a cor
                continue

            break
        
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
        endereco = input("Informe o endereço: ")
        senha = input("Informe a senha: ")
        
        novo_cliente = PessoaFisica(nome, data_nascimento, cpf, endereco, senha)
        self.clientes.append(novo_cliente)
        
        try:
            with open(clientes_arquivotxt, 'a') as file:
                file.write(f"Nome:{nome}|Data de Nascimento:{data_nascimento}|CPF:{cpf}|Endereço:{endereco}|Senha:{senha}\n")
            
            print(Fore.GREEN + "Cliente criado com sucesso!")
            print(Style.RESET_ALL)  # Resetando a cor
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro ao salvar o cliente: {e}")
            print(Style.RESET_ALL)  # Resetando a cor

        return novo_cliente


    def criar_conta(self):
        cpf_informado = input("Informe o CPF do cliente: ")
        cliente_existente = self.filtrar_cliente(cpf_informado)
        
        if cliente_existente:
            numero_conta = random.randint(1000, 9999)
            nova_conta = Conta(numero_conta)
            
            try:
                with open(contas_arquivotxt, 'a') as file:
                    file.write(f"Conta:{numero_conta}|Cliente_CPF:{cpf_informado}|Data_Criação:{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
                
                print(Fore.GREEN + "Conta criada com sucesso!")
                print(Style.RESET_ALL)  # Resetando a cor
            except Exception as e:
                print(Fore.RED + f"Ocorreu um erro ao salvar a conta: {e}")
                print(Style.RESET_ALL)  # Resetando a cor
            
            return nova_conta
        else:
            print(Fore.RED + "Cliente não encontrado. Verifique o CPF e tente novamente.")
            print(Style.RESET_ALL)  # Resetando a cor
            return None
```

### menu.py

```python
from models.pessoa_fisica import PessoaFisica
from models.conta import Conta
from models.historico import Historico

def exibir_menu():
    """
    Exibe o menu de opções para o usuário e processa a escolha.
    """
    while True:
        print("\n--- Sistema Bancário ---")
        print("1. Criar novo cliente")
        print("2. Criar nova conta")
        print("3. Sacar")
        print("4. Depositar")
        print("5. Visualizar Extrato")
        print("6. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cliente = PessoaFisica("", "", "", "", "")
            cliente.criar_cliente()
        elif opcao == '2':
            cliente = PessoaFisica("", "", "", "", "")
            cliente.criar_conta()
        elif opcao == '3':
            numero_conta = input("Informe o número da conta: ")
            valor = float(input("Informe o valor a ser sacado: "))
            conta = Conta(numero_conta)
            conta.sacar(valor)
            historico = Historico()
            historico.adicionar_transacao(conta, valor)
        elif opcao == '4':
            numero_conta = input("Informe o número da conta: ")
            valor = float(input("Informe o valor a ser depositado: "))
            conta = Conta(numero_conta)
            conta.depositar(valor)
            historico = Historico()
            historico.adicionar_transacao(conta, valor)
        elif opcao == '5':
            numero_conta = input("Informe o número da conta: ")
            conta = Conta(numero_conta)
            print("\n--- Extrato ---")
            for transacao in conta.historico.transacoes:
                print(transacao)
        elif opcao == '6':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
```



## Contribuições

Para contribuir com o projeto, siga as etapas abaixo:

1. Faça um fork do projeto.
2. Crie uma branch com a nova feature (`git checkout -b feature/nova-feature`).
3. Commit as mudanças (`git commit -am 'Adiciona nova feature'`).
4. Push para a branch (`git push origin feature/nova-feature`).
5. Crie um novo Pull Request.
