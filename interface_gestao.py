import customtkinter as ctk

# Importação da classe do backend para usar depois
from database.repositorio import ControleFrota

# Configuração visual padrão (Dark Mode)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DashboardOng(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Inicia a conexão com o banco
        self.sistema = ControleFrota()

        # Configurações da Janela Principal
        self.title("Sistema ONG - Painel de Gestão")
        self.geometry("1024x720")

        # Cria um grid para dividir a tela: Coluna 0 (Menu) e Coluna 1 (Conteúdo)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_menu_lateral()
        self.criar_area_principal()

    def criar_menu_lateral(self):
        # Frame do menu (lado esquerdo)
        self.frame_menu = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nsew")
        self.frame_menu.grid_rowconfigure(5, weight=1)

        # Prende o Label diretamente no self.frame_menu
        label_titulo = ctk.CTkLabel(
            self.frame_menu, text="SISTEMA ONG", font=("Arial", 20, "bold")
        )
        # Usa o grid para manter o padrão de layout e posicionar no topo
        label_titulo.grid(row=0, column=0, padx=20, pady=(30, 20))

        # Criação do botão
        botao = ctk.CTkButton(
            self.frame_menu,
            text="Visão Geral",
            anchor="w",  # Alinha o texto à esquerda (West)
            fg_color="transparent",  # Tira o fundo para parecer um item de menu
        )
        # Mantem apenas o grid, usando pady para dar espaçamento
        botao.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

    def criar_area_principal(self):
        # Frame do conteúdo (lado direito)
        self.frame_principal = ctk.CTkFrame(self, corner_radius=10)
        self.frame_principal.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Avisa a coluna 0 deste frame para expandir e ocupar todo o espaço disponível
        self.frame_principal.grid_columnconfigure(0, weight=1)

        # Criação do Botão +Nova Demanda (tirei o transparente para ficar azul igual ao Figma)
        botao = ctk.CTkButton(
            self.frame_principal,
            text="+ Nova Demanda",
            command=self.abrir_tela_nova_demanda,
        )

        # Aqui uso o 'e' (East/Direita) ou 'ne' (Topo-Direita) dentro do grid
        botao.grid(row=0, column=0, padx=20, pady=20, sticky="e")

        # 1. Cria um Frame Container invisível (fg_color="transparent") para segurar os cards
        self.frame_cards = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        # Coloca na linha 1 (abaixo do botão que está na linha 0) e alinhado à esquerda e direita (ew)
        self.frame_cards.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # 2. Configura as 3 colunas do container para terem o mesmo tamanho (weight=1)
        self.frame_cards.grid_columnconfigure((0, 1, 2), weight=1)

        # --- CARD 1: VEÍCULOS LIVRES ---
        # Cria a caixinha com borda e cor de fundo
        self.card_livres = ctk.CTkFrame(self.frame_cards, corner_radius=8)
        self.card_livres.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Título do Card
        titulo_livres = ctk.CTkLabel(
            self.card_livres, text="VEÍCULOS LIVRES", font=("Arial", 12)
        )
        titulo_livres.pack(
            pady=(15, 5)
        )  # Pack aqui é ok porque é só um texto empilhado no outro dentro do card

        # Número Gigante
        self.label_valor_livres = ctk.CTkLabel(
            self.card_livres,
            text="12",
            font=("Arial", 32, "bold"),
            text_color="#2ecc71",
        )  # Verde
        self.label_valor_livres.pack(pady=(0, 15))

        # --- CARD 2: EM ROTA ---
        self.valor_em_rota = ctk.CTkFrame(self.frame_cards, corner_radius=8)
        self.valor_em_rota.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Título do card
        titulo_livres = ctk.CTkLabel(
            self.valor_em_rota, text="EM ROTA", font=("Arial", 12)
        )
        titulo_livres.pack(pady=(15, 5))

        # Número Gigante
        self.label_valor_em_rota = ctk.CTkLabel(
            self.valor_em_rota,
            text="12",
            font=("Arial", 32, "bold"),
            text_color="#284eee",
        )
        self.label_valor_em_rota.pack(pady=(0, 15))

        # CARD 3: DEMANDAS PENDENTES ---
        self.valor_pendente = ctk.CTkFrame(self.frame_cards, corner_radius=8)
        self.valor_pendente.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Título do card
        titulo_livres = ctk.CTkLabel(
            self.valor_pendente, text="DEMANDAS PENDENTES", font=("Arial", 12)
        )
        titulo_livres.pack(pady=(15, 5))

        # Número Gigante
        self.label_valor_pendentes = ctk.CTkLabel(
            self.valor_pendente,
            text="12",
            font=("Arial", 32, "bold"),
            text_color="#ffc637",
        )
        self.label_valor_pendentes.pack(pady=(0, 15))

        # 1. Cria o Frame principal da tabela (uso cor de fundo para ficar igual ao Figma)
        self.frame_tabela = ctk.CTkFrame(self.frame_principal, corner_radius=10)
        self.frame_tabela.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        # Configura as 4 colunas do container para terem o mesmo espaço (weight=1)
        self.frame_tabela.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Título Geral da secção que aparece no seu print
        titulo_tabela = ctk.CTkLabel(
            self.frame_tabela, text="ATIVIDADES DO DIA", font=("Arial", 16, "bold")
        )
        titulo_tabela.grid(
            row=0, column=0, columnspan=4, padx=15, pady=(15, 10), sticky="w"
        )

        # --- CABEÇALHOS ---

        # Cabeçalho HORÁRIO em AZUL/CIANO
        cabecalho_horario = ctk.CTkLabel(
            self.frame_tabela,
            text="HORÁRIO",
            font=("Arial", 12, "bold"),
            text_color="#00d2ff",  # Aqui define a cor azul
        )
        cabecalho_horario.grid(row=1, column=0, padx=15, pady=5, sticky="w")

        # Cabeçalho TIPO em AZUL/CIANO
        cabecalho_tipo = ctk.CTkLabel(
            self.frame_tabela,
            text="TIPO",
            font=("Arial", 12, "bold"),
            text_color="#00d2ff",
        )
        cabecalho_tipo.grid(row=1, column=1, padx=15, pady=5, sticky="w")

        # Cabeçalho ORIGEM em AZUL/CIANO
        cabecalho_origem = ctk.CTkLabel(
            self.frame_tabela,
            text="ORIGEM",
            font=("Arial", 12, "bold"),
            text_color="#00d2ff",
        )
        cabecalho_origem.grid(row=1, column=2, padx=15, pady=5, sticky="w")

        # Cabeçalho STATUS em AZUL/CIANO
        cabecalho_status = ctk.CTkLabel(
            self.frame_tabela,
            text="STATUS",
            font=("Arial", 12, "bold"),
            text_color="#00d2ff",
        )
        cabecalho_status.grid(row=1, column=3, padx=15, pady=5, sticky="w")
        self.atualizar_tabela_demandas()
        self.atualizar_cards_resumo()

    def atualizar_tabela_demandas(self):
        # 1. Limpa os dados antigos da tabela, exceto os cabeçalhos que estão nas linhas 0 e 1
        for widget in self.frame_tabela.winfo_children():
            info = widget.grid_info()
            # Se o elemento estiver da linha 2 para baixo, apago para redesenhar
            if info and info.get("row", 0) >= 2:
                widget.destroy()

        # 2. Puxa os dados reais do banco
        demandas = self.sistema.buscar_demandas_recentes()

        # 3. Cria uma linha na tela para cada demanda encontrada no banco
        for index, demanda in enumerate(demandas):
            linha_atual = index + 2

            # Os índices mudaram porque agora o demanda[0] é a Chave Primária (id_demanda)
            id_dem = demanda[0]
            data_crua = demanda[1]
            tipo = demanda[2]
            origem = demanda[3]
            status = demanda[4]

            horario = data_crua.split(" ")[1][:5] if " " in data_crua else data_crua

            # Desenha as 3 primeiras colunas normalmente
            ctk.CTkLabel(
                self.frame_tabela, text=f"HORÁRIO: {horario}", font=("Arial", 12)
            ).grid(row=linha_atual, column=0, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(
                self.frame_tabela, text=f"TIPO: {tipo}", font=("Arial", 12)
            ).grid(row=linha_atual, column=1, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(
                self.frame_tabela, text=f"ORIGEM: {origem}", font=("Arial", 12)
            ).grid(row=linha_atual, column=2, padx=15, pady=10, sticky="w")

            # miniframe invisível só para deixar o texto e o botão lado a lado
            frame_status = ctk.CTkFrame(self.frame_tabela, fg_color="transparent")
            frame_status.grid(row=linha_atual, column=3, padx=15, pady=10, sticky="w")

            ctk.CTkLabel(
                frame_status, text=f"STATUS: {status}", font=("Arial", 12)
            ).pack(side="left")

            # Se a demanda estiver pendente, cria um botão verde de 'Concluir'
            if status == "Pendente":
                # O comando lambda garante que o botão saiba exatamente qual é o ID daquela linha
                botao_concluir = ctk.CTkButton(
                    frame_status,
                    text="✔",
                    width=30,
                    height=24,
                    fg_color="#2ecc71",
                    hover_color="#27ae60",
                    command=lambda d=id_dem: self.concluir_demanda(d),
                )
                botao_concluir.pack(side="left", padx=10)

    def atualizar_cards_resumo(self):
        # 1. Vai buscar os três números ao banco de dados
        livres, em_rota, pendentes = self.sistema.obter_resumo_dashboard()

        # 2. Atualiza os textos na tela convertendo os números (int) para texto (str)
        self.label_valor_livres.configure(text=str(livres))
        self.label_valor_em_rota.configure(text=str(em_rota))
        self.label_valor_pendentes.configure(text=str(pendentes))

    def concluir_demanda(self, id_demanda):
        # 1. Avisa o banco para mudar o status para 'Concluído'
        self.sistema.atualizar_status_demanda(id_demanda, "Concluído")

        # 2. Atualiza a tabela para o utilizador ver a mudança na hora!
        self.atualizar_tabela_demandas()
        self.atualizar_cards_resumo()

    def abrir_tela_nova_demanda(self):
        # 1. Cria a janela flutuante
        janela_demanda = ctk.CTkToplevel(self)
        janela_demanda.title("Cadastrar Nova Demanda")
        janela_demanda.geometry("600x400")

        # Faz com que a janela principal fique bloqueada enquanto esta estiver aberta (opcional, mas recomendado)
        janela_demanda.grab_set()

        # 2. Título da Janela
        titulo = ctk.CTkLabel(
            janela_demanda, text="CADASTRAR NOVA DEMANDA", font=("Arial", 16, "bold")
        )
        titulo.pack(pady=20)

        # 3. Campo Tipo de Demanda
        entrada_demanda = ctk.CTkComboBox(
            janela_demanda,
            values=["Coleta de Doação", "Cesta Básica", "Transporte Médico"],
            width=400,
        )
        entrada_demanda.pack(pady=10)

        # 4. Campo Endereço de Origem
        entrada_origem = ctk.CTkEntry(
            janela_demanda, placeholder_text="Endereço de Origem", width=400
        )
        entrada_origem.pack(pady=10)

        # Campo Endereço de Destino
        entrada_destino = ctk.CTkEntry(
            janela_demanda, placeholder_text="Endereço de Destino", width=400
        )
        entrada_destino.pack(pady=10)

        # Frame para os botões
        frame_botoes = ctk.CTkFrame(janela_demanda, fg_color="transparent")
        frame_botoes.pack(pady=10)

        # --- A FUNÇÃO QUE SALVA OS DADOS ---
        def salvar_no_banco():
            # 1. Pega os valores que estão escritos nas caixinhas
            tipo = entrada_demanda.get()
            orig = entrada_origem.get()
            dest = entrada_destino.get()

            # 2. Chama a função da classe ControleFrota
            self.sistema.cadastrar_demanda(tipo_demanda=tipo, origem=orig, destino=dest)
            self.atualizar_tabela_demandas()
            self.atualizar_cards_resumo()

            # 3. Fecha a janela flutuante
            janela_demanda.destroy()

        # --- BOTÕES ATUALIZADOS ---
        # Botão cadastrar (agora aponta para a função salvar_no_banco)
        botao_cadastrar_demanda = ctk.CTkButton(
            frame_botoes, text="Cadastrar Demanda", command=salvar_no_banco
        )
        botao_cadastrar_demanda.pack(side="left", padx=5)

        # Botão cancelar (continua apenas fechando a janela)
        botao_voltar = ctk.CTkButton(
            frame_botoes, text="Cancelar", command=janela_demanda.destroy
        )
        botao_voltar.pack(side="left", padx=5)


if __name__ == "__main__":
    app = DashboardOng()
    app.mainloop()
