class Desenho:
    # Gerencia a persistência lógica de todas as figuras desenhadas
    def __init__(self):
        self.figuras = []
        self.__selecionada = -1
        self.buffer = None

    def adiciona_figura(self, figura):
        self.figuras.append(figura)

    def desenha_figuras(self, canvas, dash=()):
        canvas.delete("all")
        for i in range(len(self.figuras)):
            if i == self.__selecionada:
                # Desenha a figura selecionada com destaque visual tracejado grosso
                self.figuras[i].desenha(canvas, dash=(10, 2), width=4)
            else:
                self.figuras[i].desenha(canvas, dash=dash)

    def limpa_selecao(self):
        self.__selecionada = -1

    def seleciona(self, px, py):
        # Seleciona de tras para frente para priorizar figuras no topo do canvas
        i = len(self.figuras) - 1
        while i >= 0 and not self.figuras[i].contem(px, py):
            i -= 1
        self.__selecionada = i

    def selecionada(self):
        if self.__selecionada >= 0:
            return self.figuras[self.__selecionada]
        return None

    def copiar_selecionada(self):
        import copy
        self.buffer = copy.deepcopy(self.selecionada())

    def colar(self):
        if self.buffer is not None:
            f = self.buffer
            f.mover(10, 10)
            self.figuras.append(f)
            import copy
            self.buffer = copy.deepcopy(f)

    def selecionada_para_topo(self):
        s = self.__selecionada
        if s != -1:
            f = self.figuras.pop(s)
            self.figuras.append(f)
            self.__selecionada = len(self.figuras) - 1

    def selecionada_para_fundo(self):
        s = self.__selecionada
        if s != -1:
            f = self.figuras.pop(s)
            self.figuras.insert(0, f)
            self.__selecionada = 0

    def selecionada_para_tras(self):
        s = self.__selecionada
        if s > 0:
            self.figuras[s], self.figuras[s-1] = self.figuras[s-1], self.figuras[s]
            self.__selecionada -= 1

    def selecionada_para_frente(self):
        s = self.__selecionada
        if 0 <= s < len(self.figuras) - 1:
            self.figuras[s], self.figuras[s+1] = self.figuras[s+1], self.figuras[s]
            self.__selecionada += 1

    def apaga_selecionada(self):
        s = self.__selecionada
        if s != -1:
            self.figuras.pop(s)
            self.__selecionada = -1
