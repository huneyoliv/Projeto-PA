from dataclasses import dataclass
from modelo.figura_solida import FiguraSolida
from modelo.figura import Figura


@dataclass
class Circulo(FiguraSolida):
    raio: float

    def desenha(self, canvas, dash=(), width=None) -> None:
        w = width if width is not None else 1
        self.id = canvas.create_oval(
            self.x_inicio - self.raio, self.y_inicio - self.raio,
            self.x_inicio + self.raio, self.y_inicio + self.raio,
            outline=self.cor_borda, fill=self.cor_preenchimento, width=w, dash=dash
        )

    def contem(self, px: float, py: float) -> bool:
        # Ponto esta dentro do circulo se a distancia ao centro for menor ou igual ao raio
        return Figura.calcular_distancia(self.x_inicio, self.y_inicio, px, py) <= self.raio

    def mover(self, dx: float, dy: float) -> None:
        # Move o circulo transladando apenas o seu centro
        self.x_inicio += dx
        self.y_inicio += dy

    def vazia(self) -> bool:
        return self.raio < 5

    @classmethod
    def a_partir_de_centro_e_ponto(cls, cx: float, cy: float, px: float, py: float, cor_borda: str, cor_preenchimento: str):
        raio_calculado = Figura.calcular_distancia(cx, cy, px, py)
        return cls(
            x_inicio=cx, y_inicio=cy,
            cor_borda=cor_borda, cor_preenchimento=cor_preenchimento,
            raio=raio_calculado
        )
