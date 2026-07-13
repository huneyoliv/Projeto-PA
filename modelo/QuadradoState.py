from modelo.Estado import Estado
from modelo.Quadrado import Quadrado 


class QuadradoState(Estado):

    def __init__(self, desenho,  canvas, visao):
        super().__init__(desenho, canvas, visao)

        self.x_inicio = 0 
        self.y_inicio =0 

    def clicar(self, event):
        self.x_inicio = event.x
        self.y_inicio = event.y

    def arrastar(self, event):
        cor_borda = self.visao.cor_borda_var.get()
        cor_preenchimento = self.visao.cor_preenchimento_var.get()

        Quadrado = Quadrado.a_partir_de_pontos(self.x_inicio,
                                               self.y_inicio,
                                               event.x,
                                               event.y,
                                               cor_borda,
                                               cor_preenchimento)
        self.desenho.desenha_figuras(self.canvas)
        Quadrado.desenha(self.canvas, dash=(4, 2))

    def soltar(self, event):
        
        cor_borda = self.visao.cor_borda_var.get()
        cor_preenchimento = self.visao.cor_preenchimentto_var.get()

        Quadrado = Quadrado.a_partir_de_pontos(self.x_inicio,
                                               self.y_inicio,
                                               event.x,
                                               event.y,
                                               cor_borda,
                                               cor_preenchimento)
        if not Quadrado.vazia():
            self.desenho.adiciona_figura(Quadrado)

        self.desenho.desenha_figura(self.canvas)
