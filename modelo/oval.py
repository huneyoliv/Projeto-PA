from dataclasses import dataclass
from modelo.figura_solida import FiguraSolida


@dataclass
class Oval(FiguraSolida):
    x_fim: float
    y_fim: float

    def vazia(self) -> bool:
        # Retorna True se não possuir largura ou altura válidas
        return abs(self.x_fim - self.x_inicio) < 5 or abs(self.y_fim - self.y_inicio) < 5
