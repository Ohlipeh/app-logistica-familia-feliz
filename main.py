from datetime import datetime
import sqlite3


class Veiculo:
    def __init__(self, placa, modelo, km_atual):
        self.placa = placa
        self.modelo = modelo
        self.km_atual = km_atual
        self.status = "Livre"

    def exibir_informacoes(self):
        print(f"Placa: {self.placa} - Modelo: {self.modelo} - Km: {self.km_atual}")


class ControleFrota:
    def __init__(self, db_nome="sistema_ong.db"):
        self.db_nome = db_nome

    def realizar_checkin(self, id_motorista, id_veiculo, km_inicial):
        data = datetime.now()

        # Conecta diretamente no banco
        conexao = sqlite3.connect(self.db_nome)
        cursor = conexao.cursor()

        # Adicionando 'data_hora_retirada'
        cursor.execute(
            "INSERT INTO checkin_checkout (id_motorista, id_veiculo, data_hora_retirada, km_inicial) VALUES (?, ?, ?, ?)",
            (id_motorista, id_veiculo, data, km_inicial),
        )
        conexao.commit()
        conexao.close()

        print(f"Check-in realizado para o veículo ID {id_veiculo}.")

    def realizar_checkout(self, id_motorista, id_veiculo, km_final):
        data = datetime.now()

        conexao = sqlite3.connect(self.db_nome)
        cursor = conexao.cursor()

        cursor.execute(
            """
            UPDATE checkin_checkout
            SET data_hora_devolucao = ?, km_final = ?
            WHERE id_veiculo = ? AND data_hora_devolucao IS NULL
        """,
            (data, km_final, id_veiculo),
        )

        conexao.commit()
        conexao.close()

        print(f"Checkout realizado para o veículo ID {id_veiculo}.")
