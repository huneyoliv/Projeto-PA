from dataclasses import dataclass
from modelo.figura_solida import FiguraSolida


@dataclass
class Retangulo(FiguraSolida):
    x_fim: float
    y_fim: float

    def vazia(self) -> bool:
        # Retorna True se for um ponto ou uma linha simples
        return abs(self.x_fim - self.x_inicio) < 5 or abs(self.y_fim - self.y_inicio) < 5
