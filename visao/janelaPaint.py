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
        # ADICIONADO: "Linha" na tupla abaixo
        for texto, chave in [("Retângulo", "retangulo"), ("Oval", "oval"), ("Círculo", "circulo"), ("Linha", "linha"), ("Borracha", "borracha")]:
            Button(painel, text=texto, command=lambda c=chave: self.tipo_figura_var.set(c), bg="lightgray").pack(side=LEFT, padx=2)

        Label(painel, text="  |  Cor Borda/Linha:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        for nome, cor in [("Preto", "black"), ("Vermelho", "red"), ("Verde", "green"), ("Azul", "blue")]:
            Button(painel, text=nome, fg="white", bg=cor, command=lambda c=cor: self.cor_borda_var.set(c)).pack(side=LEFT, padx=2)

        Label(painel, text="  |  Preenchimento:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        Button(painel, text="Nenhum", bg="white", command=lambda: self.cor_preenchimento_var.set("")).pack(side=LEFT, padx=2)
        for nome, cor in [("Amarelo", "yellow"), ("Rosa", "pink"), ("Ciano", "cyan"), ("Branco", "white")]:
            Button(painel, text=nome, bg=cor, command=lambda c=cor: self.cor_preenchimento_var.set(c)).pack(side=LEFT, padx=2)

        # ADICIONADO: Nova seção de comandos que o controlador vai assinar depois
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

    def update(self):
        self.root.update()

    def atualiza_status(self, texto):
        self.lbl_status.config(text=texto)

from tkinter import Tk, Frame, Label, Button, Canvas, StringVar, TOP, BOTTOM, LEFT, X, BOTH, SUNKEN, W

class JanelaPaint:
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

    def atualiza_status(self, texto):
        self.lbl_status.config(text=texto)

    # --- NOVO MÉTODO DA VISÃO ---
    def desenhar_figuras(self, lista_figuras, figura_temporaria=None):
        """Limpa o canvas e renderiza todas as figuras baseando-se nos dados do Modelo"""
        self.canvas.delete("all")
        
        # Junta as figuras salvas com a que está sendo arrastada no momento (se houver)
        todas_figuras = lista_figuras + ([figura_temporaria] if figura_temporaria else [])
        
        for fig in todas_figuras:
            nome_classe = fig.__class__.__name__.lower()
            
            # A visão decide COMO desenhar cada tipo de dados estruturado
            if nome_classe == "retangulo":
                self.canvas.create_rectangle(
                    fig.x_inicio, fig.y_inicio, fig.x_fim, fig.y_fim,
                    outline=fig.cor_borda, fill=fig.cor_preenchimento
                )
            elif nome_classe == "oval":
                self.canvas.create_oval(
                    fig.x_inicio, fig.y_inicio, fig.x_fim, fig.y_fim,
                    outline=fig.cor_borda, fill=fig.cor_preenchimento
                )
            elif nome_classe == "circulo":
                self.canvas.create_oval(
                    fig.x_inicio, fig.y_inicio, fig.x_fim, fig.y_fim,
                    outline=fig.cor_borda, fill=fig.cor_preenchimento
                )
                
    def iniciar(self):
        self.root.mainloop()
    # Caso o desenho seja feito via varredura de classes:
elif ferramenta == "linha":
    self.canvas.create_line(self.x_inicio, self.y_inicio, event.x, event.y, fill=bc, dash=(4, 2))