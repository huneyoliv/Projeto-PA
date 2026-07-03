from dataclasses import dataclass
from abc import ABC, abstractmethod
import math

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
    """Classe intermediária responsável por injetar propriedades visuais nas figuras.
    Implementa validação rigorosa de tipo para os atributos cor_borda e cor_preenchimento
    utilizando o interceptador de atributos _setattr_."""
    cor_borda: str
    cor_preenchimento: str

    def __setattr__(self, nome, valor):
        # Validação/Encapsulamento
        if nome == "cor_borda":
            if not isinstance(valor, str):
                raise TypeError("A cor da borda deve ser texto.")
            if valor.strip() == "":
                valor = "black"
        elif nome == "cor_preenchimento":
            if not isinstance(valor, str):
                raise TypeError("A cor de preenchimento deve ser texto.")
        
        super().__setattr__(nome, valor)


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

