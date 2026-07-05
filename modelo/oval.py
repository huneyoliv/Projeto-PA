from dataclasses import dataclass
from modelo.figura_solida import FiguraSolida


@dataclass
class Oval(FiguraSolida):
    x_fim: float
    y_fim: float

    def desenha(self, canvas, dash=()) -> None:
        self.id = canvas.create_oval(
            self.x_inicio, self.y_inicio, self.x_fim, self.y_fim,
            outline=self.cor_borda, fill=self.cor_preenchimento, dash=dash
        )

    def vazia(self) -> bool:
        # Retorna True se não possuir largura ou altura válidas
        return self.x_inicio == self.x_fim or self.y_inicio == self.y_fim
