from tkinter import Tk, Frame, Label, Button, Canvas, StringVar, TOP, BOTTOM, LEFT, X, BOTH, SUNKEN, W, colorchooser


class JanelaPaint:
    # View: Contém apenas a estrutura de layouts e declaração de componentes visuais
    def __init__(self):
        self.root = Tk()
        self.root.title("Desenhos Geométricos Coloridos - MVC")

        self.tipo_figura_var = StringVar(self.root, value="retangulo")
        self.cor_borda_var = StringVar(self.root, value="black")
        self.cor_preenchimento_var = StringVar(self.root, value="white")

        self._criar_painel()
        self._criar_status()
        self._criar_canvas()

    def _criar_painel(self):
        painel = Frame(self.root, bd=2, relief=SUNKEN)
        painel.pack(side=TOP, fill=X, padx=5, pady=5)

        Label(painel, text="Formas:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        for texto, chave in [("Retângulo", "retangulo"), ("Oval", "oval"), ("Círculo", "circulo"), ("Linha", "linha"), ("Mão Livre", "maolivre"), ("Borracha", "borracha")]:
            Button(painel, text=texto, command=lambda c=chave: self.tipo_figura_var.set(c), bg="lightgray").pack(side=LEFT, padx=2)

        Label(painel, text="  |  Cor Borda/Linha:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        for nome, cor in [("Preto", "black"), ("Vermelho", "red"), ("Verde", "green"), ("Azul", "blue"), ("Laranja", "orange"), ("Roxo", "purple")]:
            fg_color = "black" if cor in ["orange"] else "white"
            Button(painel, text=nome, fg=fg_color, bg=cor, command=lambda c=cor: self.cor_borda_var.set(c)).pack(side=LEFT, padx=2)
        Button(painel, text="Outra...", bg="lightgray", command=self.selecionar_cor_borda_personalizada).pack(side=LEFT, padx=2)

        Label(painel, text="  |  Preenchimento:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        Button(painel, text="Nenhum", bg="white", command=lambda: self.cor_preenchimento_var.set("")).pack(side=LEFT, padx=2)
        for nome, cor in [("Amarelo", "yellow"), ("Rosa", "pink"), ("Ciano", "cyan"), ("Branco", "white"), ("Cinza", "gray"), ("Marrom", "brown")]:
            fg_color = "black" if cor in ["yellow", "pink", "cyan", "white"] else "white"
            Button(painel, text=nome, fg=fg_color, bg=cor, command=lambda c=cor: self.cor_preenchimento_var.set(c)).pack(side=LEFT, padx=2)
        Button(painel, text="Outra...", bg="lightgray", command=self.selecionar_cor_preenchimento_personalizada).pack(side=LEFT, padx=2)

        # Ações
        Label(painel, text="  |  Ações:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        self.btn_desfazer = Button(painel, text="Desfazer", bg="lightgray")
        self.btn_desfazer.pack(side=LEFT, padx=2)
        self.btn_limpar = Button(painel, text="Limpar Tudo", bg="lightgray")
        self.btn_limpar.pack(side=LEFT, padx=2)

    def _criar_status(self):
        self.lbl_status = Label(self.root, text="", bd=1, relief=SUNKEN, anchor=W, font=("Arial", 9, "italic"))
        self.lbl_status.pack(side=BOTTOM, fill=X)

    def _criar_canvas(self):
        self.canvas = Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=BOTH, expand=True)

    def atualiza_status(self, texto):
        self.lbl_status.config(text=texto)

    # Abre a janelinha do sistema para escolher uma cor de contorno/linha personalizada
    def selecionar_cor_borda_personalizada(self):
        cor = colorchooser.askcolor(title="Escolha a cor da Borda/Linha", parent=self.root)
        if cor[1]:  # se o usuario nao cancelar e escolher uma cor valida
            self.cor_borda_var.set(cor[1])  # atualiza a cor de borda selecionada

    # Abre a janelinha do sistema para escolher uma cor de preenchimento personalizada
    def selecionar_cor_preenchimento_personalizada(self):
        cor = colorchooser.askcolor(title="Escolha a cor do Preenchimento", parent=self.root)
        if cor[1]:  # se o usuario nao cancelar e escolher uma cor valida
            self.cor_preenchimento_var.set(cor[1])  # atualiza a cor de preenchimento