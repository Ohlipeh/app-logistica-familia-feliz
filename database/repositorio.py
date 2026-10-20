from datetime import datetime
import os
import gspread


class Veiculo:
    def __init__(self, placa, modelo, km_atual):
        self.placa = placa
        self.modelo = modelo
        self.km_atual = km_atual
        self.status = "Livre"

    def exibir_informacoes(self):
        print(f"Placa: {self.placa} - Modelo: {self.modelo} - Km: {self.km_atual}")


# --- Classe para manipular o BD na NUVEM (Google Sheets) ---
class ControleFrota:
    def __init__(self):
        # 1. Pega os caminhos exatos dos arquivos na pasta database
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_credenciais = os.path.join(pasta_atual, "credentials.json")
        caminho_token = os.path.join(pasta_atual, "token.json")

        # 2. Faz o Login usando a Autenticação de Utilizador (OAuth)
        # Na primeira vez, isto vai abrir o navegador para aprovar.
        # Depois, ele salva um "token.json" oculto para não ter de pedir mais!
        cliente = gspread.oauth(
            credentials_filename=caminho_credenciais,
            authorized_user_filename=caminho_token,
        )

        # 3. Abre a planilha pelo NOME EXATO que está no Google Drive
        self.planilha = cliente.open("Banco de Dados - ONG Familia Feliz")

        # 4. Seleciona as abas (Worksheets)
        self.aba_demandas = self.planilha.worksheet("Demandas")
        self.aba_veiculos = self.planilha.worksheet("Veiculos")
        self.aba_checkin = self.planilha.worksheet("CheckinCheckout")

        print("Conectado ao Google Sheets com sucesso!")

    # --- Função para cadastrar a demanda ---
    def cadastrar_demanda(self, tipo_demanda, origem, destino):
        # O Sheets prefere as datas formatadas em texto simples
        data_prevista = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Pega todas as linhas para descobrir qual é o último ID
        registros = self.aba_demandas.get_all_values()

        # Se a planilha só tiver o cabeçalho (linha 1), o id é 1. Senão, é o último id + 1.
        novo_id = int(registros[-1][0]) + 1 if len(registros) > 1 else 1

        # Adiciona uma nova linha no final da aba Demandas
        # Colunas: id_demanda, data, tipo_demanda, origem, destino, status
        self.aba_demandas.append_row(
            [novo_id, data_prevista, tipo_demanda, origem, destino, "Pendente"]
        )
        print(f"Demanda de {tipo_demanda} para {destino} salva no Sheets!")

    # --- Função para buscar a demanda ---
    def buscar_demandas_recentes(self):
        # Pega todos os dados da aba e ignora a linha 1 (que são os cabeçalhos [1:])
        registros = self.aba_demandas.get_all_values()[1:]

        resultados = []
        for linha in registros:
            # Pega as colunas na mesma ordem que o seu painel espera
            # 0:id_demanda, 1:data, 2:tipo_demanda, 3:origem, 5:status
            resultados.append((int(linha[0]), linha[1], linha[2], linha[3], linha[5]))

        # Inverte a lista (para os mais recentes aparecerem primeiro) e pega só os 5 primeiros
        resultados.reverse()
        return resultados[:5]

    # --- Função para atualizar o status da demanda ---
    def atualizar_status_demanda(self, id_demanda, novo_status):
        # Encontra em qual linha exata (row) está este ID na Coluna 1 da planilha
        celula = self.aba_demandas.find(str(id_demanda), in_column=1)
        if celula:
            # Atualiza a coluna 6 (Status) daquela linha encontrada
            self.aba_demandas.update_cell(celula.row, 6, novo_status)

    # --- Função para excluir demanda ---
    def excluir_demanda(self, id_demanda):
        # Encontra a linha pelo ID
        celula = self.aba_demandas.find(str(id_demanda), in_column=1)
        if celula:
            # Deleta a linha inteira do Sheets
            self.aba_demandas.delete_rows(celula.row)
            print(f"Demanda ID {id_demanda} excluída com sucesso.")

    # --- Função para obter resumo de Dashboard ---
    def obter_resumo_dashboard(self):
        veiculos = self.aba_veiculos.get_all_values()[1:]
        demandas = self.aba_demandas.get_all_values()[1:]

        # Conta veículos livres e em rota (Coluna de Status na planilha Veiculos é o índice 4)
        livres = sum(1 for v in veiculos if v[4] == "Livre")
        em_rota = sum(1 for v in veiculos if v[4] == "Em Rota")

        # Conta demandas pendentes (Coluna de Status na planilha Demandas é o índice 5)
        pendentes = sum(1 for d in demandas if d[5] == "Pendente")

        return livres, em_rota, pendentes

    # --- Função para cadastrar o veiculo ---
    def cadastrar_veiculo(self, placa, modelo, km_atual):
        registros = self.aba_veiculos.get_all_values()
        novo_id = int(registros[-1][0]) + 1 if len(registros) > 1 else 1

        # Adiciona a linha. Colunas: id_veiculo, placa, modelo, km_atual, status
        self.aba_veiculos.append_row([novo_id, placa, modelo, km_atual, "Livre"])
        print("Veículo cadastrado no Sheets com sucesso!")

    # --- Função para buscar veiculo ---
    def buscar_veiculos(self):
        registros = self.aba_veiculos.get_all_values()[1:]

        resultados = []
        for linha in registros:
            # Puxa os dados formatados
            resultados.append((int(linha[0]), linha[1], linha[2], linha[3], linha[4]))
        return resultados

    # --- Função para excluir o veiculo ---
    def excluir_veiculo(self, id_veiculo):
        celula = self.aba_veiculos.find(str(id_veiculo), in_column=1)
        if celula:
            self.aba_veiculos.delete_rows(celula.row)
            print(f"Veiculo ID {id_veiculo} excluído com sucesso.")

    # --- Função para realizar Check-in ---
    def realizar_checkin(self, id_motorista, id_veiculo, km_inicial):
        data = datetime.now().strftime("%Y-%m-%d %H:%M")
        registros = self.aba_checkin.get_all_values()

        # Pega o último ID ou começa no 1
        novo_id = int(registros[-1][0]) + 1 if len(registros) > 1 else 1

        # Insere a linha. Colunas: id_registro, id_motorista, id_veiculo, retirada, km_inicial, devolucao, km_final, obs
        self.aba_checkin.append_row(
            [novo_id, id_motorista, id_veiculo, data, km_inicial, "", "", ""]
        )
        print(f"Check-in realizado para o veículo ID {id_veiculo}.")

    # --- Função para realizar Checkout ---
    def realizar_checkout(self, id_veiculo, km_final, observacoes=""):
        data = datetime.now().strftime("%Y-%m-%d %H:%M")
        registros = self.aba_checkin.get_all_values()

        linha_alvo = None
        # O reversed() faz ele procurar de baixo para cima (do mais recente para o mais antigo)
        for index, linha in reversed(list(enumerate(registros))):
            if index > 0:
                # Verifica se o carro é o mesmo e se a devolução (coluna 6) está em branco
                if str(linha[2]) == str(id_veiculo) and linha[5] == "":
                    linha_alvo = index + 1
                    break

        if linha_alvo:
            self.aba_checkin.update_cell(linha_alvo, 6, data)
            self.aba_checkin.update_cell(linha_alvo, 7, km_final)

            # Força a gravação da observação (mesmo se estiver vazia)
            texto_obs = str(observacoes) if observacoes else "Sem observações"
            self.aba_checkin.update_cell(linha_alvo, 8, texto_obs)

            print(
                f"Checkout realizado para o veículo ID {id_veiculo} na linha {linha_alvo}."
            )
        else:
            print("Nenhum check-in em aberto encontrado para este veículo.")


# --- TESTE DE CONEXÃO ---
# Este código só roda se apertar o Play neste arquivo diretamente
if __name__ == "__main__":
    banco = ControleFrota()
    print(
        "Sucesso! A ponte com o Google Sheets está funcionando e todas as funções foram convertidas!"
    )
