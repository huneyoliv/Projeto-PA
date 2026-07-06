from dataclasses import dataclass
from abc import ABC, abstractmethod
import math
from modulos.cores.visual import ValidadorCores
# --- CLASSES ABSTRATAS ---

@dataclass
class Figura(ABC):
    """Classe base para todas figuras geométricas"""
    x_inicio: float
    y_inicio: float

    @abstractmethod
    def desenhar(self, canvas) -> None:
        """Desenha a figura no canvas."""
        pass

    @abstractmethod
    def eh_valida(self) -> bool:
        """Verifica se a figura tem tamanho válido."""
        pass

    @staticmethod
    def calcular_distancia(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calcula a distância entre dois pontos (estático)."""
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


@dataclass
class FiguraSolida(Figura, ABC):
    """Classe para figuras com borda e preenchimento (Herança)."""
    cor_borda: str
    cor_preenchimento: str

    def _setattr_(self, nome, valor):
        # Delega a responsabilidade de validação para o módulo (THÉO)
        if nome in ["cor_borda", "cor_preenchimento"]:
            valor = ValidadorCores.validar(nome, valor)
        
        super()._setattr_(nome, valor)


# --- CLASSES CONCRETAS (HUNEY) ---

@dataclass
class Retangulo(FiguraSolida):
    """Classe para desenhar retângulos."""
    x_fim: float
    y_fim: float

    def desenhar(self, canvas) -> None:
        canvas.create_rectangle(
            self.x_inicio, self.y_inicio, self.x_fim, self.y_fim,
            outline=self.cor_borda, fill=self.cor_preenchimento
        )

    def eh_valida(self) -> bool:
        return self.x_inicio != self.x_fim or self.y_inicio != self.y_fim


@dataclass
class Oval(FiguraSolida):
    """Classe para desenhar elipses/ovais."""
    x_fim: float
    y_fim: float

    def desenhar(self, canvas) -> None:
        canvas.create_oval(
            self.x_inicio, self.y_inicio, self.x_fim, self.y_fim,
            outline=self.cor_borda, fill=self.cor_preenchimento
        )

    def eh_valida(self) -> bool:
        return self.x_inicio != self.x_fim or self.y_inicio != self.y_fim


@dataclass
class Circulo(FiguraSolida):
    """Classe para desenhar círculos."""
    raio: float

    def desenhar(self, canvas) -> None:
        canvas.create_oval(
            self.x_inicio - self.raio, self.y_inicio - self.raio,
            self.x_inicio + self.raio, self.y_inicio + self.raio,
            outline=self.cor_borda, fill=self.cor_preenchimento
        )

    def eh_valida(self) -> bool:
        return self.raio > 0

    @classmethod
    def a_partir_de_centro_e_ponto(cls, cx: float, cy: float, px: float, py: float, cor_borda: str, cor_preenchimento: str):
        """Cria um círculo calculando o raio a partir do centro e um ponto (método de classe)."""
        raio_calculado = cls.calcular_distancia(cx, cy, px, py)
        return cls(
            x_inicio=cx, y_inicio=cy,
            cor_borda=cor_borda, cor_preenchimento=cor_preenchimento,
            raio=raio_calculado
        )

