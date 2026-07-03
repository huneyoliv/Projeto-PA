from modulos.formas_geometricas.formas import Figura

#-------classe mãe --------# colocar aqui o que todas possuem em comum

class Figuras(Figura):  #classe abstrata
    def __init__(self, x_inicio, y_inicio, cor="black"):  #metodo construtor
        super().__init__(x_inicio, y_inicio)
        self.cor = cor #guardando dentro do objeto
        self.id = None # id vazio mas posso usar para mexer na figura(acho)
        self.x1 = x_inicio
        self.y1 = y_inicio #formam um ponto

    def iniciar(self, x, y): # posicao atual do mouse na vertical e na horizontal 
        self.x1 = x 
        self.y1 = y
        
    def atualizar(self, x2, y2): #atualiza a posição das figuras 
        pass

    def mudar_cor(self, cor):
        self.cor = cor # modificar as propriedades de um item que ja existe | contorno linha

    def mover(self, dx, dy):  #move as formas 
        pass

#-------classes filhas ------
class Linha(Figuras): #criar uma classe so para linhas 
    
    def __init__(self, x_inicio, y_inicio, x_fim, y_fim, cor="black"):
        super().__init__(x_inicio, y_inicio, cor)
        self.x_fim = x_fim
        self.y_fim = y_fim
        
    def desenhar(self, canvas) -> None:
        self.id = canvas.create_line(
            self.x_inicio, self.y_inicio, self.x_fim, self.y_fim, #vai escrver a linha e guardar o numero id
            fill=self.cor, 
            width=2
        )

    def eh_valida(self) -> bool:
        return (self.x_inicio, self.y_inicio) != (self.x_fim, self.y_fim)


class MaoLivre(Figuras): #classe so para desenhar livre

    def __init__(self, x_inicio, y_inicio, pontos, cor="black"):
        super().__init__(x_inicio, y_inicio, cor)
        self.pontos = pontos #guarda os pontos do desenho

    def iniciar(self, x, y):
        super().iniciar(x, y)
        self.pontos = [(x, y)] #primeiros a serem salvos
        
    def atualizar(self, x, y):
        self.pontos.append((x, y)) #adiciona pontos toda vez que o mouse se move

    def desenhar(self, canvas) -> None:
        # lista pra enviar para o canvas e atualiza a lista inteira usando todos os pontos
        if len(self.pontos) > 1:
            coordenadas = []
            for px, py in self.pontos:
                coordenadas.extend([px, py]) # vai colocando tudo em numa lista so
            self.id = canvas.create_line(
                *coordenadas,
                fill=self.cor,
                width=2
            )

    def eh_valida(self) -> bool:
        return len(self.pontos) >= 2

# Alias para compatibilidade com o main.py
Rabisco = MaoLivre
