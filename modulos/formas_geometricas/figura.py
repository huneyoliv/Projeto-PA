from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import math


@dataclass
class Figura(ABC):
    # Ponto de origem da figura
    x_inicio: float
    y_inicio: float
    id: int = field(default=None, init=False)

    @abstractmethod
    def desenhar(self, canvas) -> None:
        pass

    @abstractmethod
    def eh_valida(self) -> bool:
        pass

    @staticmethod
    def calcular_distancia(x1: float, y1: float, x2: float, y2: float) -> float:
        # Distância euclidiana entre dois pontos
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
