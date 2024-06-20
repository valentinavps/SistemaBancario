import textwrap
from colorama import Fore, Style


def menu() -> str:
    """
    Exibe o menu principal para o usuário e retorna a opção escolhida.

    Returns:
    - str: A opção escolhida pelo usuário.
    """
    # Texto do menu formatado com cores e estilo
    menu_text: str = f"""{Fore.CYAN + Style.BRIGHT}
    ================ MENU ================
    [d]💰\tDepositar
    [s]💸\tSacar
    [e]📊\tExtrato
    [nc]📋\tNova conta
    [nu]👤\tNovo usuário
    [lc]📄\tListar contas
    [q]🚪\tSair
    => {Style.RESET_ALL}"""

    # Exibe o menu e retorna a entrada do usuário, removendo indentação
    return input(textwrap.dedent(menu_text))
