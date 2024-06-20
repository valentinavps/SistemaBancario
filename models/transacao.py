from abc import ABC, abstractclassmethod, abstractproperty

# Classe abstrata Transacao, que serve como base para outras classes de transações


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self) -> float:
        """Getter abstrato para o valor da transação."""
        pass

    @abstractclassmethod
    def registrar(cls, conta: object) -> None:
        """
        Método abstrato para registrar uma transação em uma conta específica.

        Args:
        - conta (object): Objeto da conta onde a transação será registrada.

        Returns:
        - None
        """
        pass

# Classe Saque que herda de Transacao e implementa os métodos abstratos


class Saque(Transacao):
    def __init__(self, valor: float) -> None:
        """
        Inicializa um objeto Saque com um valor específico.

        Args:
        - valor (float): Valor do saque.
        """
        self._valor: float = valor

    @property
    def valor(self) -> float:
        """
        Retorna o valor do saque.

        Returns:
        - float: Valor do saque.
        """
        return self._valor

    def registrar(self, conta: object) -> None:
        """
        Registra o saque em uma conta, adicionando-o ao histórico se for bem-sucedido.

        Args:
        - conta (object): Objeto da conta onde o saque será registrado.

        Returns:
        - None
        """
        sucesso_transacao: bool = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self, conta)

# Classe Deposito que herda de Transacao e implementa os métodos abstratos


class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        """
        Inicializa um objeto Deposito com um valor específico.

        Args:
        - valor (float): Valor do depósito.
        """
        self._valor: float = valor

    @property
    def valor(self) -> float:
        """
        Retorna o valor do depósito.

        Returns:
        - float: Valor do depósito.
        """
        return self._valor

    def registrar(self, conta: object) -> None:
        """
        Registra o depósito em uma conta, adicionando-o ao histórico se for bem-sucedido.

        Args:
        - conta (object): Objeto da conta onde o depósito será registrado.

        Returns:
        - None
        """
        sucesso_transacao: bool = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self, conta)
