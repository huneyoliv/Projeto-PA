from dataclasses import dataclass
from modelo.FiguraLinear import FiguraLinear


@dataclass
class Linha(FiguraLinear):#herda da classe mae FiguraLinear
    #coordenadas do ponto final da linha
    x_fim: float
    y_fim: float

    def desenha(self, canvas, dash=(), width=None) -> None: #pra criar figuras dentro canvas
        w = width if width is not None else 2
        self.id = canvas.create_line(  #id ajuda a registrar e achar rapido
            self.x_inicio, #ponto inicial
            self.y_inicio,
            self.x_fim,   #ponto final
            self.y_fim,
            fill=self.cor,
            width=w,
            dash=dash  #desenha linhas tracejadas
        )

    def contem(self, px: float, py: float) -> bool:
        # Retorna True se o ponto (px, py) estiver a ate 3 pixels de distancia da linha
        from modelo.figura import distancia_ponto_segmento
        return distancia_ponto_segmento(self.x_inicio, self.y_inicio, self.x_fim, self.y_fim, px, py) <= 3

    def mover(self, dx: float, dy: float) -> None:
        # Move a linha adicionando dx e dy aos pontos de inicio e fim
        self.x_inicio += dx
        self.y_inicio += dy
        self.x_fim += dx
        self.y_fim += dy

    def vazia(self) -> bool:
        # Retorna True se a linha for apenas um ponto ou muito curta
        from modelo.figura import Figura
        return Figura.calcular_distancia(self.x_inicio, self.y_inicio, self.x_fim, self.y_fim) < 5

    @classmethod   #pertence a classe e nao ao objeto 
    def a_partir_de_pontos(
        cls,
        x_inicio: float,
        y_inicio: float,
        x_fim: float,
        y_fim: float,
        cor: str
    ):
        return cls(
            x_inicio=x_inicio,
            y_inicio=y_inicio,
            cor=cor,
            x_fim=x_fim,
            y_fim=y_fim
        )
    
def contem(self, px: float, py: float) -> bool:
    from modelo.figura import distancia_ponto_segmento
    dist = distancia_ponto_segmento(self.x_inicio, self.y_inicio, self.x1, self.y1, px, py)
    return dist <= 5.0

def mover(self, dx: float, dy: float) -> None:
    self.x_inicio += dx
    self.y_inicio += dy
    self.x1 += dx
    self.y1 += dy