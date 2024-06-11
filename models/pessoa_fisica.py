from datetime import datetime
from .cliente import Cliente

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf

        while True:
            try:
                data_nascimento_dt = datetime.strptime(data_nascimento, "%d-%m-%Y")
                data_atual = datetime.now()
                if data_nascimento_dt > data_atual:
                    raise ValueError("❌ Data de nascimento não pode ser maior que a data atual. ❌")
                else:
                    self.data_nascimento = data_nascimento
                    break
            except ValueError as e:
                print(e)
                data_nascimento = input("Informe uma nova data de nascimento (dd-mm-aaaa): ")

    def __repr__(self):
        return f"PessoaFisica(nome={self.nome}, cpf={self.cpf}, data_nascimento={self.data_nascimento}, endereco={self.endereco})"
