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
        botao = ctk.CTkButton(self.frame_principal, text="+ Nova Demanda")

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
        valor_livres = ctk.CTkLabel(
            self.card_livres,
            text="12",
            font=("Arial", 32, "bold"),
            text_color="#2ecc71",
        )  # Verde
        valor_livres.pack(pady=(0, 15))

        # --- CARD 2: EM ROTA ---
        self.card_livres = ctk.CTkFrame(self.frame_cards, corner_radius=8)
        self.card_livres.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Título do card
        titulo_livres = ctk.CTkLabel(
            self.card_livres, text="EM ROTA", font=("Arial", 12)
        )
        titulo_livres.pack(pady=(15, 5))

        # Número Gigante
        valor_livres = ctk.CTkLabel(
            self.card_livres,
            text="12",
            font=("Arial", 32, "bold"),
            text_color="#284eee",
        )
        valor_livres.pack(pady=(0, 15))

        # CARD 3: DEMANDAS PENDENTES ---
        self.card_livres = ctk.CTkFrame(self.frame_cards, corner_radius=8)
        self.card_livres.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Título do card
        titulo_livres = ctk.CTkLabel(
            self.card_livres, text="DEMANDAS PENDENTES", font=("Arial", 12)
        )
        titulo_livres.pack(pady=(15, 5))

        # Número Gigante
        valor_livres = ctk.CTkLabel(
            self.card_livres,
            text="12",
            font=("Arial", 32, "bold"),
            text_color="#ffc637",
        )
        valor_livres.pack(pady=(0, 15))

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
        cabecalho_horario = ctk.CTkLabel(
            self.frame_tabela,
            text="TIPO",
            font=("Arial", 12, "bold"),
            text_color="#00d2ff",
        )
        cabecalho_horario.grid(row=1, column=1, padx=15, pady=5, sticky="w")

        # Cabeçalho ORIGEM em AZUL/CIANO
        cabecalho_horario = ctk.CTkLabel(
            self.frame_tabela,
            text="ORIGEM",
            font=("Arial", 12, "bold"),
            text_color="#00d2ff",
        )
        cabecalho_horario.grid(row=1, column=2, padx=15, pady=5, sticky="w")

        # Cabeçalho STATUS em AZUL/CIANO
        cabecalho_horario = ctk.CTkLabel(
            self.frame_tabela,
            text="STATUS",
            font=("Arial", 12, "bold"),
            text_color="#00d2ff",
        )
        cabecalho_horario.grid(row=1, column=3, padx=15, pady=5, sticky="w")

        # --- DADOS DA TABELA ---

        # Dado do horário que fica debaixo do cabeçalho
        dado_horario = ctk.CTkLabel(
            self.frame_tabela, text="HORÁRIO: 10:30", font=("Arial", 12)
        )
        dado_horario.grid(row=2, column=0, padx=15, pady=10, sticky="w")

        # Dado do tipo que fica debaixo do cabeçalho
        dado_tipo = ctk.CTkLabel(
            self.frame_tabela, text="TIPO: COLETA DE DOAÇÃO", font=("Arial", 12)
        )
        dado_tipo.grid(row=2, column=1, padx=15, pady=10, sticky="w")

        # Dado do origem que fica debaixo do cabeçalho
        dado_origem = ctk.CTkLabel(
            self.frame_tabela, text="ORIGEM: MERCADO/SEDE X", font=("Arial", 12)
        )
        dado_origem.grid(row=2, column=2, padx=15, pady=10, sticky="w")

        # Dado do status que fica debaixo do cabeçalho
        dado_status = ctk.CTkLabel(
            self.frame_tabela,
            text="STATUS: CONCLUIDO",
            font=("Arial", 12),
        )
        dado_status.grid(row=2, column=3, padx=15, pady=10, sticky="w")


if __name__ == "__main__":
    app = DashboardOng()
    app.mainloop()
