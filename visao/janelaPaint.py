from tkinter import Tk, Frame, Label, Button, Canvas, StringVar, TOP, BOTTOM, LEFT, X, BOTH, SUNKEN, W


class JanelaPaint:
    # View: Contém apenas a estrutura de layouts e declaração de componentes visuais
    def __init__(self):
        self.root = Tk()
        self.root.title("Desenhos Geométricos Coloridos - MVC")

        self.tipo_figura_var = StringVar(self.root, value="retangulo")
        self.cor_borda_var = StringVar(self.root, value="black")
        self.cor_preenchimento_var = StringVar(self.root, value="white")
        self.id_borracha_temp = None

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
        for nome, cor in [("Preto", "black"), ("Vermelho", "red"), ("Verde", "green"), ("Azul", "blue")]:
            Button(painel, text=nome, fg="white", bg=cor, command=lambda c=cor: self.cor_borda_var.set(c)).pack(side=LEFT, padx=2)

        Label(painel, text="  |  Preenchimento:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        Button(painel, text="Nenhum", bg="white", command=lambda: self.cor_preenchimento_var.set("")).pack(side=LEFT, padx=2)
        for nome, cor in [("Amarelo", "yellow"), ("Rosa", "pink"), ("Ciano", "cyan"), ("Branco", "white")]:
            Button(painel, text=nome, bg=cor, command=lambda c=cor: self.cor_preenchimento_var.set(c)).pack(side=LEFT, padx=2)

        # Ações — o controlador vai assinar os comandos depois
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

    def desenhar_figura(self, figura, dash=()):
        from modelo.retangulo import Retangulo
        from modelo.oval import Oval
        from modelo.circulo import Circulo
        from modelo.Linha import Linha
        from modelo.MaoLivre import MaoLivre

        if isinstance(figura, Retangulo):
            figura.id = self.canvas.create_rectangle(
                figura.x_inicio, figura.y_inicio, figura.x_fim, figura.y_fim,
                outline=figura.cor_borda, fill=figura.cor_preenchimento, dash=dash
            )
        elif isinstance(figura, Oval):
            figura.id = self.canvas.create_oval(
                figura.x_inicio, figura.y_inicio, figura.x_fim, figura.y_fim,
                outline=figura.cor_borda, fill=figura.cor_preenchimento, dash=dash
            )
        elif isinstance(figura, Circulo):
            figura.id = self.canvas.create_oval(
                figura.x_inicio - figura.raio, figura.y_inicio - figura.raio,
                figura.x_inicio + figura.raio, figura.y_inicio + figura.raio,
                outline=figura.cor_borda, fill=figura.cor_preenchimento, dash=dash
            )
        elif isinstance(figura, Linha):
            figura.id = self.canvas.create_line(
                figura.x_inicio, figura.y_inicio, figura.x_fim, figura.y_fim,
                fill=figura.cor, width=2, dash=dash
            )
        elif isinstance(figura, MaoLivre):
            if len(figura.pontos) > 1:
                coordenadas = []
                for x, y in figura.pontos:
                    coordenadas.extend([x, y])
                figura.id = self.canvas.create_line(
                    *coordenadas, fill=figura.cor, width=2, dash=dash
                )

    def atualizar_tela(self, desenho):
        self.canvas.delete("all")
        for figura in desenho.figuras:
            self.desenhar_figura(figura)

    def desenhar_preview_retangulo(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        self.canvas.create_rectangle(x1, y1, x2, y2, outline=cor_borda, fill=cor_preenchimento, dash=(4, 2))

    def desenhar_preview_oval(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        self.canvas.create_oval(x1, y1, x2, y2, outline=cor_borda, fill=cor_preenchimento, dash=(4, 2))

    def desenhar_preview_circulo(self, cx, cy, raio, cor_borda, cor_preenchimento):
        self.canvas.create_oval(cx - raio, cy - raio, cx + raio, cy + raio, outline=cor_borda, fill=cor_preenchimento, dash=(4, 2))

    def desenhar_preview_linha(self, x1, y1, x2, y2, cor_borda):
        self.canvas.create_line(x1, y1, x2, y2, fill=cor_borda, width=2, dash=(4, 2))

    def atualizar_indicador_borracha(self, x, y):
        r = 6
        if self.id_borracha_temp is None:
            self.id_borracha_temp = self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                outline="red", width=1, dash=(2, 2)
            )
        else:
            self.canvas.coords(self.id_borracha_temp, x - r, y - r, x + r, y + r)
            self.canvas.tag_raise(self.id_borracha_temp)

    def limpar_indicador_borracha(self):
        if self.id_borracha_temp is not None:
            self.canvas.delete(self.id_borracha_temp)
            self.id_borracha_temp = None

    def obter_figura_sob_cursor(self, x, y):
        itens = self.canvas.find_overlapping(x - 3, y - 3, x + 3, y + 3)
        if itens:
            id_para_remover = itens[-1]
            if id_para_remover == self.id_borracha_temp and len(itens) > 1:
                id_para_remover = itens[-2]
            if id_para_remover != self.id_borracha_temp:
                return id_para_remover
        return None