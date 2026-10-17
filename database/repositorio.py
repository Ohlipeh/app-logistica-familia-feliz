from datetime import datetime
import sqlite3
import os

# Importa o caminho do banco e a função de criar tabelas do seu ficheiro conexao.py
from database.conexao import criar_banco_dados, CAMINHO_BANCO


class Veiculo:
    def __init__(self, placa, modelo, km_atual):
        self.placa = placa
        self.modelo = modelo
        self.km_atual = km_atual
        self.status = "Livre"

    def exibir_informacoes(self):
        print(f"Placa: {self.placa} - Modelo: {self.modelo} - Km: {self.km_atual}")


# --- Classe para manipular o BD. ---
class ControleFrota:
    def __init__(self):
        # 1. Usa o caminho exato que foi definido no conexao.py
        self.db_nome = CAMINHO_BANCO

        # 2. Chama a sua função de criar tabelas sempre que o sistema arrancar!
        # Assim, se o banco ou as tabelas não existirem, ele cria automaticamente.
        criar_banco_dados()

    # --- Função para cadastrar a demanda ---
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

    # --- Função para buscar a demanda ---
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

        # Captura todas as linhas encontradas
        resultados = cursor.fetchall()
        conexao.close()

        return resultados

    # --- Função para atualizar o status da demanda ---
    def atualizar_status_demanda(self, id_demanda, novo_status):
        conexao = sqlite3.connect(self.db_nome)
        cursor = conexao.cursor()

        # UPDATE pra atualizar demanda
        cursor.execute(
            "UPDATE demandas SET status = ? WHERE id_demanda = ?",
            (novo_status, id_demanda),
        )

        conexao.commit()
        conexao.close()

    # --- Função para excluir demanda ---
    def excluir_demanda(self, id_demanda):
        conexao = sqlite3.connect(self.db_nome)
        cursor = conexao.cursor()

        # Comando DELETE remove a linha específica usando a Chave Primária
        cursor.execute("DELETE FROM demandas WHERE id_demanda = ?", (id_demanda,))

        conexao.commit()
        conexao.close()
        print(f"Demanda ID {id_demanda} excluída com sucesso.")

    # --- Função para obter resumo de Deshboard ---
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

    # --- Função para cadastrar o veiculo ---
    def cadastrar_veiculo(self, placa, modelo, km_atual):
        conexao = sqlite3.connect(self.db_nome)
        cursor = conexao.cursor()

        # Insere valores na tabela veiculos
        cursor.execute(
            "INSERT INTO veiculos (placa, modelo, km_atual, status) VALUES (?, ?, ?, ?)",
            (placa, modelo, km_atual, "Livre"),
        )
        conexao.commit()
        conexao.close()

        print("Cadastro realizado com sucesso!")

    # --- Função para excluir o veiculo ---
    def excluir_veiculo(self, id_veiculo):
        conexao = sqlite3.connect(self.db_nome)
        cursor = conexao.cursor()

        # Comando DELETE remove a linha específica usando a Chave Primária
        cursor.execute("DELETE FROM veiculos WHERE id_veiculo = ?", (id_veiculo,))

        conexao.commit()
        conexao.close()
        print(f"Veiculo ID {id_veiculo} excluído com sucesso.")

    # --- Função para buscar veiculo ---
    def buscar_veiculos(self):
        conexao = sqlite3.connect(self.db_nome)
        cursor = conexao.cursor()

        # Busca todas as informações dos veículos
        cursor.execute(
            "SELECT id_veiculo, placa, modelo, km_atual, status FROM veiculos"
        )
        resultados = cursor.fetchall()

        conexao.close()
        return resultados

    # --- Função para realizar Check-in ---
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

    # --- Função para realizar Checkout ---
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
