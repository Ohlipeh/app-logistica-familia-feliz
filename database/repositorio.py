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


# Classe para manipular o BD.
class ControleFrota:
    def __init__(self, db_nome="sistema_ong.db"):
        self.db_nome = db_nome

    def cadastrar_demanda(self, tipo_demanda, origem, destino):
        # Captura a data/hora atual para usar como previsão inicial
        data_prevista = datetime.now()

        conexao = sqlite3.connect(self.db_nome)
        cursor = conexao.cursor()

        # O id_veiculo fica vazio (NULL) por enquanto, porque a demanda acabou de ser criada
        # e ainda não tem um carro atribuído.
        cursor.execute(
            "INSERT INTO demandas (tipo_demanda, origem, destino, data_horario_previsto, status) VALUES (?, ?, ?, ?, ?)",
            (tipo_demanda, origem, destino, data_prevista, "Pendente"),
        )

        conexao.commit()
        conexao.close()
        print(f"Demanda de {tipo_demanda} para {destino} cadastrada no banco!")

    def buscar_demandas_recentes(self):
        conexao = sqlite3.connect(self.db_nome)
        cursor = conexao.cursor()

        # O SELECT busca os campos na ordem que exibir.
        # Adicionamos o id_demanda logo no início
        cursor.execute("""
            SELECT id_demanda, data_horario_previsto, tipo_demanda, origem, status 
            FROM demandas 
            ORDER BY id_demanda DESC LIMIT 5
        """)

        resultados = cursor.fetchall()  # Captura todas as linhas encontradas
        conexao.close()

        return resultados

    def atualizar_status_demanda(self, id_demanda, novo_status):
        conexao = sqlite3.connect(self.db_nome)
        cursor = conexao.cursor()

        cursor.execute(
            "UPDATE demandas SET status = ? WHERE id_demanda = ?",
            (novo_status, id_demanda),
        )

        conexao.commit()
        conexao.close()

    def obter_resumo_dashboard(self):
        conexao = sqlite3.connect(self.db_nome)
        cursor = conexao.cursor()

        # Conta veículos livres
        cursor.execute("SELECT COUNT(*) FROM veiculos WHERE status = 'Livre'")
        livres = cursor.fetchone()[
            0
        ]  # fetchone()[0] pega exatamente o número da resposta

        # Conta veículos em rota
        cursor.execute("SELECT COUNT(*) FROM veiculos WHERE status = 'Em Rota'")
        em_rota = cursor.fetchone()[0]

        # Conta demandas pendentes
        cursor.execute("SELECT COUNT(*) FROM demandas WHERE status = 'Pendente'")
        pendentes = cursor.fetchone()[0]

        conexao.close()

        return livres, em_rota, pendentes

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

    def realizar_checkout(self, id_veiculo, km_final):
        data = datetime.now()

        # Conecta diretamente no banco
        conexao = sqlite3.connect(self.db_nome)
        cursor = conexao.cursor()

        # Adicionando 'data_hora_devolucao'
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
