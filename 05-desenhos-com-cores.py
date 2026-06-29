from tkinter import *
from tkinter import ttk

# --- VARIAVEIS GLOBAIS GIGANTES QUE CONTROLAM TUDO ---
# Aqui eu guardo todos os desenhos que o usuario ja terminou de fazer.
# Cada desenho é salvo como uma tupla com tamanho diferente porque eu nao padronizei:
# - Retangulo: ("retangulo", x1, y1, x2, y2, cor_borda, cor_preenchimento)
# - Oval: ("oval", x1, y1, x2, y2, cor_borda, cor_preenchimento)
# - Circulo: ("circulo", x_centro, y_centro, raio, cor_borda, cor_preenchimento)
desenhos_salvos = []

# Variaveis para saber o que o usuario quer desenhar e com quais cores
tipo_desenho_atual = "retangulo"
cor_borda_atual = "black"
cor_preenchimento_atual = "white"

# Variaveis para guardar onde o usuario clicou com o mouse na tela
x_inicio = 0
y_inicio = 0
x_fim = 0
y_fim = 0
raio_calculado = 0.0

# --- FUNCOES PARA MUDAR O QUE VAI SER DESENHADO ---
# Essas funcoes sao chamadas quando o usuario clica nos botoes na tela.
# Elas mudam as variaveis globais e atualizam o texto de status para o usuario nao se perder.

def muda_para_retangulo():
    global tipo_desenho_atual
    tipo_desenho_atual = "retangulo"
    atualiza_texto_status()

def muda_para_oval():
    global tipo_desenho_atual
    tipo_desenho_atual = "oval"
    atualiza_texto_status()

def muda_para_circulo():
    global tipo_desenho_atual
    tipo_desenho_atual = "circulo"
    atualiza_texto_status()

def muda_cor_borda(cor):
    global cor_borda_atual
    cor_borda_atual = cor
    atualiza_texto_status()

def muda_cor_preenchimento(cor):
    global cor_preenchimento_atual
    cor_preenchimento_atual = cor
    atualiza_texto_status()

def atualiza_texto_status():
    # Esse label avisa o usuario o que ele selecionou atualmente,
    # senao ele desenha com a cor errada sem querer.
    lbl_status.config(text=f"Ferramenta: {tipo_desenho_atual.upper()} | Borda: {cor_borda_atual.upper()} | Preenchimento: {cor_preenchimento_atual.upper()}")


# --- LOGICA DOS EVENTOS DO MOUSE ---

def ao_clicar(event):
    # Quando clica com o botao esquerdo, eu salvo as coordenadas de inicio.
    # Uso global porque se nao colocar, o Python cria uma variavel local e nao salva no resto do codigo.
    global x_inicio, y_inicio
    x_inicio = event.x
    y_inicio = event.y

def ao_arrastar(event):
    # Conforme o usuario arrasta o mouse, eu preciso mostrar um "rascunho" do desenho.
    # O metodo que usei aqui é: apago tudo o que ta no canvas, redesenho todos os desenhos salvos
    # e depois desenho a figura temporaria por cima. É meio lento mas funciona bem.
    global x_fim, y_fim, raio_calculado
    x_fim = event.x
    y_fim = event.y
    
    # Redesenha o que ja estava salvo primeiro
    redesenhar_todos_salvos()
    
    # Agora desenha o temporario dependendo do tipo selecionado
    if tipo_desenho_atual == "retangulo":
        # Desenha o retangulo temporario com borda tracejada pra pessoa ver o tamanho
        canvas.create_rectangle(x_inicio, y_inicio, x_fim, y_fim, 
                                 outline=cor_borda_atual, fill=cor_preenchimento_atual, dash=(4, 2))
    
    elif tipo_desenho_atual == "oval":
        # Desenha a oval temporaria
        canvas.create_oval(x_inicio, y_inicio, x_fim, y_fim, 
                           outline=cor_borda_atual, fill=cor_preenchimento_atual, dash=(4, 2))
        
    elif tipo_desenho_atual == "circulo":
        # Pro circulo eu tenho que calcular o raio usando a formula da distancia entre dois pontos.
        # Usei (dx^2 + dy^2)^0.5 que é a mesma coisa que raiz quadrada, assim nao precisei importar o math.
        # O x_inicio e y_inicio sao o centro do circulo.
        raio_calculado = ((x_inicio - x_fim)**2 + (y_inicio - y_fim)**2) ** 0.5
        canvas.create_oval(x_inicio - raio_calculado, y_inicio - raio_calculado,
                           x_inicio + raio_calculado, y_inicio + raio_calculado,
                           outline=cor_borda_atual, fill=cor_preenchimento_atual, dash=(4, 2))

def ao_soltar(event):
    # Quando o usuario solta o mouse, o desenho atual deixa de ser rascunho e vai pra lista de salvos.
    global raio_calculado
    
    if tipo_desenho_atual == "retangulo":
        # Guarda na lista pra nao sumir depois
        desenhos_salvos.append(("retangulo", x_inicio, y_inicio, event.x, event.y, cor_borda_atual, cor_preenchimento_atual))
        
    elif tipo_desenho_atual == "oval":
        desenhos_salvos.append(("oval", x_inicio, y_inicio, event.x, event.y, cor_borda_atual, cor_preenchimento_atual))
        
    elif tipo_desenho_atual == "circulo":
        # Calcula o raio final no ponto onde soltou o mouse
        raio_calculado = ((x_inicio - event.x)**2 + (y_inicio - event.y)**2) ** 0.5
        desenhos_salvos.append(("circulo", x_inicio, y_inicio, raio_calculado, cor_borda_atual, cor_preenchimento_atual))
        
    # Redesenha tudo definitivo sem o tracejado
    redesenhar_todos_salvos()


# --- FUNCAO PARA REDESENHAR TUDO ---

def redesenhar_todos_salvos():
    # Esse metodo limpa a tela inteira do canvas com o "delete('all')" e depois faz um loop
    # gigante lendo cada tupla e desenhando de novo na tela com as cores certas.
    # É o jeito mais facil que achei pra nao duplicar desenho ou deixar rastro na tela.
    canvas.delete("all")
    
    for desenho in desenhos_salvos:
        tipo = desenho[0]
        if tipo == "retangulo":
            # Pega as posicoes e cores da tupla do retangulo
            # desenho[1] = x1, desenho[2] = y1, desenho[3] = x2, desenho[4] = y2, desenho[5] = borda, desenho[6] = fill
            canvas.create_rectangle(desenho[1], desenho[2], desenho[3], desenho[4], 
                                     outline=desenho[5], fill=desenho[6])
        elif tipo == "oval":
            # Pega as posicoes e cores da tupla da oval
            canvas.create_oval(desenho[1], desenho[2], desenho[3], desenho[4], 
                               outline=desenho[5], fill=desenho[6])
        elif tipo == "circulo":
            # Pega as posicoes da tupla do circulo (centro_x, centro_y, raio, borda, fill)
            cx = desenho[1]
            cy = desenho[2]
            r = desenho[3]
            canvas.create_oval(cx - r, cy - r, cx + r, cy + r, 
                               outline=desenho[4], fill=desenho[5])


# --- CODIGO DA TELA (INTERFACE GRAFICA) ---

root = Tk()
root.title("Desenhos Geométricos Coloridos - Sem POO")

# Criei um painel em cima para colocar todos os botoes organizados
painel_controles = Frame(root, bd=2, relief=SUNKEN)
painel_controles.pack(side=TOP, fill=X, padx=5, pady=5)

# --- SECAO DE FERRAMENTAS (FORMAS) ---
lbl_formas = Label(painel_controles, text="Formas:", font=("Arial", 10, "bold"))
lbl_formas.pack(side=LEFT, padx=5)

btn_ret = Button(painel_controles, text="Retângulo", command=muda_para_retangulo, bg="lightgray")
btn_ret.pack(side=LEFT, padx=2)

btn_ova = Button(painel_controles, text="Oval", command=muda_para_oval, bg="lightgray")
btn_ova.pack(side=LEFT, padx=2)

btn_cir = Button(painel_controles, text="Círculo", command=muda_para_circulo, bg="lightgray")
btn_cir.pack(side=LEFT, padx=2)

# --- SECAO DE BORDAS ---
lbl_bordas = Label(painel_controles, text="  |  Borda:", font=("Arial", 10, "bold"))
lbl_bordas.pack(side=LEFT, padx=5)

# Botoes de cores de borda
btn_b_preto = Button(painel_controles, text="Preto", fg="white", bg="black", command=lambda: muda_cor_borda("black"))
btn_b_preto.pack(side=LEFT, padx=2)

btn_b_verm = Button(painel_controles, text="Vermelho", fg="white", bg="red", command=lambda: muda_cor_borda("red"))
btn_b_verm.pack(side=LEFT, padx=2)

btn_b_verde = Button(painel_controles, text="Verde", fg="white", bg="green", command=lambda: muda_cor_borda("green"))
btn_b_verde.pack(side=LEFT, padx=2)

btn_b_azul = Button(painel_controles, text="Azul", fg="white", bg="blue", command=lambda: muda_cor_borda("blue"))
btn_b_azul.pack(side=LEFT, padx=2)

# --- SECAO DE PREENCHIMENTOS ---
lbl_preench = Label(painel_controles, text="  |  Preenchimento:", font=("Arial", 10, "bold"))
lbl_preench.pack(side=LEFT, padx=5)

# Botoes de cores de preenchimento. Coloquei "Sem preenchimento" como "" (vazio) pro tkinter nao pintar
btn_p_nada = Button(painel_controles, text="Nenhum", bg="white", command=lambda: muda_cor_preenchimento(""))
btn_p_nada.pack(side=LEFT, padx=2)

btn_p_amarelo = Button(painel_controles, text="Amarelo", bg="yellow", command=lambda: muda_cor_preenchimento("yellow"))
btn_p_amarelo.pack(side=LEFT, padx=2)

btn_p_rosa = Button(painel_controles, text="Rosa", bg="pink", command=lambda: muda_cor_preenchimento("pink"))
btn_p_rosa.pack(side=LEFT, padx=2)

btn_p_ciano = Button(painel_controles, text="Ciano", bg="cyan", command=lambda: muda_cor_preenchimento("cyan"))
btn_p_ciano.pack(side=LEFT, padx=2)

btn_p_branco = Button(painel_controles, text="Branco", bg="white", command=lambda: muda_cor_preenchimento("white"))
btn_p_branco.pack(side=LEFT, padx=2)


# --- LABEL DE STATUS ---
# Fica no fundo pra mostrar o que ta selecionado agora
lbl_status = Label(root, text="", bd=1, relief=SUNKEN, anchor=W, font=("Arial", 9, "italic"))
lbl_status.pack(side=BOTTOM, fill=X)
atualiza_texto_status() # Chama uma vez pra iniciar o texto da label

# --- CANVAS PARA DESENHO ---
canvas = Canvas(root, bg="white", width=800, height=600)
canvas.pack(fill=BOTH, expand=True)

# Liga os cliques do mouse nas funcoes de desenho
canvas.bind('<ButtonPress-1>', ao_clicar)
canvas.bind('<B1-Motion>', ao_arrastar)
canvas.bind('<ButtonRelease-1>', ao_soltar)

root.mainloop()
