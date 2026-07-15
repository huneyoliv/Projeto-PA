from dataclasses import dataclass
from modelo.FiguraLinear import FiguraLinear


@dataclass
class MaoLivre(FiguraLinear):
    #lista de pontos (x, y) percorridos pelo mouse
    pontos: list[tuple[float, float]]

    def desenha(self, canvas, dash=(), width=None) -> None: #desenha o rabisco no canva
        if len(self.pontos) > 1: #conta quantos elementos existem pq so um ponto nao tem linha
            coordenadas = []
            #lista auxiliar percorrendo todos os pontos
            for x, y in self.pontos:
                coordenadas.extend([x, y]) #adiciona varios elementos
   
            w = width if width is not None else 2
            self.id = canvas.create_line(  # cria linha e salva o id
                *coordenadas, #desempacotamento, pega os elementos e separa um por um 
                fill=self.cor,
                width=w,
                dash=dash
            )

    def contem(self, px: float, py: float) -> bool:
        # Verifica se o clique do mouse esta proximo de qualquer segmento da linha livre
        from modelo.figura import distancia_ponto_segmento
        return any(
            distancia_ponto_segmento(x1, y1, x2, y2, px, py) <= 3
            for (x1, y1), (x2, y2) in zip(self.pontos, self.pontos[1:])
        )

    def mover(self, dx: float, dy: float) -> None:
        # Move a mao livre e todos os seus pontos acumulados
        self.x_inicio += dx
        self.y_inicio += dy
        for i in range(len(self.pontos)):
            x, y = self.pontos[i]
            self.pontos[i] = (x + dx, y + dy)

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
    
def contem(self, px: float, py: float) -> bool:
    from modelo.figura import distancia_ponto_segmento
    for i in range(len(self.pontos) - 1):
        p1 = self.pontos[i]
        p2 = self.pontos[i + 1]
        dist = distancia_ponto_segmento(p1[0], p1[1], p2[0], p2[1], px, py)
        if dist <= 5.0:
            return True
    return False

def mover(self, dx: float, dy: float) -> None:
    novos_pontos = []
    for x, y in self.pontos:
        novos_pontos.append((x + dx, y + dy))
    self.pontos = novos_pontos