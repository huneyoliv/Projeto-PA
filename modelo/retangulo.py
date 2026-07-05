from dataclasses import dataclass
from modelo.figura_solida import FiguraSolida


@dataclass
class Retangulo(FiguraSolida):
    x_fim: float
    y_fim: float

    def desenha(self, canvas, dash=()) -> None:
        self.id = canvas.create_rectangle(
            self.x_inicio, self.y_inicio, self.x_fim, self.y_fim,
            outline=self.cor_borda, fill=self.cor_preenchimento, dash=dash
        )

    def vazia(self) -> bool:
        # Retorna True se for um ponto ou uma linha simples
        return self.x_inicio == self.x_fim or self.y_inicio == self.y_fim
