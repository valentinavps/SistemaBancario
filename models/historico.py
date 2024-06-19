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
