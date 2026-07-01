# Módulo: Linhas e Rabiscos (Eline)

Este diretório está reservado para a implementação das linhas e rabiscos à mão livre seguindo a orientação a objetos.

> [!IMPORTANT]
> **Aviso Importante**:
> 1. Remova qualquer código de debug/testes temporários do `main.py` antes de finalizar.
> 2. Após implementar suas classes e validar que estão funcionando no `main.py`, **exclua este arquivo README.md**.

## O que você (Eline) precisa fazer:
Crie um arquivo Python (ex: `linhas.py` ou `rabiscos.py`) dentro desta pasta e implemente as classes:

1. **`Linha`**:
   - Deve herdar da classe base `Figura` (que está em `modulos/formas_geometricas/formas.py`).
   - Atributos adicionais: `x_fim` e `y_fim` (do tipo `float`), além de um atributo para a cor da linha (que pode vir da classe `FiguraSolida` ou ser criado diretamente na classe).
   - Implementar o método `desenhar(self, canvas)` chamando `canvas.create_line()`.
   - Implementar `eh_valida(self) -> bool` para garantir que a linha tem algum comprimento.

2. **`Rabisco`**:
   - Deve herdar de `Figura`.
   - Atributos adicionais: `pontos` (uma lista de tuplas contendo as coordenadas `(x, y)` por onde o mouse passou), além da cor.
   - Implementar `desenhar(self, canvas)` chamando `canvas.create_line(self.pontos)`.
   - Implementar `eh_valida(self) -> bool` verificando se há pelo menos 2 pontos na lista.

## Exemplo de estrutura esperada:
```python
from dataclasses import dataclass
from modulos.formas_geometricas.formas import Figura

@dataclass
class Linha(Figura):
    x_fim: float
    y_fim: float
    cor: str = "black"

    def desenhar(self, canvas) -> None:
        canvas.create_line(
            self.x_inicio, 
            self.y_inicio, 
            self.x_fim, 
            self.y_fim, 
            fill=self.cor
        )

    def eh_valida(self) -> bool:
        return (self.x_inicio, self.y_inicio) != (self.x_fim, self.y_fim)
```
