from dataclasses import dataclass
from abc import ABC
from modelo.figura import Figura


@dataclass
class FiguraSolida(Figura, ABC):
    # Atributos de cor e comportamento encapsulado
    cor_borda: str
    cor_preenchimento: str

    def __setattr__(self, nome, valor):
        if nome == "cor_borda":
            if not isinstance(valor, str):
                raise TypeError("A cor da borda deve ser texto.")
            if valor.strip() == "":
                valor = "black"
        elif nome == "cor_preenchimento":
            if not isinstance(valor, str):
                raise TypeError("A cor de preenchimento deve ser texto.")
        super().__setattr__(nome, valor)
