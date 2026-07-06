from modelo.desenho import Desenho
from modelo.figura import Figura
from modelo.retangulo import Retangulo
from modelo.oval import Oval
from modelo.circulo import Circulo
from modelo.Linha import Linha
from modelo.MaoLivre import MaoLivre
from visao.janelaPaint import JanelaPaint


class ControladorPaint:
    # Controller: Centraliza a escuta de eventos e interações com o modelo e a visão
    def __init__(self, desenho: Desenho, visao: JanelaPaint):
        self.desenho = desenho
        self.visao = visao
        self.canvas = self.visao.canvas

        self.x_inicio = 0
        self.y_inicio = 0
        self.figura_atual = None  # guarda a mao livre em andamento

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
            self.visao.limpar_indicador_borracha()

    def ao_clicar(self, event):
        t = self.visao.tipo_figura_var.get()
        if t == "borracha":
            id_para_remover = self.visao.obter_figura_sob_cursor(event.x, event.y)
            if id_para_remover is not None:
                self.desenho.figuras = [fig for fig in self.desenho.figuras if fig.id != id_para_remover]
                self.visao.atualizar_tela(self.desenho)
                self.visao.atualizar_indicador_borracha(event.x, event.y)
            return

        self.x_inicio = event.x
        self.y_inicio = event.y

        if t == "maolivre":
            # inicia um novo rabisco a partir do ponto clicado
            bc = self.visao.cor_borda_var.get()
            self.figura_atual = MaoLivre.a_partir_do_primeiro_ponto(event.x, event.y, bc)

    def ao_arrastar(self, event):
        t = self.visao.tipo_figura_var.get()
        if t == "borracha":
            self.visao.atualizar_indicador_borracha(event.x, event.y)
            id_para_remover = self.visao.obter_figura_sob_cursor(event.x, event.y)
            if id_para_remover is not None:
                self.desenho.figuras = [fig for fig in self.desenho.figuras if fig.id != id_para_remover]
                self.visao.atualizar_tela(self.desenho)
                self.visao.atualizar_indicador_borracha(event.x, event.y)
            return

        bc = self.visao.cor_borda_var.get()
        pc = self.visao.cor_preenchimento_var.get()

        self.visao.atualizar_tela(self.desenho)

        if t == "retangulo":
            self.visao.desenhar_preview_retangulo(self.x_inicio, self.y_inicio, event.x, event.y, bc, pc)
        elif t == "oval":
            self.visao.desenhar_preview_oval(self.x_inicio, self.y_inicio, event.x, event.y, bc, pc)
        elif t == "circulo":
            raio = Figura.calcular_distancia(self.x_inicio, self.y_inicio, event.x, event.y)
            self.visao.desenhar_preview_circulo(self.x_inicio, self.y_inicio, raio, bc, pc)
        elif t == "linha":
            # preview tracejado enquanto arrasta
            self.visao.desenhar_preview_linha(self.x_inicio, self.y_inicio, event.x, event.y, bc)
        elif t == "maolivre" and self.figura_atual:
            self.figura_atual.adicionar_ponto(event.x, event.y) #adiciona pontos toda vez que o mouse se move
            self.visao.desenhar_figura(self.figura_atual)

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
        elif t == "linha":
            figura_nova = Linha.a_partir_de_pontos(ki, yi, event.x, event.y, bc)
        elif t == "maolivre" and self.figura_atual:
            figura_nova = self.figura_atual
            self.figura_atual = None  # limpa a figura em andamento

        if figura_nova and not figura_nova.vazia():
            self.desenho.adiciona_figura(figura_nova)

        self.visao.atualizar_tela(self.desenho)

    def ao_mover(self, event):
        if self.visao.tipo_figura_var.get() == "borracha":
            self.visao.atualizar_indicador_borracha(event.x, event.y)
        else:
            self.visao.limpar_indicador_borracha()

    def ao_sair(self, event):
        self.visao.limpar_indicador_borracha()
