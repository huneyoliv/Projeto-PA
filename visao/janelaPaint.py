from tkinter import Tk, Frame, Label, Button, Canvas, StringVar, TOP, BOTTOM, LEFT, X, BOTH, SUNKEN, W


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
        for texto, chave in [("Retângulo", "retangulo"), ("Oval", "oval"), ("Círculo", "circulo"), ("Borracha", "borracha")]:
            Button(painel, text=texto, command=lambda c=chave: self.tipo_figura_var.set(c), bg="lightgray").pack(side=LEFT, padx=2)

        Label(painel, text="  |  Cor Borda/Linha:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        for nome, cor in [("Preto", "black"), ("Vermelho", "red"), ("Verde", "green"), ("Azul", "blue")]:
            Button(painel, text=nome, fg="white", bg=cor, command=lambda c=cor: self.cor_borda_var.set(c)).pack(side=LEFT, padx=2)

        Label(painel, text="  |  Preenchimento:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        Button(painel, text="Nenhum", bg="white", command=lambda: self.cor_preenchimento_var.set("")).pack(side=LEFT, padx=2)
        for nome, cor in [("Amarelo", "yellow"), ("Rosa", "pink"), ("Ciano", "cyan"), ("Branco", "white")]:
            Button(painel, text=nome, bg=cor, command=lambda c=cor: self.cor_preenchimento_var.set(c)).pack(side=LEFT, padx=2)

    def _criar_status(self):
        self.lbl_status = Label(self.root, text="", bd=1, relief=SUNKEN, anchor=W, font=("Arial", 9, "italic"))
        self.lbl_status.pack(side=BOTTOM, fill=X)

    def _criar_canvas(self):
        self.canvas = Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=BOTH, expand=True)

    def update(self):
        self.root.update()

    def atualiza_status(self, texto):
        self.lbl_status.config(text=texto)
