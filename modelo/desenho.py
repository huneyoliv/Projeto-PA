class Desenho:
    # Gerencia a persistência lógica de todas as figuras desenhadas
    def __init__(self):
        self.figuras = []

    def adiciona_figura(self, figura):
        self.figuras.append(figura)
