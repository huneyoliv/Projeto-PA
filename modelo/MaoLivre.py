from dataclasses import dataclass
from modelo.FiguraLinear import FiguraLinear


@dataclass
class MaoLivre(FiguraLinear):
    #lista de pontos (x, y) percorridos pelo mouse
    pontos: list[tuple[float, float]]

    def vazia(self) -> bool:
        # Retorna True se o rabisco tiver menos de dois pontos
        return len(self.pontos) < 2

    def adicionar_ponto(self, x: float, y: float) -> None:
        self.pontos.append((x, y))

    @classmethod
    def a_partir_do_primeiro_ponto(
        cls,
        x_inicio: float,
        y_inicio: float,
        cor: str
    ) -> "MaoLivre":
        #o ponto inicial permanece sendo o primeiro ponto do desenho.
        return cls(
            x_inicio=x_inicio,
            y_inicio=y_inicio,
            cor=cor,
            pontos=[(x_inicio, y_inicio)]
        )