class Desenho:
    # Gerencia a persistência lógica de todas as figuras desenhadas
    def __init__(self):
        self.figuras = []

    def adiciona_figura(self, figura):
        self.figuras.append(figura)

    def desenha_figuras(self, canvas, dash=()):
        canvas.delete("all")
        for figura in self.figuras:
            figura.desenha(canvas, dash=dash)
