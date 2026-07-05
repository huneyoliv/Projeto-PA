from modelo.desenho import Desenho
from modelo.figura import Figura
from modelo.retangulo import Retangulo
from modelo.oval import Oval
from modelo.circulo import Circulo
from visao.janelaPaint import JanelaPaint


class ControladorPaint:
    # Controller: Centraliza a escuta de eventos e interações com o modelo e a visão
    def __init__(self, desenho: Desenho, visao: JanelaPaint):
        self.desenho = desenho
        self.visao = visao
        self.canvas = self.visao.canvas
        
        self.x_inicio = 0
        self.y_inicio = 0
        self.id_borracha_temp = None

        self.canvas.bind("<ButtonPress-1>", self.ao_clicar)
        self.canvas.bind("<B1-Motion>", self.ao_arrastar)
        self.canvas.bind("<ButtonRelease-1>", self.ao_soltar)
        self.canvas.bind("<Motion>", self.ao_mover)
        self.canvas.bind("<Leave>", self.ao_sair)

        # Observa mudanças nas variáveis da visão para atualizar status
        self.visao.tipo_figura_var.trace_add("write", lambda *a: self._atualiza_status())
        self.visao.cor_borda_var.trace_add("write", lambda *a: self._atualiza_status())
        self.visao.cor_preenchimento_var.trace_add("write", lambda *a: self._atualiza_status())
        self._atualiza_status()

    def _atualiza_status(self):
        f = self.visao.tipo_figura_var.get().upper()
        b = self.visao.cor_borda_var.get().upper()
        p = self.visao.cor_preenchimento_var.get().upper()
        self.visao.atualiza_status(f"Ferramenta: {f} | Borda: {b} | Preenchimento: {p}")
        if self.visao.tipo_figura_var.get() != "borracha":
            self._limpar_indicador_borracha()

    def ao_clicar(self, event):
        t = self.visao.tipo_figura_var.get()
        if t == "borracha":
            itens = self.canvas.find_overlapping(event.x - 3, event.y - 3, event.x + 3, event.y + 3)
            if itens:
                id_para_remover = itens[-1]
                self.desenho.figuras = [fig for fig in self.desenho.figuras if fig.id != id_para_remover]
                self.desenho.desenha_figuras(self.canvas)
            return

        self.x_inicio = event.x
        self.y_inicio = event.y

    def ao_arrastar(self, event):
        t = self.visao.tipo_figura_var.get()
        if t == "borracha":
            return

        self.desenho.desenha_figuras(self.canvas)
        bc = self.visao.cor_borda_var.get()
        pc = self.visao.cor_preenchimento_var.get()

        if t == "retangulo":
            self.canvas.create_rectangle(self.x_inicio, self.y_inicio, event.x, event.y, outline=bc, fill=pc, dash=(4, 2))
        elif t == "oval":
            self.canvas.create_oval(self.x_inicio, self.y_inicio, event.x, event.y, outline=bc, fill=pc, dash=(4, 2))
        elif t == "circulo":
            raio = Figura.calcular_distancia(self.x_inicio, self.y_inicio, event.x, event.y)
            self.canvas.create_oval(self.x_inicio - raio, self.y_inicio - raio, self.x_inicio + raio, self.y_inicio + raio, outline=bc, fill=pc, dash=(4, 2))

    def ao_soltar(self, event):
        t = self.visao.tipo_figura_var.get()
        if t == "borracha":
            return

        figura_nova = None
        ki, yi = self.x_inicio, self.y_inicio
        bc = self.visao.cor_borda_var.get()
        pc = self.visao.cor_preenchimento_var.get()

        if t == "retangulo":
            figura_nova = Retangulo(ki, yi, bc, pc, event.x, event.y)
        elif t == "oval":
            figura_nova = Oval(ki, yi, bc, pc, event.x, event.y)
        elif t == "circulo":
            figura_nova = Circulo.a_partir_de_centro_e_ponto(ki, yi, event.x, event.y, bc, pc)

        if figura_nova and not figura_nova.vazia():
            self.desenho.adiciona_figura(figura_nova)

        self.desenho.desenha_figuras(self.canvas)

    def ao_mover(self, event):
        if self.visao.tipo_figura_var.get() == "borracha":
            r = 6
            if self.id_borracha_temp is None:
                self.id_borracha_temp = self.canvas.create_oval(
                    event.x - r, event.y - r, event.x + r, event.y + r,
                    outline="red", width=1, dash=(2, 2)
                )
            else:
                self.canvas.coords(self.id_borracha_temp, event.x - r, event.y - r, event.x + r, event.y + r)
                self.canvas.tag_raise(self.id_borracha_temp)
        else:
            self._limpar_indicador_borracha()

    def ao_sair(self, event):
        self._limpar_indicador_borracha()

    def _limpar_indicador_borracha(self):
        if self.id_borracha_temp is not None:
            self.canvas.delete(self.id_borracha_temp)
            self.id_borracha_temp = None
