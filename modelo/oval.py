from dataclasses import dataclass
from modelo.figura_solida import FiguraSolida


@dataclass
class Oval(FiguraSolida):
    x_fim: float
    y_fim: float

    def desenha(self, canvas, dash=(), width=None) -> None:
        w = width if width is not None else 1
        self.id = canvas.create_oval(
            self.x_inicio, self.y_inicio, self.x_fim, self.y_fim,
            outline=self.cor_borda, fill=self.cor_preenchimento, width=w, dash=dash
        )

    def contem(self, px: float, py: float) -> bool:
        # Equacao da elipse: (px-h)^2 / a^2 + (py-k)^2 / b^2 <= 1
        h = (self.x_inicio + self.x_fim) / 2
        k = (self.y_inicio + self.y_fim) / 2
        a = abs(self.x_fim - self.x_inicio) / 2
        b = abs(self.y_fim - self.y_inicio) / 2
        if a == 0 or b == 0:
            return False
        return ((px - h) / a) ** 2 + ((py - k) / b) ** 2 <= 1.0

    def mover(self, dx: float, dy: float) -> None:
        # Move a elipse transladando seus pontos delimitadores
        self.x_inicio += dx
        self.y_inicio += dy
        self.x_fim += dx
        self.y_fim += dy

    def vazia(self) -> bool:
        # Retorna True se não possuir largura ou altura válidas
        return abs(self.x_fim - self.x_inicio) < 5 or abs(self.y_fim - self.y_inicio) < 5

def contem(self, px: float, py: float) -> bool:
    
    cx = (self.x_inicio + self.x1) / 2
    cy = (self.y_inicio + self.y1) / 2
    rx = abs(self.x1 - self.x_inicio) / 2
    ry = abs(self.y1 - self.y_inicio) / 2
    if rx == 0 or ry == 0:
        return False
    return ((px - cx)**2 / rx**2) + ((py - cy)**2 / ry**2) <= 1.0

def mover(self, dx: float, dy: float) -> None:
    self.x_inicio += dx
    self.y_inicio += dy
    self.x1 += dx
    self.y1 += dy