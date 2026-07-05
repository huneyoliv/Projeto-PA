from dataclasses import dataclass
from modelo.figura_solida import FiguraSolida
from modelo.figura import Figura


@dataclass
class Circulo(FiguraSolida):
    raio: float

    def desenha(self, canvas, dash=()) -> None:
        self.id = canvas.create_oval(
            self.x_inicio - self.raio, self.y_inicio - self.raio,
            self.x_inicio + self.raio, self.y_inicio + self.raio,
            outline=self.cor_borda, fill=self.cor_preenchimento, dash=dash
        )

    def vazia(self) -> bool:
        return self.raio <= 0

    @classmethod
    def a_partir_de_centro_e_ponto(cls, cx: float, cy: float, px: float, py: float, cor_borda: str, cor_preenchimento: str):
        raio_calculado = Figura.calcular_distancia(cx, cy, px, py)
        return cls(
            x_inicio=cx, y_inicio=cy,
            cor_borda=cor_borda, cor_preenchimento=cor_preenchimento,
            raio=raio_calculado
        )
