import sqlite3
import os

# 1. Descobre a pasta atual (onde está o conexao.py)
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
# 2. Cria o caminho absoluto para o banco (vai ficar dentro da pasta database)
CAMINHO_BANCO = os.path.join(PASTA_ATUAL, "sistema_ong.db")


def criar_banco_dados():
    # Usando a variável com o caminho absoluto em vez de apenas o nome
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()

    # 1. Criando tabela Motorista
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS motorista (
        id_motorista INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT NOT NULL,
        cnh TEXT UNIQUE NOT NULL,
        telefone TEXT,
        status TEXT NOT NULL
    )
    """)

    # 2. Criando tabela Veiculos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veiculos (
        id_veiculo INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT UNIQUE NOT NULL,
        modelo TEXT NOT NULL,
        km_atual INTEGER NOT NULL,
        status TEXT NOT NULL
    )
    """)

    # 3. Criando a tabela CheckinCheckout
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checkin_checkout (
        id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
        id_motorista INTEGER,
        id_veiculo INTEGER,
        data_hora_retirada DATETIME NOT NULL,
        km_inicial INTEGER NOT NULL,
        data_hora_devolucao DATETIME,
        km_final INTEGER,
        observacoes_carro TEXT,
        FOREIGN KEY (id_motorista) REFERENCES motorista (id_motorista),
        FOREIGN KEY (id_veiculo) REFERENCES veiculos (id_veiculo)
    )
    """)

    # 4. Criando tabela Demandas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS demandas (
        id_demanda INTEGER PRIMARY KEY AUTOINCREMENT,
        id_veiculo INTEGER,
        tipo_demanda TEXT NOT NULL,
        origem TEXT NOT NULL,
        destino TEXT NOT NULL,
        data_horario_previsto DATETIME NOT NULL,
        status TEXT NOT NULL,
        necessidades_especiais TEXT,
        FOREIGN KEY (id_veiculo) REFERENCES veiculos (id_veiculo)
    )
    """)

    # Salva as alterações e fecha a conexão
    conexao.commit()
    conexao.close()
    print("Banco de dados 'sistema_ong.db' criado com sucesso!")


# Executa a função
if __name__ == "__main__":
    criar_banco_dados()
