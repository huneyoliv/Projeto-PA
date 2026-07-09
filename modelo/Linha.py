from dataclasses import dataclass
from modelo.FiguraLinear import FiguraLinear


@dataclass
class Linha(FiguraLinear):#herda da classe mae FiguraLinear
    #coordenadas do ponto final da linha
    x_fim: float
    y_fim: float

    def desenha(self, canvas, dash=()) -> None: #pra criar figuras dentro canvas
        self.id = canvas.create_line(  #id ajuda a registrar e achar rapido
            self.x_inicio, #ponto inicial
            self.y_inicio,
            self.x_fim,   #ponto final
            self.y_fim,
            fill=self.cor,
            width=2,
            dash=dash  #desenha linhas tracejadas
        )

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