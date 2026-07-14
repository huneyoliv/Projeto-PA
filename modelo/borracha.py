from dataclasses import dataclass, field
from modelo.figura import Figura

@dataclass
class Borracha(Figura):
    pontos: list = field(default_factory=list)
    cor_borda: str = "white"
    espessura: int = 15

    def vazia(self) -> bool:
        return len(self.pontos) < 2

    def desenha(self, canvas, dash=()):
        
        for i in range(len(self.pontos) - 1):
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[i+1]
            canvas.create_line(x1, y1, x2, y2, fill=self.cor_borda, width=self.espessura, capstyle="round", joinstyle="round")