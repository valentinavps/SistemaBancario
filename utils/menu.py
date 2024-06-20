import textwrap
from colorama import Fore, Style

def menu():
    menu_text = f"""{Fore.CYAN + Style.BRIGHT}
    ================ MENU ================
    [d]💰\tDepositar
    [s]💸\tSacar
    [e]📊\tExtrato
    [nc]📋\tNova conta
    [nu]👤\tNovo usuário
    [lc]📄\tListar contas
    [q]🚪\tSair
    => {Style.RESET_ALL}"""
    return input(textwrap.dedent(menu_text))
