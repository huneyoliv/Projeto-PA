from modelo.Estado import Estado
from modelo.MaoLivre import MaoLivre 


class MaoLivreState(Estado): #concreteState da ferramenta mao livre

    def __init__(self, desenho, canvas, visao):
        super().__init__(desenho, canvas, visao)
        self.figura_atual = None #guada que esta sendo desenhada pq vai crescendo durante o arraste 

    def clicar(self, event):
        cor = self.visao.cor_borda_var.get()

        self.figura_atual = MaoLivre.a_partir_do_primeiro_ponto(event.x,
                                                                event.y,
                                                                cor)
        
    def arrastar (self, event):

        if self.figura_atual is None:  #se o usuario arrastar sem clicar antes nada acontece 
            return
        
        self.figura_atual.adicionar_ponto(event.x, event.y)
        self.desenho.desenha_figura(self.canvas)
        self.figura_atual.desenha(self.canvas)

    def soltar(self, _event): #parametro nao utilizado 

        if self.figura_atual is None:
            return 
        if not self.figura_atual.vazia():
            self.desenho.adiciona_figura(self.figura_atual)

        self.figura_atual = None
        self.desenho.desenha_figuras(self.canvas)