from dataclasses import dataclass
from abc import ABC, abstractmethod


from modelo.MaoLivre import MaoLivre
from modelo.borracha import Borracha
from modelo.retangulo import Retangulo
from modelo.oval import Oval
from modelo.circulo import Circulo
from modelo.borracha import Borracha
from modelo.Linha import Linha
from modelo.Quadrado import Quadrado

# Classe Base (O Molde do Professor)
@dataclass
class Ferramenta(ABC):
    visao: any
    desenho: any
    canvas: any

    @abstractmethod
    def mouse_pressionado(self, event):
        pass

    @abstractmethod
    def mouse_arrastado(self, event):
        pass

    @abstractmethod
    def mouse_solto(self, event):
        pass

# Ferramenta Retângulo (Sua parte)
@dataclass
class Retangulo_Ferramenta(Ferramenta):
    retangulo_atual : 'Retangulo' = None

    def mouse_pressionado(self, event):
        bc = self.visao.cor_borda_var.get() or "black"
        pc = self.visao.cor_preenchimento_var.get() or "black"
        self.retangulo_atual = Retangulo(event.x, event.y, bc, pc, event.x, event.y)

    def mouse_arrastado(self, event):
        self.retangulo_atual = Retangulo(self.retangulo_atual.x1, self.retangulo_atual.y1, self.retangulo_atual.cor_borda, self.retangulo_atual.cor_preenchimento, event.x, event.y)
        self.desenho.desenha_figuras(self.canvas)
        self.retangulo_atual.desenha(self.canvas, dash=(4, 2))

    def mouse_solto(self, event):
        if not self.retangulo_atual.vazia():
            self.desenho.adiciona_figura(self.retangulo_atual)
        self.desenho.desenha_figuras(self.canvas)

# Ferramenta Oval (Sua parte)
@dataclass
class Oval_Ferramenta(Ferramenta):
    oval_atual : 'Oval' = None

    def mouse_pressionado(self, event):
        bc = self.visao.cor_borda_var.get() or "black"
        pc = self.visao.cor_preenchimento_var.get() or "black"
        self.oval_atual = Oval(event.x, event.y, bc, pc, event.x, event.y)

    def mouse_arrastado(self, event):
        self.oval_atual = Oval(self.oval_atual.x1, self.oval_atual.y1, self.oval_atual.cor_borda, self.oval_atual.cor_preenchimento, event.x, event.y)
        self.desenho.desenha_figuras(self.canvas)
        self.oval_atual.desenha(self.canvas, dash=(4, 2))

    def mouse_solto(self, event):
        if not self.oval_atual.vazia():
            self.desenho.adiciona_figura(self.oval_atual)
        self.desenho.desenha_figuras(self.canvas)

# Ferramenta Círculo (Sua parte)
@dataclass
class Circulo_Ferramenta(Ferramenta):
    circulo_atual : 'Circulo' = None

    def mouse_pressionado(self, event):
        bc = self.visao.cor_borda_var.get() or "black"
        pc = self.visao.cor_preenchimento_var.get() or "black"
    
        self.circulo_atual = Circulo.a_partir_de_centro_e_ponto(event.x, event.y, event.x, event.y, bc, pc)
        pass
    
    def mouse_arrastado(self, event):
        self.circulo_atual = Circulo.a_partir_de_centro_e_ponto(self.circulo_atual.x_centro, self.circulo_atual.y_centro, event.x, event.y, self.circulo_atual.cor_borda, self.circulo_atual.cor_preenchimento)
        self.desenho.desenha_figuras(self.canvas)
        self.circulo_atual.desenha(self.canvas, dash=(4, 2))
        pass

    def mouse_solto(self, event):
        if not self.circulo_atual.vazia():
            self.desenho.adiciona_figura(self.circulo_atual)
        self.desenho.desenha_figuras(self.canvas)
        pass

# Ferramenta Retângulo

@dataclass
class Retangulo_Ferramenta(Ferramenta):
    retangulo_atual : 'Retangulo' = None

    def mouse_pressionado(self, event):
        
        bc = self.visao.cor_borda_var.get() or "black"
        pc = self.visao.cor_preenchimento_var.get() or "black"
        self.retangulo_atual = Retangulo(event.x, event.y, bc, pc, event.x, event.y)

    def mouse_arrastado(self, event):
        
        self.retangulo_atual = Retangulo(self.retangulo_atual.x1, self.retangulo_atual.y1, self.retangulo_atual.cor_borda, self.retangulo_atual.cor_preenchimento, event.x, event.y)
        self.desenho.desenha_figuras(self.canvas) 
        self.retangulo_atual.desenha(self.canvas, dash=(4, 2)) 

    def mouse_solto(self, event):
        if not self.retangulo_atual.vazia():
            self.desenho.adiciona_figura(self.retangulo_atual)
        self.desenho.desenha_figuras(self.canvas)

# Ferramenta Oval

@dataclass
class Oval_Ferramenta(Ferramenta):
    oval_atual : 'Oval' = None

    def mouse_pressionado(self, event):
        bc = self.visao.cor_borda_var.get() or "black"
        pc = self.visao.cor_preenchimento_var.get() or "black"
        self.oval_atual = Oval(event.x, event.y, bc, pc, event.x, event.y)

    def mouse_arrastado(self, event):
        self.oval_atual = Oval(self.oval_atual.x1, self.oval_atual.y1, self.oval_atual.cor_borda, self.oval_atual.cor_preenchimento, event.x, event.y)
        self.desenho.desenha_figuras(self.canvas)
        self.oval_atual.desenha(self.canvas, dash=(4, 2))

    def mouse_solto(self, event):
        if not self.oval_atual.vazia():
            self.desenho.adiciona_figura(self.oval_atual)
        self.desenho.desenha_figuras(self.canvas)

# Ferramenta Círculo

@dataclass
class Circulo_Ferramenta(Ferramenta):
    circulo_atual : 'Circulo' = None

    def mouse_pressionado(self, event):
        bc = self.visao.cor_borda_var.get() or "black"
        pc = self.visao.cor_preenchimento_var.get() or "black"
        
        self.circulo_atual = Circulo.a_partir_de_centro_e_ponto(event.x, event.y, event.x, event.y, bc, pc)

    def mouse_arrastado(self, event):
        self.circulo_atual = Circulo.a_partir_de_centro_e_ponto(self.circulo_atual.x_centro, self.circulo_atual.y_centro, event.x, event.y, self.circulo_atual.cor_borda, self.circulo_atual.cor_preenchimento)
        self.desenho.desenha_figuras(self.canvas)
        self.circulo_atual.desenha(self.canvas, dash=(4, 2))

    def mouse_solto(self, event):
        if not self.circulo_atual.vazia():
            self.desenho.adiciona_figura(self.circulo_atual)
        self.desenho.desenha_figuras(self.canvas)

# Ferramenta Borracha

@dataclass
class Borracha_Ferramenta(Ferramenta):
    borracha_atual : 'Borracha' = None

    def mouse_pressionado(self, event):
        # Cria a borracha passando a coordenada inicial x_inicio e y_inicio exigidos pela classe mãe Figura
        self.borracha_atual = Borracha(x_inicio=event.x, y_inicio=event.y, pontos=[(event.x, event.y)]) 

    def mouse_arrastado(self, event):
        self.borracha_atual.pontos.append((event.x, event.y))
        self.desenho.desenha_figuras(self.canvas)
        self.borracha_atual.desenha(self.canvas)

    def mouse_solto(self, event):
        if not self.borracha_atual.vazia():
            self.desenho.adiciona_figura(self.borracha_atual)
        self.desenho.desenha_figuras(self.canvas)

#ferramenta Linha
@dataclass
class Linha_Ferramenta(Ferramenta):
    linha_atual: 'Linha' = None

    def mouse_pressionado(self, event):
        cor = self.visao.cor_borda_var.get() or "black"

        self.linha_atual = Linha.a_partir_de_pontos(
            event.x,
            event.y,
            event.x,
            event.y,
            cor)

    def mouse_arrastado(self, event):
        self.linha_atual = Linha.a_partir_de_pontos(
            self.linha_atual.x_inicio,
            self.linha_atual.y_inicio,
            event.x,
            event.y,
            self.linha_atual.cor)

        self.desenho.desenha_figuras(self.canvas)
        self.linha_atual.desenha(self.canvas, dash=(4, 2))

    def mouse_solto(self, event):
        if not self.linha_atual.vazia():
            self.desenho.adiciona_figura(self.linha_atual)
        self.desenho.desenha_figuras(self.canvas)     

#ferramenta Mão Livre
@dataclass
class MaoLivre_Ferramenta(Ferramenta):
    mao_livre_atual: 'MaoLivre' = None

    def mouse_pressionado(self, event):
        cor = self.visao.cor_borda_var.get() or "black"

        self.mao_livre_atual = MaoLivre.a_partir_do_primeiro_ponto(
            event.x,
            event.y,
            cor)

    def mouse_arrastado(self, event):
        self.mao_livre_atual.adicionar_ponto(
            event.x,
            event.y)

        self.desenho.desenha_figuras(self.canvas)
        self.mao_livre_atual.desenha(self.canvas)

    def mouse_solto(self, event):
        if not self.mao_livre_atual.vazia():
            self.desenho.adiciona_figura(self.mao_livre_atual)

        self.mao_livre_atual = None

        self.desenho.desenha_figuras(self.canvas)

#ferramenta Quadrado
@dataclass
class Quadrado_Ferramenta(Ferramenta):
    quadrado_atual: 'Quadrado' = None

    def mouse_pressionado(self, event):
        cor_borda = self.visao.cor_borda_var.get() or "black"
        cor_preenchimento = (
            self.visao.cor_preenchimento_var.get() or "black")

        self.quadrado_atual = Quadrado.a_partir_de_pontos(
            event.x,
            event.y,
            event.x,
            event.y,
            cor_borda,
            cor_preenchimento)

    def mouse_arrastado(self, event):
        self.quadrado_atual = Quadrado.a_partir_de_pontos(
            self.quadrado_atual.x_inicio,
            self.quadrado_atual.y_inicio,
            event.x,
            event.y,
            self.quadrado_atual.cor_borda,
            self.quadrado_atual.cor_preenchimento)

        self.desenho.desenha_figuras(self.canvas)
        self.quadrado_atual.desenha(
            self.canvas,
            dash=(4, 2))

    def mouse_solto(self, event):
        if not self.quadrado_atual.vazia():
            self.desenho.adiciona_figura(
                self.quadrado_atual)
        self.desenho.desenha_figuras(self.canvas)