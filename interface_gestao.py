import customtkinter as ctk

from interface.tela_frota import TelaFrota
from interface.tela_dashboard import TelaDashboard

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
        self.mostrar_tela_dashboard()

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

        # Criação do botão "Visão Geral"
        botao = ctk.CTkButton(
            self.frame_menu,
            text="Visão Geral",
            anchor="w",  # Alinha o texto à esquerda (West)
            fg_color="transparent",
            command=self.mostrar_tela_dashboard,  # Tira o fundo para parecer um item de menu
        )
        # Mantem apenas o grid, usando pady para dar espaçamento
        botao.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Criação do botão "Frota"
        botao = ctk.CTkButton(
            self.frame_menu,
            text="Frota",
            anchor="w",  # Alinha o texto à esquerda (West)
            fg_color="transparent",  # Tira o fundo para parecer um item de menu
            command=self.mostrar_tela_frota,
        )
        # Mantem apenas o grid, usando pady para dar espaçamento
        botao.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    def limpar_tela(self):
        # Se já existir o lado direito desenhado, destruo para limpar o espaço
        if hasattr(self, "frame_principal"):
            self.frame_principal.destroy()

    def mostrar_tela_dashboard(self):
        self.limpar_tela()

        # Instancia a nova classe do Dashboard passando a janela e o banco
        self.frame_principal = TelaDashboard(self, sistema=self.sistema)
        self.frame_principal.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def mostrar_tela_frota(self):
        self.limpar_tela()  # Apaga o dashboard

        # Instancia a nova classe passando a própria janela (self) e o banco (self.sistema)
        self.frame_principal = TelaFrota(self, sistema=self.sistema)

        # Posiciona a tela de frota no lado direito
        self.frame_principal.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")


if __name__ == "__main__":
    app = DashboardOng()
    app.mainloop()
