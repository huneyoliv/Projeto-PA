from dataclasses import dataclass
from modelo.figura_solida import FiguraSolida


@dataclass
class Quadrado(FiguraSolida):
    x_fim: float
    y_fim: float

    @classmethod
    def a_partir_de_pontos(cls, x_inicio,
                           y_inicio,
                           x_atual,
                           y_atual,
                           cor_borda,
                           cor_preenchimento
                        ):
        deslocamento_x = x_atual - x_inicio #calcula quanto o mouse se moveu horizontal e verticalmente
        deslocamento_y = y_atual - y_inicio

        lado = min(abs(deslocamento_x), #para garantir que a altura e largura tenham o mesmo tamanho 
                   abs(deslocamento_y))
        
        direcao_x = -1 if deslocamento_x < 0 else 1  #p/ desenhar o quadrado, E e D, C e B 
        direcao_y = -1 if deslocamento_y < 0 else 1 

        x_fim = x_inicio + lado * direcao_x #coordenadas 
        y_fim = y_inicio + lado * direcao_y
        return cls(x_inicio, y_inicio, #criacao do objeto 
                   cor_borda,
                   cor_preenchimento,
                   x_fim,
                   y_fim)
    def desenha(self, canvas, dash=()) -> None:
        self.id = canvas.create_rectangle(self.x_inicio,
                                          self.y_inicio,
                                          self.x_fim,
                                          self.y_fim,
                                          outline=self.cor_borda,
                                          fill=self.cor_preenchimento, dash=dash)
        
    def vazia(self) -> bool: #verifica um dos lados pq largura e altura sao iguais 
        return abs(self.x_fim - self.x_inicio)  < 5 