from tkinter import Frame, Label, Button, Canvas, TOP, BOTTOM, LEFT, X, BOTH, SUNKEN, W


class Interface:
    # Gerencia a criação e disposição dos elementos visuais da interface
    def __init__(self, root, ao_mudar_ferramenta, ao_mudar_borda, ao_mudar_preenchimento,
                 ao_clicar, ao_arrastar, ao_soltar, ao_mover, ao_sair):
        self._criar_painel(root, ao_mudar_ferramenta, ao_mudar_borda, ao_mudar_preenchimento)
        self._criar_status(root)
        self._criar_canvas(root, ao_clicar, ao_arrastar, ao_soltar, ao_mover, ao_sair)

    def _criar_painel(self, root, ao_mudar_ferramenta, ao_mudar_borda, ao_mudar_preenchimento):
        # Cria a barra superior de botões de controle
        painel = Frame(root, bd=2, relief=SUNKEN)
        painel.pack(side=TOP, fill=X, padx=5, pady=5)

        Label(painel, text="Formas:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        for texto, chave in [("Retângulo", "retangulo"), ("Oval", "oval"), ("Círculo", "circulo"), ("Linha", "linha"), ("Rabisco", "rabisco"), ("Borracha", "borracha")]:
            Button(painel, text=texto, command=lambda c=chave: ao_mudar_ferramenta(c), bg="lightgray").pack(side=LEFT, padx=2)

        Label(painel, text="  |  Cor Borda/Linha:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        for nome, cor in [("Preto", "black"), ("Vermelho", "red"), ("Verde", "green"), ("Azul", "blue")]:
            Button(painel, text=nome, fg="white", bg=cor, command=lambda c=cor: ao_mudar_borda(c)).pack(side=LEFT, padx=2)

        Label(painel, text="  |  Preenchimento:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        Button(painel, text="Nenhum", bg="white", command=lambda: ao_mudar_preenchimento("")).pack(side=LEFT, padx=2)
        for nome, cor in [("Amarelo", "yellow"), ("Rosa", "pink"), ("Ciano", "cyan"), ("Branco", "white")]:
            Button(painel, text=nome, bg=cor, command=lambda c=cor: ao_mudar_preenchimento(c)).pack(side=LEFT, padx=2)

    def _criar_status(self, root):
        # Barra inferior de status
        self.lbl_status = Label(root, text="", bd=1, relief=SUNKEN, anchor=W, font=("Arial", 9, "italic"))
        self.lbl_status.pack(side=BOTTOM, fill=X)

    def _criar_canvas(self, root, ao_clicar, ao_arrastar, ao_soltar, ao_mover, ao_sair):
        # Área de desenho interativa com binds adicionais de movimento
        self.canvas = Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind('<ButtonPress-1>', ao_clicar)
        self.canvas.bind('<B1-Motion>', ao_arrastar)
        self.canvas.bind('<ButtonRelease-1>', ao_soltar)
        self.canvas.bind('<Motion>', ao_mover)
        self.canvas.bind('<Leave>', ao_sair)

    def atualiza_status(self, texto):
        self.lbl_status.config(text=texto)
