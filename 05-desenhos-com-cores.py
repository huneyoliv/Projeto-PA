from tkinter import *
from tkinter import ttk

# --- VARIAVEIS GLOBAIS GIGANTES ---
# [Huney e Eline]: Lista que guarda todos os desenhos definitivos feitos no canvas.
desenhos_salvos = []

# [Huney]: Variaveis de selecao de ferramentas e cores atuais
tipo_desenho_atual = "retangulo"
cor_borda_atual = "black"
cor_preenchimento_atual = "white"

# [Eline]: Lista temporaria para acumular os pontos do rabisco conforme o mouse se move
pontos_rabisco_temp = []

# [Huney]: Variaveis auxiliares para guardar onde o clique comecou e terminou
x_inicio = 0
y_inicio = 0
x_fim = 0
y_fim = 0
raio_calculado = 0.0


# --- FUNCOES DE SELECAO (CONTROLES) ---

# [Huney]: Selecao de formas geométricas solidas
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

# [Eline]: Funcoes de selecao para ferramentas de traco livre e linhas
def muda_para_linha():
    global tipo_desenho_atual
    tipo_desenho_atual = "linha"
    atualiza_texto_status()

def muda_para_rabisco():
    global tipo_desenho_atual
    tipo_desenho_atual = "rabisco"
    atualiza_texto_status()

# [Huney]: Funcoes de configuracao de cores
def muda_cor_borda(cor):
    global cor_borda_atual
    cor_borda_atual = color_map(cor)
    atualiza_texto_status()

def muda_cor_preenchimento(cor):
    global cor_preenchimento_atual
    cor_preenchimento_atual = color_map(cor)
    atualiza_texto_status()

def color_map(cor):
    # Converte nomes de cores para facilitar o tkinter
    return cor

# [Huney]: Atualiza o texto informativo na tela
def atualiza_texto_status():
    lbl_status.config(text=f"Ferramenta: {tipo_desenho_atual.upper()} | Borda: {cor_borda_atual.upper()} | Preenchimento: {cor_preenchimento_atual.upper()}")


# --- EVENTOS DO MOUSE ---

# [Huney]: Evento quando o botao do mouse é clicado
def ao_clicar(event):
    global x_inicio, y_inicio, pontos_rabisco_temp
    x_inicio = event.x
    y_inicio = event.y
    
    # [Eline]: Inicializa o primeiro ponto do rabisco quando clica
    if tipo_desenho_atual == "rabisco":
        pontos_rabisco_temp = [(event.x, event.y)]

# [Huney & Eline]: Desenho temporario do rascunho enquanto arrasta o mouse
def ao_arrastar(event):
    global x_fim, y_fim, raio_calculado, pontos_rabisco_temp
    x_fim = event.x
    y_fim = event.y
    
    # [Huney]: Primeiro apaga tudo e desenha os salvos definitivos de novo
    redesenhar_todos_salvos()
    
    # --- Huney: Rascunho das figuras solidas ---
    if tipo_desenho_atual == "retangulo":
        # Metodo do Retangulo: Usa o ponto inicial do clique como um canto e a posicao atual do mouse como o canto oposto.
        canvas.create_rectangle(x_inicio, y_inicio, x_fim, y_fim, 
                                 outline=cor_borda_atual, fill=cor_preenchimento_atual, dash=(4, 2))
    
    elif tipo_desenho_atual == "oval":
        # Metodo da Oval: Define os limites da elipse a partir de um retangulo imaginario com os cantos inicial e final.
        canvas.create_oval(x_inicio, y_inicio, x_fim, y_fim, 
                           outline=cor_borda_atual, fill=cor_preenchimento_atual, dash=(4, 2))
        
    elif tipo_desenho_atual == "circulo":
        # Metodo do Circulo: Calcula o raio medindo a distancia euclidiana entre o ponto inicial (centro) e a borda.
        # Depois desenha o contorno circular usando a distancia igual para os quatro lados a partir do centro.
        raio_calculado = ((x_inicio - x_fim)**2 + (y_inicio - y_fim)**2) ** 0.5
        canvas.create_oval(x_inicio - raio_calculado, y_inicio - raio_calculado,
                           x_inicio + raio_calculado, y_inicio + raio_calculado,
                           outline=cor_borda_atual, fill=cor_preenchimento_atual, dash=(4, 2))
        
    # --- Eline: Rascunho das linhas e rabiscos ---
    elif tipo_desenho_atual == "linha":
        # Metodo da Linha: Traca um segmento reto ligando apenas o ponto inicial do clique ao ponto final do mouse.
        canvas.create_line(x_inicio, y_inicio, x_fim, y_fim, fill=cor_borda_atual, dash=(4, 2))
        
    elif tipo_desenho_atual == "rabisco":
        # Metodo do Rabisco: Salva todas as coordenadas do arrasto em uma lista e desenha linhas interligando cada ponto.
        pontos_rabisco_temp.append((event.x, event.y))
        if len(pontos_rabisco_temp) > 1:
            canvas.create_line(pontos_rabisco_temp, fill=cor_borda_atual, dash=(4, 2))

# [Huney & Eline]: Adiciona o desenho definitivo na lista quando solta o mouse
def ao_soltar(event):
    global raio_calculado, pontos_rabisco_temp
    
    # --- Huney: Salvando formas solidas ---
    if tipo_desenho_atual == "retangulo":
        desenhos_salvos.append(("retangulo", x_inicio, y_inicio, event.x, event.y, cor_borda_atual, cor_preenchimento_atual))
        
    elif tipo_desenho_atual == "oval":
        desenhos_salvos.append(("oval", x_inicio, y_inicio, event.x, event.y, cor_borda_atual, cor_preenchimento_atual))
        
    elif tipo_desenho_atual == "circulo":
        raio_calculado = ((x_inicio - event.x)**2 + (y_inicio - event.y)**2) ** 0.5
        desenhos_salvos.append(("circulo", x_inicio, y_inicio, raio_calculado, cor_borda_atual, cor_preenchimento_atual))
        
    # --- Eline: Salvando linhas e rabiscos ---
    elif tipo_desenho_atual == "linha":
        if (x_inicio, y_inicio) != (event.x, event.y):
            desenhos_salvos.append(("linha", x_inicio, y_inicio, event.x, event.y, cor_borda_atual))
            
    elif tipo_desenho_atual == "rabisco":
        if len(pontos_rabisco_temp) > 1:
            desenhos_salvos.append(("rabisco", pontos_rabisco_temp, cor_borda_atual))
        pontos_rabisco_temp = []
        
    # Redesenha a tela toda sem linhas tracejadas
    redesenhar_todos_salvos()


# --- DESENHAR TUDO ---

def redesenhar_todos_salvos():
    # Metodo de renderizacao: o canvas é apagado completamente e tudo é recriado de forma sequencial.
    canvas.delete("all")
    
    for desenho in desenhos_salvos:
        tipo = desenho[0]
        
        # --- Huney: Renderiza formas solidas com borda e preenchimento ---
        if tipo == "retangulo":
            canvas.create_rectangle(desenho[1], desenho[2], desenho[3], desenho[4], 
                                     outline=desenho[5], fill=desenho[6])
        elif tipo == "oval":
            canvas.create_oval(desenho[1], desenho[2], desenho[3], desenho[4], 
                               outline=desenho[5], fill=desenho[6])
        elif tipo == "circulo":
            cx, cy, r, cb, cp = desenho[1], desenho[2], desenho[3], desenho[4], desenho[5]
            canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=cb, fill=cp)
            
        # --- Eline: Renderiza linhas e rabiscos com a cor da linha ---
        elif tipo == "linha":
            canvas.create_line(desenho[1], desenho[2], desenho[3], desenho[4], fill=desenho[5])
        elif tipo == "rabisco":
            canvas.create_line(desenho[1], fill=desenho[2])


# --- INTERFACE GRAFICA ---

root = Tk()
root.title("Desenhos Geométricos Coloridos - Huney & Eline")

painel_controles = Frame(root, bd=2, relief=SUNKEN)
painel_controles.pack(side=TOP, fill=X, padx=5, pady=5)

# --- SECAO DE FORMAS (Huney & Eline) ---
lbl_formas = Label(painel_controles, text="Formas:", font=("Arial", 10, "bold"))
lbl_formas.pack(side=LEFT, padx=5)

# [Huney]
btn_ret = Button(painel_controles, text="Retângulo", command=muda_para_retangulo, bg="lightgray")
btn_ret.pack(side=LEFT, padx=2)

btn_ova = Button(painel_controles, text="Oval", command=muda_para_oval, bg="lightgray")
btn_ova.pack(side=LEFT, padx=2)

btn_cir = Button(painel_controles, text="Círculo", command=muda_para_circulo, bg="lightgray")
btn_cir.pack(side=LEFT, padx=2)

# [Eline]
btn_lin = Button(painel_controles, text="Linha", command=muda_para_linha, bg="lightgray")
btn_lin.pack(side=LEFT, padx=2)

btn_rab = Button(painel_controles, text="Rabisco", command=muda_para_rabisco, bg="lightgray")
btn_rab.pack(side=LEFT, padx=2)


# --- SECAO DE BORDAS/LINHAS (Huney) ---
lbl_bordas = Label(painel_controles, text="  |  Cor Borda/Linha:", font=("Arial", 10, "bold"))
lbl_bordas.pack(side=LEFT, padx=5)

btn_b_preto = Button(painel_controles, text="Preto", fg="white", bg="black", command=lambda: muda_cor_borda("black"))
btn_b_preto.pack(side=LEFT, padx=2)

btn_b_verm = Button(painel_controles, text="Vermelho", fg="white", bg="red", command=lambda: muda_cor_borda("red"))
btn_b_verm.pack(side=LEFT, padx=2)

btn_b_verde = Button(painel_controles, text="Verde", fg="white", bg="green", command=lambda: muda_cor_borda("green"))
btn_b_verde.pack(side=LEFT, padx=2)

btn_b_azul = Button(painel_controles, text="Azul", fg="white", bg="blue", command=lambda: muda_cor_borda("blue"))
btn_b_azul.pack(side=LEFT, padx=2)


# --- SECAO DE PREENCHIMENTOS (Huney) ---
lbl_preench = Label(painel_controles, text="  |  Preenchimento:", font=("Arial", 10, "bold"))
lbl_preench.pack(side=LEFT, padx=5)

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


# --- BARRA DE STATUS (Huney) ---
lbl_status = Label(root, text="", bd=1, relief=SUNKEN, anchor=W, font=("Arial", 9, "italic"))
lbl_status.pack(side=BOTTOM, fill=X)
atualiza_texto_status()

# --- CANVAS (Huney & Eline) ---
canvas = Canvas(root, bg="white", width=800, height=600)
canvas.pack(fill=BOTH, expand=True)

canvas.bind('<ButtonPress-1>', ao_clicar)
canvas.bind('<B1-Motion>', ao_arrastar)
canvas.bind('<ButtonRelease-1>', ao_soltar)

root.mainloop()
