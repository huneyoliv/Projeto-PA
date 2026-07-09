from dataclasses import dataclass
from modelo.FiguraLinear import FiguraLinear


@dataclass
class MaoLivre(FiguraLinear):
    #lista de pontos (x, y) percorridos pelo mouse
    pontos: list[tuple[float, float]]

    def desenha(self, canvas, dash=()) -> None: #desenha o rabisco no canva
        if len(self.pontos) > 1: #conta quantos elementos existem pq so um ponto nao tem linha
            coordenadas = []
            #lista auxiliar percorrendo todos os pontos
            for x, y in self.pontos:
                coordenadas.extend([x, y]) #adiciona varios elementos
   
            self.id = canvas.create_line(  # cria linha e salva o id
                *coordenadas, #desempacotamento, pega os elementos e separa um por um 
                fill=self.cor,
                width=2,
                dash=dash
            )

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