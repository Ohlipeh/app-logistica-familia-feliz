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

    def _gerar_novo_id(self, aba):
        # Busca todas as linhas da planilha
        registros = aba.get_all_values()

        # Se a planilha só tiver o cabeçalho (1 linha), o primeiro ID será 1
        if len(registros) <= 1:
            return 1

        # Vai à última linha preenchida, pega o número da coluna A (índice 0) e soma 1
        try:
            ultimo_id = int(registros[-1][0])
            return ultimo_id + 1
        except ValueError:
            # Proteção caso a célula esteja vazia ou com texto
            return len(registros)

    def cadastrar_demanda(
        self, data_horario, descricao, pessoa, origem, destino, veiculo, acolhido
    ):
        novo_id = self._gerar_novo_id(self.aba_demandas)
        status = "Pendente"
        # Segue exatamente a nova ordem das colunas (A até I)
        # O status entra automaticamente como "Pendente" na coluna I
        nova_linha = [
            novo_id,
            data_horario,
            descricao,
            pessoa,
            origem,
            destino,
            veiculo,
            status,
            acolhido,
        ]

        self.aba_demandas.append_row(nova_linha)
        print(f"Demanda {novo_id} adicionada com sucesso para {pessoa}.")

    def buscar_locais_historico(self):
        # Lê todas as demandas e extrai Origem (coluna 4) e Destino (coluna 5) sem repetir
        try:
            registros = self.aba_demandas.get_all_values()[1:]  # Pula o cabeçalho
            locais = set()
            for linha in registros:
                if len(linha) >= 6:
                    if linha[4].strip():
                        locais.add(linha[4].strip())
                    if linha[5].strip():
                        locais.add(linha[5].strip())
            return sorted(list(locais))
        except Exception:
            return []

    # --- Função para buscar a demanda ---

    def buscar_demandas_recentes(self):
        # Pega todos os dados da aba e ignora a linha 1 (cabeçalhos)
        registros = self.aba_demandas.get_all_values()[1:]

        resultados = []
        for linha in registros:
            # Retorna a linha completa para a tela ter acesso a tudo (incluindo Status e Acolhido)
            resultados.append(linha)

        # Inverte a lista (mais recentes primeiro) e pega só os 5 primeiros
        resultados.reverse()
        return resultados[:5]

    # --- Função para atualizar o status da demanda ---
    def atualizar_status_demanda(self, id_demanda, novo_status):
        celula = self.aba_demandas.find(str(id_demanda), in_column=1)
        if celula:
            # Atualiza a coluna 8 (H) que é o verdadeiro Status
            self.aba_demandas.update_cell(celula.row, 8, novo_status)

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

        livres = sum(1 for v in veiculos if len(v) > 4 and v[4] == "Livre")
        em_rota = sum(1 for v in veiculos if len(v) > 4 and v[4] == "Em Rota")

        # O Status da demanda agora é o índice 7 (coluna 8)
        pendentes = sum(1 for d in demandas if len(d) > 7 and d[7] == "Pendente")

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

    # --- Função para atualizar o status do veiculo ---
    def atualizar_status_veiculo(self, id_veiculo, novo_status):
        celula = self.aba_veiculos.find(str(id_veiculo), in_column=1)
        if celula:
            # A coluna de status dos veículos é a 5 (E)
            self.aba_veiculos.update_cell(celula.row, 5, novo_status)

    # --- Função para excluir o veiculo ---
    def excluir_veiculo(self, id_veiculo):
        celula = self.aba_veiculos.find(str(id_veiculo), in_column=1)
        if celula:
            self.aba_veiculos.delete_rows(celula.row)
            print(f"Veiculo ID {id_veiculo} excluído com sucesso.")

    # --- Função para realizar Check-in ---
    def realizar_checkin(self, id_motorista, id_veiculo, km_inicial):
        data = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Pega o último ID usando a função protegida
        novo_id = self._gerar_novo_id(self.aba_checkin)

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
        for index, linha in reversed(list(enumerate(registros))):
            if index > 0:
                # PREVENÇÃO DE ERRO: Garante que a linha tem 8 espaços, mesmo se o Sheets ocultar os vazios
                linha = list(linha)
                while len(linha) < 8:
                    linha.append("")

                # str(linha[2]) é o ID do carro, linha[5] é a data de devolução vazia
                if str(linha[2]) == str(id_veiculo) and linha[5] == "":
                    linha_alvo = index + 1
                    break

        if linha_alvo:
            self.aba_checkin.update_cell(linha_alvo, 6, data)
            self.aba_checkin.update_cell(linha_alvo, 7, km_final)

            texto_obs = str(observacoes) if observacoes else "Sem observações"
            self.aba_checkin.update_cell(linha_alvo, 8, texto_obs)

            # Libera o veículo para voltar ao painel de Livres
            self.atualizar_status_veiculo(id_veiculo, "Livre")
            print(f"Checkout realizado na linha {linha_alvo}.")
        else:
            print("Nenhum check-in em aberto encontrado para este veículo.")


# --- TESTE DE CONEXÃO ---
# Este código só roda se apertar o Play neste arquivo diretamente
if __name__ == "__main__":
    banco = ControleFrota()
    print(
        "Sucesso! A ponte com o Google Sheets está funcionando e todas as funções foram convertidas!"
    )
