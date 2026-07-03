from tkinter import Tk
from modulos.janela.interface import Interface
from modulos.formas_geometricas.retangulo import Retangulo
from modulos.formas_geometricas.oval import Oval
from modulos.formas_geometricas.circulo import Circulo
from modulos.formas_geometricas.figura import Figura
from modulos.linhas_e_rabiscos.linhas import Linha, Rabisco


class AplicativoDesenho:
    # Gerencia o estado dos desenhos e orquestra a lógica
    def __init__(self, root: Tk):
        root.title("Desenhos Geométricos Coloridos")
        
        self.desenhos_salvos = []
        self.tipo_desenho_atual = "retangulo"
        self.cor_borda_atual = "black"
        self.cor_preenchimento_atual = "white"
        
        self.x_inicio = 0
        self.y_inicio = 0
        self.pontos_rabisco_temp = []
        
        # Inicializa a interface visual
        self.ui = Interface(
            root,
            self.muda_ferramenta, self.muda_cor_borda, self.muda_cor_preenchimento,
            self.ao_clicar, self.ao_arrastar, self.ao_soltar
        )
        self._atualiza_status()

    def muda_ferramenta(self, f):
        self.tipo_desenho_atual = f
        self._atualiza_status()

    def muda_cor_borda(self, c):
        self.cor_borda_atual = c
        self._atualiza_status()

    def muda_cor_preenchimento(self, c):
        self.cor_preenchimento_atual = c
        self._atualiza_status()

    def _atualiza_status(self):
        self.ui.atualiza_status(
            f"Ferramenta: {self.tipo_desenho_atual.upper()} | "
            f"Borda: {self.cor_borda_atual.upper()} | "
            f"Preenchimento: {self.cor_preenchimento_atual.upper()}"
        )

    def ao_clicar(self, event):
        self.x_inicio = event.x
        self.y_inicio = event.y
        self.pontos_rabisco_temp = [(event.x, event.y)]

    def ao_arrastar(self, event):
        # Limpa rascunhos anteriores e mostra feedback visual do desenho em progresso
        self._redesenhar_salvos()
        canvas = self.ui.canvas
        t = self.tipo_desenho_atual
        
        if t == "retangulo":
            canvas.create_rectangle(self.x_inicio, self.y_inicio, event.x, event.y,
                outline=self.cor_borda_atual, fill=self.cor_preenchimento_atual, dash=(4, 2))
        elif t == "oval":
            canvas.create_oval(self.x_inicio, self.y_inicio, event.x, event.y,
                outline=self.cor_borda_atual, fill=self.cor_preenchimento_atual, dash=(4, 2))
        elif t == "circulo":
            raio = Figura.calcular_distancia(self.x_inicio, self.y_inicio, event.x, event.y)
            canvas.create_oval(self.x_inicio - raio, self.y_inicio - raio,
                self.x_inicio + raio, self.y_inicio + raio,
                outline=self.cor_borda_atual, fill=self.cor_preenchimento_atual, dash=(4, 2))
        elif t == "linha":
            canvas.create_line(self.x_inicio, self.y_inicio, event.x, event.y,
                fill=self.cor_borda_atual, dash=(4, 2))
        elif t == "rabisco":
            self.pontos_rabisco_temp.append((event.x, event.y))
            if len(self.pontos_rabisco_temp) > 1:
                canvas.create_line(self.pontos_rabisco_temp, fill=self.cor_borda_atual, dash=(4, 2))

    def ao_soltar(self, event):
        # Fabrica e salva a figura se for válida
        figura = self._criar_figura(event.x, event.y)
        if figura is not None and figura.eh_valida():
            self.desenhos_salvos.append(figura)
        self._redesenhar_salvos()

    def _criar_figura(self, x, y):
        t = self.tipo_desenho_atual
        ki = self.x_inicio
        yi = self.y_inicio
        bc = self.cor_borda_atual
        pc = self.cor_preenchimento_atual
        
        if t == "retangulo":
            return Retangulo(x_inicio=ki, y_inicio=yi, cor_borda=bc, cor_preenchimento=pc, x_fim=x, y_fim=y)
        if t == "oval":
            return Oval(x_inicio=ki, y_inicio=yi, cor_borda=bc, cor_preenchimento=pc, x_fim=x, y_fim=y)
        if t == "circulo":
            return Circulo.a_partir_de_centro_e_ponto(ki, yi, x, y, bc, pc)
        if t == "linha":
            return Linha(x_inicio=ki, y_inicio=yi, x_fim=x, y_fim=y, cor=bc)
        if t == "rabisco":
            return Rabisco(x_inicio=ki, y_inicio=yi, pontos=self.pontos_rabisco_temp, cor=bc)
        return None

    def _redesenhar_salvos(self):
        self.ui.canvas.delete("all")
        for figura in self.desenhos_salvos:
            figura.desenhar(self.ui.canvas)
