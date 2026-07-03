from tkinter import Tk
from modulos.janela.aplicativo import AplicativoDesenho

if __name__ == "__main__":
    # Ponto de entrada do programa que cria a janela e inicia o loop principal
    root = Tk()
    AplicativoDesenho(root)
    root.mainloop()
