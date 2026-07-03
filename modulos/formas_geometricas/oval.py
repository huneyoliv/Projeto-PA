from dataclasses import dataclass
from modulos.formas_geometricas.figura_solida import FiguraSolida


@dataclass
class Oval(FiguraSolida):
    # Coordenadas do canto oposto delimitador
    x_fim: float
    y_fim: float

    def desenhar(self, canvas) -> None:
        self.id = canvas.create_oval(
            self.x_inicio, self.y_inicio, self.x_fim, self.y_fim,
            outline=self.cor_borda, fill=self.cor_preenchimento
        )

    def eh_valida(self) -> bool:
        # Garante que possui largura e altura
        return self.x_inicio != self.x_fim and self.y_inicio != self.y_fim
