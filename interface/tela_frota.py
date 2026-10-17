import customtkinter as ctk


# A nossa nova classe herda (é filha) de ctk.CTkFrame
class TelaFrota(ctk.CTkFrame):
    def __init__(self, master, sistema):
        # O 'master' é quem vai segurar esta tela (a janela principal)
        super().__init__(master, corner_radius=10)

        # Guardo a conexão com o banco de dados
        self.sistema = sistema

        # Configura a coluna 0 para expandir
        self.grid_columnconfigure(0, weight=1)

        # Chama a função para desenhar tudo
        self.desenhar_tela()

    def desenhar_tela(self):
        # Título da página
        titulo = ctk.CTkLabel(self, text="GESTÃO DA FROTA", font=("Arial", 20, "bold"))
        titulo.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Botão de Novo Veículo
        botao_novo_veiculo = ctk.CTkButton(
            self, text="+ Novo Veículo", command=self.abrir_tela_novo_veiculo
        )
        botao_novo_veiculo.grid(row=0, column=0, padx=20, pady=20, sticky="e")

        # --- TABELA DE VEÍCULOS ---
        self.frame_tabela_frota = ctk.CTkFrame(self, corner_radius=10)
        self.frame_tabela_frota.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_tabela_frota.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Cabeçalhos da Tabela
        ctk.CTkLabel(
            self.frame_tabela_frota,
            text="PLACA",
            font=("Arial", 12, "bold"),
            text_color="#00d2ff",
        ).grid(row=0, column=0, padx=15, pady=10, sticky="w")
        ctk.CTkLabel(
            self.frame_tabela_frota,
            text="MODELO",
            font=("Arial", 12, "bold"),
            text_color="#00d2ff",
        ).grid(row=0, column=1, padx=15, pady=10, sticky="w")
        ctk.CTkLabel(
            self.frame_tabela_frota,
            text="KM ATUAL",
            font=("Arial", 12, "bold"),
            text_color="#00d2ff",
        ).grid(row=0, column=2, padx=15, pady=10, sticky="w")
        ctk.CTkLabel(
            self.frame_tabela_frota,
            text="STATUS",
            font=("Arial", 12, "bold"),
            text_color="#00d2ff",
        ).grid(row=0, column=3, padx=15, pady=10, sticky="w")

        self.atualizar_tabela_veiculos()

    def atualizar_tabela_veiculos(self):
        # 1. Limpa os dados antigos (se existirem), exceto o cabeçalho (row=0)
        for widget in self.frame_tabela_frota.winfo_children():
            info = widget.grid_info()
            if info and info.get("row", 0) >= 1:
                widget.destroy()

        # 2. Busca os dados no banco
        veiculos = self.sistema.buscar_veiculos()

        # 3. Desenha as linhas
        for index, veiculo in enumerate(veiculos):
            linha = index + 1  # Começa na row=1

            id_veic = veiculo[0]
            placa = veiculo[1]
            modelo = veiculo[2]
            km = veiculo[3]
            status = veiculo[4]

            # Define a cor do status (Verde para Livre, Azul para Em Rota)
            cor_status = "#2ecc71" if status == "Livre" else "#284eee"

            ctk.CTkLabel(self.frame_tabela_frota, text=placa, font=("Arial", 12)).grid(
                row=linha, column=0, padx=15, pady=10, sticky="w"
            )
            ctk.CTkLabel(self.frame_tabela_frota, text=modelo, font=("Arial", 12)).grid(
                row=linha, column=1, padx=15, pady=10, sticky="w"
            )
            ctk.CTkLabel(
                self.frame_tabela_frota, text=f"{km} km", font=("Arial", 12)
            ).grid(row=linha, column=2, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(
                self.frame_tabela_frota,
                text=status,
                font=("Arial", 12, "bold"),
                text_color=cor_status,
            ).grid(row=linha, column=3, padx=15, pady=10, sticky="w")

            # Mudança coluna de Status
            frame_status = ctk.CTkFrame(self.frame_tabela_frota, fg_color="transparent")
            frame_status.grid(row=linha, column=3, padx=15, pady=10, sticky="w")

            # 1. Coloco o texto do status dentro do miniframe
            ctk.CTkLabel(
                frame_status,
                text=status,
                font=("Arial", 12, "bold"),
                text_color=cor_status,
            ).pack(side="left")

            # 2. Cria o botão vermelho dentro do miniframe
            botao_excluir = ctk.CTkButton(
                frame_status,
                text="Excluir",
                width=45,
                height=20,
                fg_color="#e74c3c",
                hover_color="#c0392b",
                command=lambda v=id_veic: self.deletar_veiculo(v),
            )
            botao_excluir.pack(side="left", padx=10)

    def abrir_tela_novo_veiculo(self):
        janela_veiculo = ctk.CTkToplevel(self)
        janela_veiculo.title("Cadastrar Novo Veículo")
        janela_veiculo.geometry("500x350")
        janela_veiculo.grab_set()

        titulo = ctk.CTkLabel(
            janela_veiculo, text="CADASTRAR VEÍCULO", font=("Arial", 16, "bold")
        )
        titulo.pack(pady=20)

        # Campo registro de veiculo "Placa"
        entrada_placa = ctk.CTkEntry(
            janela_veiculo, placeholder_text="Placa", width=400
        )
        entrada_placa.pack(pady=10)

        # Campo registro de veiculo "Modelo"
        entrada_modelo = ctk.CTkEntry(
            janela_veiculo, placeholder_text="Modelo", width=400
        )
        entrada_modelo.pack(pady=10)

        # Campo registro de veiculo "Km Atual"
        entrada_km_atual = ctk.CTkEntry(
            janela_veiculo, placeholder_text="Km Atual", width=400
        )
        entrada_km_atual.pack(pady=10)

        def salvar_carro():
            # Pega os valores que estão escritos nos campos
            plac = entrada_placa.get()
            mod = entrada_modelo.get()
            km = entrada_km_atual.get()

            self.sistema.cadastrar_veiculo(placa=plac, modelo=mod, km_atual=km)
            self.atualizar_tabela_veiculos()

            janela_veiculo.destroy()

        # --- Botões ---
        frame_botoes = ctk.CTkFrame(janela_veiculo, fg_color="transparent")
        frame_botoes.pack(pady=15)

        # Botão Cadastrar
        botao_cadastrar_veiculo = ctk.CTkButton(
            frame_botoes, text="Cadastrar Veiculo", command=salvar_carro
        )
        botao_cadastrar_veiculo.pack(side="left", padx=5)

        # Botão Cancelar
        botao_voltar = ctk.CTkButton(
            frame_botoes, text="Cancelar", command=janela_veiculo.destroy
        )
        botao_voltar.pack(side="left", padx=5)

    def deletar_veiculo(self, id_veiculo):
        # 1. Pede ao banco para apagar
        self.sistema.excluir_veiculo(id_veiculo)

        # 2. Atualiza a tabela e os números do Veiculos
        self.atualizar_tabela_veiculos()
