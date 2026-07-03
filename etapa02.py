from tkinter import *

#-------classe mãe --------# colocar aqui o que todas possuem em comum

class Figuras:  #classe abstrata
    def __init__(self, canvas):  #metodo construtor
        self.canvas = canvas #guardando dentro do objeto
        self.id = None # id vazio mas posso usar para mexer na figura(acho)
        self.x1 = 0
        self.y1 = 0 #formam um ponto

   
    def iniciar(self, x, y): # posicao atual do mouse na vertical e na horizontal 
        self.x1 = x 
        self.y1 = y
        
    def atualizar(self, x2, y2): #atualiza a posição das figuras 
        self.canvas.coords(self.id,
                           self.x1,
                           self.y1,
                           x2,y2)
    def mudar_cor(self, cor):
        self.canvas.itemconfig(self.id, fill=cor) # modificar(itemconfig) as propriedades de um item que ja existe | contorno linha

    def mover(self, dx, dy):  #move as formas 
        self.canvas.move(self.id, dx, dy)

#-------classes filhas ------
class Linha(Figuras): #criar uma classe so para linhas 
    
    def __init__(self, canvas):
        super().__init__(canvas)
        
    def criar(self, x1, y1,x2,y2):
        self.id = self.canvas.create_line(x1, y1, x2, y2, #vai escrver a linha e guardar o numero id
                                          fill= "black", 
                                          width=2)
class MaoLivre(Figuras): #classe so para desenhar livre

    def __init__(self, canvas):
        super().__init__(canvas)
        
        self.pontos = [] #guarda os pontos do desenho

    def iniciar(self, x, y):
        super().iniciar(x,y)
        self.pontos = [(x, y)] #primeiros a serem salvos

    def criar(self, x1,y1,x2,y2):
        self.id = self.canvas.create_line(x1, y1, x1, y1,
                                          fill="black",
                                          width=2)
        
    def atualizar(self, x, y):
            self.pontos.append((x,y)) #adiciona pontos toda vez que o mouse se move

            coordenadas = [] # lista pra enviar para o canvas

            for px, py in self.pontos:
                coordenadas.extend([px,py]) # vai colocando tudo em numa lista so

            self.canvas.coords(self.id, *coordenadas) #atualiza a lista inteira usando todos os pontos


class Aplicacoes: # vai gerenciar a janela, canvas e figuras 

    def __init__(self, root):
 
        self.root = root #janela principal
        #p/interagir
       #--------------------
        self.tipo = StringVar()
        self.tipo.set("Linha") #opção inicial

        frame = Frame(root) #organiza os botões
        frame.pack()

        Radiobutton(frame,                     #botao de seleçao unica para mao livre e linha que usam a mesma variavel
                    text= "Linha",
                    variable=self.tipo,
                    value="Linha").pack(side=LEFT)
        Radiobutton(frame,
                    text= "Mão Livre",
                    variable=self.tipo,
                    value="MaoLivre").pack(side=LEFT)
        
        self.canvas = Canvas(self.root,width =1680, height =800)
        self.canvas.pack(fill=BOTH, expand=True) #organizador visual(layout)                
       
        self.figuras = [] # pra guardar os ids das figuras 
        self.figura = None #guarda a linha que estou desenhando"limpa a refe"
        #self.tipo = "Linha"  #ou circulo #pra escolher o babado 
        self.canvas.bind("<Button-1>", self.iniciar_figura) #clique
        self.canvas.bind("<B1-Motion>", self.arrastar_figura) #arrasta
        self.canvas.bind("<ButtonRelease-1>", self.finalizar_figura) #solta

    def criar_figura(self,x,y) : #decide qual tipo de desenho criar 
        if self.tipo.get() == "Linha":
            return Linha(self.canvas)
        
        elif self.tipo.get() == "MaoLivre":
            return MaoLivre(self.canvas)
        return 
    
    def iniciar_figura(self, event):  #executa quando clica, crio objeto, salva posição inicial
        self.figura = self.criar_figura(event.x, event.y)

        self.figura.iniciar(event.x, event.y)
        self.figura.criar(event.x, event.y, event.x, event.y)
   
    def arrastar_figura(self, event): # muda a posição da linha em tempo real(eu acho)
        self.figura.atualizar(event.x, event.y)

    def finalizar_figura(self, event):   #salva a linha desenhada numa lista
        self.figuras.append(self.figura)
        self.figura = None

    def executar(self): #inicia o Tkinter
        self.root.mainloop()

#---------- XXXXXXXXXXX ----------#
root = Tk()
app = Aplicacoes(root) # para poder criar dentros da janela(root)
app.executar()