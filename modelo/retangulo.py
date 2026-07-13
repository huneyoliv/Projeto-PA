from dataclasses import dataclass
from modelo.figura_solida import FiguraSolida


@dataclass
class Retangulo(FiguraSolida):
    x_fim: float
    y_fim: float

    def desenha(self, canvas, dash=(), width=None) -> None:
        w = width if width is not None else 1
        self.id = canvas.create_rectangle(
            self.x_inicio, self.y_inicio, self.x_fim, self.y_fim,
            outline=self.cor_borda, fill=self.cor_preenchimento, width=w, dash=dash
        )

    def contem(self, px: float, py: float) -> bool:
        # Verifica se o ponto clicado esta dentro do retangulo
        x_min, x_max = min(self.x_inicio, self.x_fim), max(self.x_inicio, self.x_fim)
        y_min, y_max = min(self.y_inicio, self.y_fim), max(self.y_inicio, self.y_fim)
        return x_min <= px <= x_max and y_min <= py <= y_max

    def mover(self, dx: float, dy: float) -> None:
        # Move o retangulo transladando seus cantos
        self.x_inicio += dx
        self.y_inicio += dy
        self.x_fim += dx
        self.y_fim += dy

    def vazia(self) -> bool:
        # Retorna True se for um ponto ou uma linha simples
        return abs(self.x_fim - self.x_inicio) < 5 or abs(self.y_fim - self.y_inicio) < 5
