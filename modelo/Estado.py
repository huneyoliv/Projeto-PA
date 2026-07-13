from abc import ABC, abstractmethod


class Estado(ABC): #modelo para outras classe, vou usar nas figuras 

    def __init__(self, desenho, canvas, visao):

        self.desenho = desenho #modelo que guarda as figuras 
        self.canvas = canvas 
        self.visao = visao

    @abstractmethod
    def clicar(self, event):
        pass

    @abstractmethod
    def arrastar(self, event):
        pass

    @abstractmethod

    def soltar(self, event):
        pass
    
