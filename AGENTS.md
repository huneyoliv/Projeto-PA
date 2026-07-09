# Agent Instructions for Projeto-PA (Paint MVC)

## Project Overview

**Projeto-PA** is a collaborative academic Paint application implementing the **MVC (Model-View-Controller)** pattern in **Brazilian Portuguese**. The application allows users to draw geometric shapes with customizable colors and borders using tkinter.

- **Team**: Eline Evelin Dos Anjos Oliveira, Théo Santos de Alcântara, Huney Victor de Santana Oliveira
- **Language**: Brazilian Portuguese (code, comments, variables)
- **Framework**: Python + tkinter
- **Architecture**: Clean MVC separation

## Language & Naming Conventions

### Critical: All Code Must Use Brazilian Portuguese

- **Variable names**: `tipo_figura`, `cor_borda`, `figuras`, `ao_clicar`
- **Method names**: `adiciona_figura()`, `atualiza_status()`, `ao_arrastar()`
- **Class names**: `Desenho`, `JanelaPaint`, `ControladorPaint`, `Figura`
- **Comments**: Always in Portuguese
- **UI labels**: Portuguese (e.g., "Retângulo", "Cor Borda", "Desfazer")

### Code Style

- **Naming convention**: `snake_case` for methods/variables, `PascalCase` for classes
- **Private methods**: Prefix with `_` (e.g., `_criar_painel()`, `_atualiza_status()`)
- **Type hints**: Use them (e.g., `def __init__(self, desenho: Desenho, visao: JanelaPaint)`)

### Do NOT use English

- ❌ `draw_shape()` → ✅ `desenha_forma()`
- ❌ `get_color()` → ✅ `obtem_cor()`
- ❌ `update_canvas()` → ✅ `atualiza_canvas()`
- ❌ `mouse_click` → ✅ `ao_clicar`

## Architecture

### Directory Structure

```
controlador/           # Controller: event handling & coordination
modelo/               # Model: data structures & business logic
visao/                # View: UI components & layouts
main.py              # Entry point (MVC initialization)
```

### MVC Pattern

- **Model (`modelo/`)**: Manages figures (Figura, Retangulo, Circulo, etc.) and drawing state (Desenho)
- **View (`visao/`)**: JanelaPaint contains UI layout, buttons, canvas, and status labels
- **Controller (`controlador/`)**: ControladorPaint handles all mouse/button events and coordinates model-view interaction

### Key Classes

- `Desenho`: Manages figure persistence (list of figures)
- `JanelaPaint`: tkinter UI with canvas, buttons, color controls
- `ControladorPaint`: Event routing (mouse clicks, drags, releases)
- `Figura` (base), `Retangulo`, `Circulo`, `Oval`, `Linha`, `MaoLivre`: Shape implementations

## Common Development Tasks

### Adding a New Shape Type

1. Create a new class in `modelo/` (e.g., `triangulo.py`) inheriting from `Figura`
2. Import in `controlador/controladorPaint.py`
3. Add to `_atualiza_status()` and event handlers in controller
4. Add button to `_criar_painel()` in `visao/janelaPaint.py` with Portuguese label

### Modifying UI Elements

- **Colors**: Update button definitions in `_criar_painel()` with tuple `(nome_português, código_cor)`
- **Buttons**: Use Portuguese text (e.g., "Retângulo", "Preenchimento")
- **Status messages**: Update via `self.visao.atualiza_status(mensagem_português)`

### Event Handling

- Mouse events: `ao_clicar()`, `ao_arrastar()`, `ao_soltar()`, `ao_mover()`, `ao_sair()`
- tkinter StringVar observation: `trace_add("write", callback)`
- Canvas bindings: Use `<ButtonPress-1>`, `<B1-Motion>`, `<ButtonRelease-1>`, `<Motion>`, `<Leave>`

## Running the Application

```bash
python main.py
```

The application initializes MVC components in `main.py` and launches the tkinter main loop.

## Important Notes

- **No English in code**: This is a Portuguese-language project; maintain consistency
- **MVC separation**: Keep model logic separate from UI and event handling
- **Refactoring ongoing**: Code in `modulos-exclusaoembreve/` is deprecated; do not use
- **Type hints**: Add them when implementing new features for better code clarity
