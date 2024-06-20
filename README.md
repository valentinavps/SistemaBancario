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
cd SistemaBancario/versao-2
```

## Execução

Para rodar o código, utilize o seguinte comando:
```bash
python main.py
```

## Estrutura do Projeto

- `conta.py`: Define a classe base `Conta` e suas operações.
- `conta_corrente.py`: Define a classe `ContaCorrente`, que herda de `Conta` e adiciona funcionalidades específicas.
- `historico.py`: Gerencia o histórico de transações das contas.
- `pessoa_fisica.py`: Define a classe para clientes pessoas físicas.
- `transacao.py`: Define classes abstratas para transações e suas implementações (saque e depósito).
- `helpers.py`: Funções auxiliares para manipulação de arquivos e clientes.
- `menu.py`: Função para exibição do menu principal do sistema.
- `main.py`: Script principal que gerencia o fluxo do sistema.
- `operacoes.py`: Define as operações bancárias e suas implementações.

## Exemplos de Código

### conta_corrente.py

```python
from colorama import Fore, Style
from .conta import Conta
from models.transacao import Saque

class ContaCorrente(Conta):
    def __init__(self, numero: str, cliente: Cliente, limite: float = 500, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        numero_saques = sum(1 for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__)
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(Fore.RED + "\n❌❌❌ Operação falhou! O valor do saque excede o limite. ❌❌❌")
            print(Style.RESET_ALL)
            return False

        elif excedeu_saques:
            print(Fore.RED + "\n❌❌❌ Operação falhou! Número máximo de saques excedido. ❌❌❌")
            print(Style.RESET_ALL)
            return False

        return super().sacar(valor)

    def __str__(self) -> str:
        return f"""{Fore.WHITE}
    ========== CONTA CORRENTE ==========
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
    {Style.RESET_ALL}"""
```

### conta.py

```python
from colorama import Fore, Style
from datetime import datetime
from .historico import Historico

class Conta:
    def __init__(self, numero: str, cliente: Cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: str) -> 'Conta':
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
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    def sacar(self, valor: float) -> bool:
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print(Fore.RED + "\n❌❌❌ Operação falhou! Você não tem saldo suficiente. ❌❌❌")
            print(Style.RESET_ALL)
            return False
        elif valor <= 0:
            print(Fore.RED + "\n❌❌❌ Operação falhou! O valor informado é inválido. ❌❌❌")
            print(Style.RESET_ALL)
            return False

        self._saldo -= valor
        print(Fore.GREEN + f"\n✅✅✅ Saque realizado com sucesso! {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ✅✅✅")
        print(Style.RESET_ALL)
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print(Fore.RED + "\n❌❌❌ Operação falhou! O valor informado é inválido. ❌❌❌")
            print(Style.RESET_ALL)
            return False

        self._saldo += valor
        print(Fore.GREEN + f"\n✅✅✅ Depósito realizado com sucesso! {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ✅✅✅")
        print(Style.RESET_ALL)
        return True
```

## Contribuição

Para contribuir com o projeto, faça um fork do repositório, crie uma nova branch com suas alterações e envie um pull request.


---

**Nota:** Os caminhos dos arquivos e outras configurações específicas devem ser ajustados conforme necessário para o ambiente de execução.
