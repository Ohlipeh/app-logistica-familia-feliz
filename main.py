import sqlite3

# Importa a classe do arquivo que você acabou de criar (se chamou de classes.py, mude aqui)
from database.repositorio import ControleFrota


def preparar_banco_para_teste():
    """
    Função rápida só para inserir 1 motorista e 1 carro no banco.
    Isso é necessário porque a tabela checkin exige que o carro e o motorista existam
    (por causa da Foreign Key!).
    """
    conexao = sqlite3.connect("sistema_ong.db")
    cursor = conexao.cursor()

    # Ignora o erro se o motorista ou carro já existirem no teste anterior
    try:
        cursor.execute(
            "INSERT INTO motorista (nome_completo, cnh, status) VALUES ('João Silva', '123456789', 'Ativo')"
        )
        cursor.execute(
            "INSERT INTO veiculos (placa, modelo, km_atual, status) VALUES ('ABC-1234', 'HB20', 50000, 'Livre')"
        )
        conexao.commit()
    except sqlite3.IntegrityError:
        pass  # Se já existe, não faz nada

    conexao.close()


# --- INÍCIO DO SCRIPT DE TESTE ---

print("Preparando ambiente de teste...")
preparar_banco_para_teste()

print("\nIniciando sistema...")
sistema = ControleFrota()

# Simulando um Check-in: Motorista ID 1 pegou o Carro ID 1 com 50.000 KM
sistema.realizar_checkin(id_motorista=1, id_veiculo=1, km_inicial=50000)

# Simulando um Check-out: Ele devolveu o Carro ID 1 no final do dia com 50.150 KM
sistema.realizar_checkout(id_veiculo=1, km_final=50150)

print("\nTeste finalizado!")
