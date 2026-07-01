from tkinter import *
from modulos.formas_geometricas.formas import Retangulo, Oval, Circulo

# Para manter o projeto flexível, tentamos importar o trabalho da Eline se ele existir.
# Se ainda não existir, o programa avisa de forma amigável!
try:
    from modulos.linhas_e_rabiscos.linhas import Linha, Rabisco
except ImportError:
    # Classes temporárias "mock" caso Eline ainda não tenha implementado.
    # Isso evita que o programa quebre para os outros integrantes do grupo!
    Linha = None
    Rabisco = None


class AplicativoDesenho:
    """
    Classe principal que gerencia a interface gráfica e o estado do desenho.
    Seguindo o SOLID (Alta Coesão), esta classe cuida apenas da interface e dos eventos.
    """
    def __init__(self, janela_root):
        self.root = janela_root
        self.root.title("Desenhos Geométricos Coloridos - Etapa 2")
        
        # --- ESTADO DO APLICATIVO ---
        self.desenhos_salvos = []  # Lista que guardará objetos do tipo Figura (Polimorfismo!)
        self.tipo_desenho_atual = "retangulo"
        self.cor_borda_atual = "black"
        self.cor_preenchimento_atual = "white"
        
        # Coordenadas auxiliares do mouse
        self.x_inicio = 0
        self.y_inicio = 0
        self.pontos_rabisco_temp = []
        
        # --- CRIAÇÃO DOS WIDGETS ---
        self.criar_interface()
        
    def criar_interface(self):
        # Painel Superior de Controles
        painel_controles = Frame(self.root, bd=2, relief=SUNKEN)
        painel_controles.pack(side=TOP, fill=X, padx=5, pady=5)
        
        # Seção de Formas
        lbl_formas = Label(painel_controles, text="Formas:", font=("Arial", 10, "bold"))
        lbl_formas.pack(side=LEFT, padx=5)
        
        Button(painel_controles, text="Retângulo", command=lambda: self.muda_ferramenta("retangulo"), bg="lightgray").pack(side=LEFT, padx=2)
        Button(painel_controles, text="Oval", command=lambda: self.muda_ferramenta("oval"), bg="lightgray").pack(side=LEFT, padx=2)
        Button(painel_controles, text="Círculo", command=lambda: self.muda_ferramenta("circulo"), bg="lightgray").pack(side=LEFT, padx=2)
        Button(painel_controles, text="Linha", command=lambda: self.muda_ferramenta("linha"), bg="lightgray").pack(side=LEFT, padx=2)
        Button(painel_controles, text="Rabisco", command=lambda: self.muda_ferramenta("rabisco"), bg="lightgray").pack(side=LEFT, padx=2)
        
        # Seção de Cores da Borda
        lbl_bordas = Label(painel_controles, text="  |  Cor Borda/Linha:", font=("Arial", 10, "bold"))
        lbl_bordas.pack(side=LEFT, padx=5)
        
        cores_borda = [("Preto", "black"), ("Vermelho", "red"), ("Verde", "green"), ("Azul", "blue")]
        for nome_cor, valor_cor in cores_borda:
            btn = Button(
                painel_controles, 
                text=nome_cor, 
                fg="white", 
                bg=valor_cor, 
                command=lambda vc=valor_cor: self.muda_cor_borda(vc)
            )
            btn.pack(side=LEFT, padx=2)
            
        # Seção de Cores de Preenchimento
        lbl_preench = Label(painel_controles, text="  |  Preenchimento:", font=("Arial", 10, "bold"))
        lbl_preench.pack(side=LEFT, padx=5)
        
        Button(painel_controles, text="Nenhum", bg="white", command=lambda: self.muda_cor_preenchimento("")).pack(side=LEFT, padx=2)
        
        cores_preenchimento = [("Amarelo", "yellow"), ("Rosa", "pink"), ("Ciano", "cyan"), ("Branco", "white")]
        for nome_cor, valor_cor in cores_preenchimento:
            btn = Button(
                painel_controles, 
                text=nome_cor, 
                bg=valor_cor, 
                command=lambda vc=valor_cor: self.muda_cor_preenchimento(vc)
            )
            btn.pack(side=LEFT, padx=2)
            
        # Barra de Status inferior
        self.lbl_status = Label(self.root, text="", bd=1, relief=SUNKEN, anchor=W, font=("Arial", 9, "italic"))
        self.lbl_status.pack(side=BOTTOM, fill=X)
        self.atualiza_texto_status()
        
        # Área de Desenho (Canvas)
        self.canvas = Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=BOTH, expand=True)
        
        # Eventos do mouse
        self.canvas.bind('<ButtonPress-1>', self.ao_clicar)
        self.canvas.bind('<B1-Motion>', self.ao_arrastar)
        self.canvas.bind('<ButtonRelease-1>', self.ao_soltar)
        
    def muda_ferramenta(self, ferramenta):
        self.tipo_desenho_atual = ferramenta
        self.atualiza_texto_status()
        
    def muda_cor_borda(self, cor):
        self.cor_borda_atual = cor
        self.atualiza_texto_status()
        
    def muda_cor_preenchimento(self, cor):
        self.cor_preenchimento_atual = cor
        self.atualiza_texto_status()
        
    def atualiza_texto_status(self):
        status = f"Ferramenta: {self.tipo_desenho_atual.upper()} | Borda: {self.cor_borda_atual.upper()} | Preenchimento: {self.cor_preenchimento_atual.upper()}"
        self.lbl_status.config(text=status)
        
    def ao_clicar(self, event):
        self.x_inicio = event.x
        self.y_inicio = event.y
        self.pontos_rabisco_temp = [(event.x, event.y)]
        
    def ao_arrastar(self, event):
        # Primeiro, redesenhamos todas as figuras já salvas para limpar o rascunho anterior
        self.redesenhar_todos_salvos()
        
        # Rascunho temporário tracejado da nova figura
        if self.tipo_desenho_atual == "retangulo":
            self.canvas.create_rectangle(
                self.x_inicio, self.y_inicio, event.x, event.y, 
                outline=self.cor_borda_atual, fill=self.cor_preenchimento_atual, dash=(4, 2)
            )
        elif self.tipo_desenho_atual == "oval":
            self.canvas.create_oval(
                self.x_inicio, self.y_inicio, event.x, event.y, 
                outline=self.cor_borda_atual, fill=self.cor_preenchimento_atual, dash=(4, 2)
            )
        elif self.tipo_desenho_atual == "circulo":
            # Calcula o raio dinamicamente usando a distância euclidiana (método estático!)
            raio = Retangulo.calcular_distancia(self.x_inicio, self.y_inicio, event.x, event.y)
            self.canvas.create_oval(
                self.x_inicio - raio, self.y_inicio - raio,
                self.x_inicio + raio, self.y_inicio + raio,
                outline=self.cor_borda_atual, fill=self.cor_preenchimento_atual, dash=(4, 2)
            )
        elif self.tipo_desenho_atual == "linha":
            self.canvas.create_line(
                self.x_inicio, self.y_inicio, event.x, event.y, 
                fill=self.cor_borda_atual, dash=(4, 2)
            )
        elif self.tipo_desenho_atual == "rabisco":
            self.pontos_rabisco_temp.append((event.x, event.y))
            if len(self.pontos_rabisco_temp) > 1:
                self.canvas.create_line(self.pontos_rabisco_temp, fill=self.cor_borda_atual, dash=(4, 2))
                
    def ao_soltar(self, event):
        figura_nova = None
        
        # Criação dos objetos das classes
        if self.tipo_desenho_atual == "retangulo":
            figura_nova = Retangulo(
                x_inicio=self.x_inicio,
                y_inicio=self.y_inicio,
                cor_borda=self.cor_borda_atual,
                cor_preenchimento=self.cor_preenchimento_atual,
                x_fim=event.x,
                y_fim=event.y
            )
        elif self.tipo_desenho_atual == "oval":
            figura_nova = Oval(
                x_inicio=self.x_inicio,
                y_inicio=self.y_inicio,
                cor_borda=self.cor_borda_atual,
                cor_preenchimento=self.cor_preenchimento_atual,
                x_fim=event.x,
                y_fim=event.y
            )
        elif self.tipo_desenho_atual == "circulo":
            # Usa o classmethod fábrica de Círculo para calcular o raio automaticamente
            figura_nova = Circulo.a_partir_de_centro_e_ponto(
                cx=self.x_inicio,
                cy=self.y_inicio,
                px=event.x,
                py=event.y,
                cor_borda=self.cor_borda_atual,
                cor_preenchimento=self.cor_preenchimento_atual
            )
        elif self.tipo_desenho_atual == "linha":
            if Linha is not None:
                # Quando a Eline terminar de implementar, o código usará a classe dela automaticamente!
                figura_nova = Linha(
                    x_inicio=self.x_inicio,
                    y_inicio=self.y_inicio,
                    x_fim=event.x,
                    y_fim=event.y,
                    cor=self.cor_borda_atual
                )
            else:
                print("Módulo 'Linha' ainda não foi implementado pela Eline!")
        elif self.tipo_desenho_atual == "rabisco":
            if Rabisco is not None:
                # Lógica para integrar a classe Rabisco da Eline
                figura_nova = Rabisco(
                    x_inicio=self.x_inicio,
                    y_inicio=self.y_inicio,
                    pontos=self.pontos_rabisco_temp,
                    cor=self.cor_borda_atual
                )
            else:
                print("Módulo 'Rabisco' ainda não foi implementado pela Eline!")

        # Validação e salvamento
        if figura_nova is not None and figura_nova.eh_valida():
            self.desenhos_salvos.append(figura_nova)
            
        self.redesenhar_todos_salvos()
        
    def redesenhar_todos_salvos(self):
        self.canvas.delete("all")
        
        # POLIMORFISMO: Não importa o tipo do objeto (Retangulo, Oval, Circulo, etc),
        # todos herdam de Figura e sabem se desenhar quando chamamos .desenhar().
        for desenho in self.desenhos_salvos:
            desenho.desenhar(self.canvas)


# --- INICIALIZAÇÃO DA APLICAÇÃO ---
if __name__ == "__main__":
    root = Tk()
    app = AplicativoDesenho(root)
    root.mainloop()
