from modelo.Estado import Estado #importar a classe mãe 
from modelo.Linha import Linha 


class LinhaState(Estado):

    def __init__(self, desenho, canvas, visao):
        super().__init__(desenho, canvas, visao) # to chamando a classe"mãe" para usar isso

        self.x_inicio = 0 #guardar os pontos
        self.y_inicio = 0 

    def clicar(self, event): #implementa o método abstrato definido em Estado
        self.x_inicio = event.x #posição do mouse
        self.y_inicio = event.y

    def arrastar (self, event): #executa quando move o mouse com o botão pressionado
        cor = self.visao.cor_borda_var.get()

        self.desenho.desenha_figura(self.canvas)

        self.canvas.create_line(self.x_inicio,
                                self.y_inicio,
                                event.x,
                                event.y, 
                                fill=cor,
                                width=2,
                                dash=(4, 2))
    def soltar(self, event):
        cor = self.visao.cor_bordar_var.get() #guarda a cor escolhida

        Linha = Linha.a_partir_de_pontos(self.x_inicio,
                                         self.y_inicio,
                                         event.x,
                                         event.y, cor)
            
        if not Linha.vazia(): #virifica se a linha nao é vazia 
            self.desenho.adiciona_figura(Linha)

        self.desenho.desenha_figura(self.canvas)