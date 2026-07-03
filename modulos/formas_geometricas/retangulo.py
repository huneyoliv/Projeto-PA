from dataclasses import dataclass
from modulos.formas_geometricas.figura_solida import FiguraSolida


@dataclass
class Retangulo(FiguraSolida):
    # Coordenadas do canto oposto
    x_fim: float
    y_fim: float

    def desenhar(self, canvas) -> None:
        self.id = canvas.create_rectangle(
            self.x_inicio, self.y_inicio, self.x_fim, self.y_fim,
            outline=self.cor_borda, fill=self.cor_preenchimento
        )

    def eh_valida(self) -> bool:
        # Garante que não é ponto ou linha simples
        return self.x_inicio != self.x_fim and self.y_inicio != self.y_fim
