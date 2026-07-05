from modelo.desenho import Desenho
from visao.janelaPaint import JanelaPaint
from controlador.controladorPaint import ControladorPaint

if __name__ == "__main__":
    # Inicializa o MVC puro conforme o padrão do professor
    visao = JanelaPaint()
    desenho = Desenho()
    controlador = ControladorPaint(desenho, visao)
    visao.root.mainloop()
