from tkinter import *
from tkinter import ttk

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova

    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("Linha", (event.x, event.y, event.x, event.y))
        
    elif tipo_figura_var.get() == "Rabisco":
        figura_nova=("Rabisco", [(event.x, event.y)])

    else: #circulo
        figura_nova = ("Círculo", (event.x, event.y, 0))


# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova

    print(tipo_figura_var.get())
    fig, valores = figura_nova
    if fig == "Linha":
        figura_nova = ("Linha", (valores[0], valores [1], event.x, event.y))

    elif fig == "Rabisco":
        valores.append((event.x, event.y))

    else:  #circulo
        x, y,_ = valores
        raio = ((event.x - x) ** 2 + (event.y - y ) ** 2) ** 0.5
        figura_nova = ("Círculo", (x, y, raio))


    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event): 
    if not incompleta(figura_nova): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        figuras.append(figura_nova) 

    desenhar_figuras()


def desenhar_figuras():
    canvas.delete("all")

    for fig, values in figuras:

        if fig == "Linha":
            canvas.create_line(values[0], values[1], values[2], values[3])
        elif fig == "Rabisco":
            canvas.create_line(values) 

        else: #circulo
            x, y, r = values
            canvas.create_oval(x-r, y-r, x + r, y + r)

def desenhar_figura_nova():
    fig, values = figura_nova

    if fig == "Linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2))
   
    elif fig == "Rabisco":
        canvas.create_line(values, dash= (4, 2))    

    else : #circulo
        x, y, r = values
        canvas.create_oval(x - r, y - r, x + r, dash=(4, 2))


def incompleta(figura):
    fig, values = figura
    if fig == "Linha":
        return (values[0], values[1]) == (values[2], values[3])
    elif fig == "Rabisco": # fig == "rabisco"
        return len(values) <= 1
    else:
        return values [2] == 0


#******* MAIN *******#

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras

root = Tk()
frame = Frame(root)

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5} 

# label
label = ttk.Label(frame,  text='Linha, Rabisco ou Círculo:')
label.grid(column=0, row=0, sticky=W, **paddings)

# option menu # adicionar novas figuras aqui
tipo_figura_var = StringVar(root) # Guarda o tipo de figura selecionado no option menu 
option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                             "Linha", "Linha", "Rabisco", "Círculo")
option_menu.grid(column=1, row=0, sticky=W, **paddings)

# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=1, columnspan=2, sticky=W, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()

