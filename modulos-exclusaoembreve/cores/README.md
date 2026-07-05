# Módulo: Cores (Théo)

Este diretório está reservado para a implementação do controle de cores das figuras de forma orientada a objetos.

> [!IMPORTANT]
> **Aviso Importante**:
> 1. Remova qualquer código de debug/testes temporários do `main.py` antes de finalizar.
> 2. Após implementar sua parte e validar que está funcionando no `main.py`, **exclua este arquivo README.md**.

## O que você (Théo) precisa fazer:
Implemente a lógica para que as figuras possam ter cores individuais de borda e de preenchimento de maneira flexível.

Você pode criar uma classe ou interface que permita configurar e alterar essas propriedades dinamicamente, ou fornecer um gerenciador/paleta que controle a cor selecionada e aplique na criação das figuras.

### Ideia de implementação:
Você pode definir um Mixin (uma classe que adiciona comportamento a outras classes) chamada `Colorivel` ou uma classe base `ComCores`:

```python
from dataclasses import dataclass

@dataclass
class Colorivel:
    cor_borda: str = "black"
    cor_preenchimento: str = ""

    def definir_cores(self, cor_borda: str, cor_preenchimento: str):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
```

Isso ajudará a separar a responsabilidade de gerenciar cores do restante do código, garantindo **alta coesão** e **baixo acoplamento**!
