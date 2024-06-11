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
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao, conta):
        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        tipo_transacao = transacao.__class__.__name__
        valor_transacao = transacao.valor
        numero_conta = conta.numero

        for t in self._transacoes:
            if (
                t["conta"] == numero_conta
                and t["tipo"] == tipo_transacao
                and t["valor"] == valor_transacao
            ):
                return

        with open("log.txt", "a") as file:
            file.write(
                f"Conta: {numero_conta} | Tipo: {tipo_transacao} | "
                f"Valor: R$ {valor_transacao:.2f} | ({data_hora})\n"
            )

        registro_transacao = (
            f"{Fore.CYAN}Conta: {numero_conta} | Tipo: {tipo_transacao} | "
            f"Valor: R$ {valor_transacao:.2f} | ({data_hora})"
            f"{Style.RESET_ALL}"
        )
        self._transacoes.append(
            {
                "conta": numero_conta,
                "tipo": tipo_transacao,
                "valor": valor_transacao,
                "data": data_hora,
                "registro": registro_transacao,
            }
        )
