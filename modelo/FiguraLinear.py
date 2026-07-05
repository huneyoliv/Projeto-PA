from dataclasses import dataclass
from abc import ABC
from modelo.figura import Figura #importar classe mãe (metodos abstratos)


@dataclass
class FiguraLinear(Figura, ABC): #criei para figuras que nao precisa de preenchimento 
    #atributo de cor e comportamento encapsulado
    cor: str

    def __setattr__(self, nome, valor): # pra controlar o que pode ser atribuido aos atributos

        if nome == "cor":    # ve qual atributo esta sendo alterado 
            if not isinstance(valor, str):
                raise TypeError("A cor deve ser um texto.")

            if valor.strip() == "":
                valor = "black"

        super().__setattr__(nome, valor) # chama o metodo para guardar o valor 