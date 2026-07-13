from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import math


@dataclass
class Figura(ABC):
    # Origem do desenho
    x_inicio: float
    y_inicio: float
    id: int = field(default=None, init=False)

    @abstractmethod
    def desenha(self, canvas, dash=(), width=None) -> None:
        pass

    @abstractmethod
    def vazia(self) -> bool:
        pass

    @abstractmethod
    def contem(self, px: float, py: float) -> bool:
        pass

    @abstractmethod
    def mover(self, dx: float, dy: float) -> None:
        pass

    @staticmethod
    def calcular_distancia(x1: float, y1: float, x2: float, y2: float) -> float:
        # Distância euclidiana entre dois pontos
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def distancia_ponto_segmento(x1, y1, x2, y2, px, py) -> float:
    # Calcula a menor distância entre um ponto (px, py) e o segmento de reta ((x1,y1), (x2,y2))
    dx = x2 - x1
    dy = y2 - y1
    ab_len_sq = dx**2 + dy**2
    if ab_len_sq == 0:
        return math.sqrt((px - x1)**2 + (py - y1)**2)
    t = (px - x1) * dx + (py - y1) * dy
    t = max(0.0, min(1.0, t / ab_len_sq))
    ponto_proximo_x = x1 + t * dx
    ponto_proximo_y = y1 + t * dy
    return math.sqrt((px - ponto_proximo_x)**2 + (py - ponto_proximo_y)**2)
