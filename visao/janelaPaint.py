from tkinter import Tk, Frame, Label, Button, Canvas, StringVar, Menu, TOP, BOTTOM, LEFT, X, BOTH, SUNKEN, W, colorchooser, filedialog


class JanelaPaint:
    # View: Contém apenas a estrutura de layouts e declaração de componentes visuais
    def __init__(self):
        self.root = Tk()
        # O título padrão inicial é "Novo design*" caso nenhum arquivo tenha sido aberto ou salvo ainda
        self.root.title("Novo design*")

        self.tipo_figura_var = StringVar(self.root, value="retangulo")
        self.cor_borda_var = StringVar(self.root, value="black")
        self.cor_preenchimento_var = StringVar(self.root, value="white")

        self._criar_painel()
        self._criar_status()
        self._criar_canvas()
        self._criar_menu_superior()

    def _criar_painel(self):
        self.painel_principal = Frame(self.root, bd=2, relief=SUNKEN)
        self.painel_principal.pack(side=TOP, fill=X, padx=5, pady=5)

        self.linha1 = Frame(self.painel_principal)
        self.linha1.pack(side=TOP, fill=X, pady=2)
        self.linha2 = Frame(self.painel_principal)
        self.linha2.pack(side=TOP, fill=X, pady=2)

        # Subframe: Arquivo
        self.frame_arquivo = Frame(self.linha1)
        Label(self.frame_arquivo, text="Arquivo:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        self.btn_abrir = Button(self.frame_arquivo, text="Abrir", bg="lightgray")
        self.btn_abrir.pack(side=LEFT, padx=2)
        self.btn_salvar = Button(self.frame_arquivo, text="Salvar", bg="lightgray")
        self.btn_salvar.pack(side=LEFT, padx=2)

        # Subframe: Ações
        self.frame_acoes = Frame(self.linha1)
        Label(self.frame_acoes, text="Ações:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        self.btn_desfazer = Button(self.frame_acoes, text="Desfazer", bg="lightgray")
        self.btn_desfazer.pack(side=LEFT, padx=2)
        self.btn_limpar = Button(self.frame_acoes, text="Limpar Tudo", bg="lightgray")
        self.btn_limpar.pack(side=LEFT, padx=2)

        # Subframe: Formas
        self.frame_formas = Frame(self.linha1)
        Label(self.frame_formas, text="Formas:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        for texto, chave in [("Retângulo", "retangulo"), ("Oval", "oval"), ("Círculo", "circulo"), ("Linha", "linha"), ("Mão Livre", "maolivre"), ("Borracha", "borracha"), ("Seleção", "selecao")]:
            Button(self.frame_formas, text=texto, command=lambda c=chave: self.tipo_figura_var.set(c), bg="lightgray").pack(side=LEFT, padx=2)

        # Subframe: Cor Borda
        self.frame_borda = Frame(self.linha2)
        Label(self.frame_borda, text="Cor Borda/Linha:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        for nome, cor in [("Preto", "black"), ("Vermelho", "red"), ("Verde", "green"), ("Azul", "blue"), ("Laranja", "orange"), ("Roxo", "purple")]:
            fg_color = "black" if cor in ["orange"] else "white"
            Button(self.frame_borda, text=nome, fg=fg_color, bg=cor, command=lambda c=cor: self.cor_borda_var.set(c)).pack(side=LEFT, padx=2)
        Button(self.frame_borda, text="Outra...", bg="lightgray", command=self.selecionar_cor_borda_personalizada).pack(side=LEFT, padx=2)

        # Subframe: Cor Preenchimento
        self.frame_preenchimento = Frame(self.linha2)
        Label(self.frame_preenchimento, text="Preenchimento:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        Button(self.frame_preenchimento, text="Nenhum", bg="white", command=lambda: self.cor_preenchimento_var.set("")).pack(side=LEFT, padx=2)
        for nome, cor in [("Amarelo", "yellow"), ("Rosa", "pink"), ("Ciano", "cyan"), ("Branco", "white"), ("Cinza", "gray"), ("Marrom", "brown")]:
            fg_color = "black" if cor in ["yellow", "pink", "cyan", "white"] else "white"
            Button(self.frame_preenchimento, text=nome, fg=fg_color, bg=cor, command=lambda c=cor: self.cor_preenchimento_var.set(c)).pack(side=LEFT, padx=2)
        Button(self.frame_preenchimento, text="Outra...", bg="lightgray", command=self.selecionar_cor_preenchimento_personalizada).pack(side=LEFT, padx=2)

        self.layout_atual = None
        self.root.bind("<Configure>", self._ao_redimensionar)

    def _ao_redimensionar(self, event=None):
        if event and event.widget != self.root:
            return

        largura = self.root.winfo_width()

        # Se a janela for menor que 960px, empilha verticalmente as seções para não cortar
        if largura < 960:
            if self.layout_atual != "compacto":
                self.layout_atual = "compacto"
                self.frame_arquivo.pack_forget()
                self.frame_acoes.pack_forget()
                self.frame_formas.pack_forget()
                self.frame_borda.pack_forget()
                self.frame_preenchimento.pack_forget()

                self.frame_arquivo.pack(in_=self.linha1, side=TOP, anchor=W, pady=2)
                self.frame_acoes.pack(in_=self.linha1, side=TOP, anchor=W, pady=2)
                self.frame_formas.pack(in_=self.linha1, side=TOP, anchor=W, pady=2)
                self.frame_borda.pack(in_=self.linha2, side=TOP, anchor=W, pady=2)
                self.frame_preenchimento.pack(in_=self.linha2, side=TOP, anchor=W, pady=2)
        else:
            if self.layout_atual != "normal":
                self.layout_atual = "normal"
                self.frame_arquivo.pack_forget()
                self.frame_acoes.pack_forget()
                self.frame_formas.pack_forget()
                self.frame_borda.pack_forget()
                self.frame_preenchimento.pack_forget()

                self.frame_arquivo.pack(in_=self.linha1, side=LEFT, padx=5, pady=2)
                self.frame_acoes.pack(in_=self.linha1, side=LEFT, padx=15, pady=2)
                self.frame_formas.pack(in_=self.linha1, side=LEFT, padx=15, pady=2)
                self.frame_borda.pack(in_=self.linha2, side=LEFT, padx=5, pady=2)
                self.frame_preenchimento.pack(in_=self.linha2, side=LEFT, padx=15, pady=2)

    def _criar_status(self):
        self.lbl_status = Label(self.root, text="", bd=1, relief=SUNKEN, anchor=W, font=("Arial", 9, "italic"))
        self.lbl_status.pack(side=BOTTOM, fill=X)

    def _criar_canvas(self):
        self.canvas = Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=BOTH, expand=True)

    def atualiza_status(self, texto):
        self.lbl_status.config(text=texto)

    # Altera o título exibido na barra superior da janela do paint
    def definir_titulo(self, titulo):
        self.root.title(titulo)

    # Abre a janelinha do sistema para escolher uma cor de contorno/linha personalizada
    def selecionar_cor_borda_personalizada(self):
        cor = colorchooser.askcolor(title="Escolha a cor da Borda/Linha", parent=self.root)
        if cor[1]:  # se o usuario nao cancelar e escolher uma cor valida
            self.cor_borda_var.set(cor[1])  # atualiza a cor de borda selecionada

    # Abre a janelinha do sistema para escolher uma cor de preenchimento personalizada
    def selecionar_cor_preenchimento_personalizada(self):
        cor = colorchooser.askcolor(title="Escolha a cor do Preenchimento", parent=self.root)
        if cor[1]:  # se o usuario nao cancelar e escolher uma cor valida
            self.cor_preenchimento_var.set(cor[1])  # atualiza a cor de preenchimento

    # Abre a janelinha de "Salvar como" e retorna o caminho escolhido pelo estudante
    def pedir_caminho_salvar(self):
        titulo_atual = self.root.title()
        # Se for o titulo padrao de novo design, removemos o "*" porque nao eh um caractere valido para arquivos
        if titulo_atual == "Novo design*":
            nome_sugerido = "Novo design"
        else:
            nome_sugerido = titulo_atual

        return filedialog.asksaveasfilename(
            defaultextension=".teh",
            filetypes=[("Arquivo de Desenho", "*.teh")],
            initialfile=nome_sugerido,
            title="Salvar desenho"
        )

    # Abre a janelinha de "Abrir arquivo" e retorna o caminho do arquivo selecionado
    def pedir_caminho_abrir(self):
        return filedialog.askopenfilename(
            filetypes=[("Arquivo de Desenho", "*.teh")],
            title="Abrir desenho"
        )

    # Cria a barra de menus do sistema na parte superior
    def _criar_menu_superior(self):
        barra_menus = Menu(self.root)
        self.root.config(menu=barra_menus)

        # Menu: Arquivo
        menu_arquivo = Menu(barra_menus, tearoff=0)
        barra_menus.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Novo (Ctrl+N)", command=lambda: self.btn_limpar.invoke())
        menu_arquivo.add_command(label="Abrir... (Ctrl+O)", command=lambda: self.btn_abrir.invoke())
        menu_arquivo.add_command(label="Salvar (Ctrl+S)", command=lambda: self.btn_salvar.invoke())
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.root.quit)

        # Menu: Editar
        menu_editar = Menu(barra_menus, tearoff=0)
        barra_menus.add_cascade(label="Editar", menu=menu_editar)
        menu_editar.add_command(label="Desfazer (Ctrl+Z)", command=lambda: self.btn_desfazer.invoke())

        # Menu: Exibir
        menu_exibir = Menu(barra_menus, tearoff=0)
        barra_menus.add_cascade(label="Exibir", menu=menu_exibir)
        menu_exibir.add_command(label="Barra de Status (Ativa)", state="disabled")

        # Menu: Ajuda
        menu_ajuda = Menu(barra_menus, tearoff=0)
        barra_menus.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Sobre o Paint...", command=self.mostrar_sobre)

    def mostrar_sobre(self):
        from tkinter import Toplevel, Label, Frame, TOP, LEFT, BOTH
        sobre = Toplevel(self.root)
        sobre.title("Sobre o Paint")
        sobre.geometry("680x320")
        sobre.resizable(False, False)
        sobre.transient(self.root)
        sobre.grab_set()

        sobre.configure(bg="white")

        container = Frame(sobre, bg="white")
        container.pack(fill=BOTH, expand=True, padx=15, pady=15)

        ascii_art = """                                    @@@@@@@@@@@                       
                                 @@@           @@@                    
                               @@                @@@                  
                             @@@                   @@                 
                             @@                     @@                
                            @@        @@@@@@        @@@               
                            @@       @@@   @@@@@@@@@@@@               
                            @@       @@                               
 @@@@@@@@@@      @@@@@@@@@@@@@       @@@@@@@@@@@@@@@@@@@@@@@@@        
@@       @@    @@                                           @@        
@@       @@    @@                                           @@        
@@       @@    @@        @@@@@       @@@@@@@                @@        
@@       @@    @@        @@ @@       @@  @@                @@         
@@       @@    @@        @@ @@       @@  @@        @@@@@@@@@          
@@       @@    @@        @@ @@       @@  @@       @@                  
@@       @@@   @@        @@ @@       @@  @@       @@@                 
@@         @@@@@        @@  @@       @@  @@          @@@@@@@@@        
 @@                     @@  @@       @@   @@                  @@@     
  @@                  @@@   @@       @@    @@                   @@@   
   @@@               @@     @@       @@     @@@@                  @@  
     @@@@@       @@@@       @@@@@@@@@@@        @@@@@@@@@@          @@ 
         @@@@@@@@                                       @@@        @@ 
                                                          @@       @@ 
                                            @@@@@@@@@@@@@@@        @@ 
                                          @@                       @@ 
                                          @@                      @@  
                                          @@                    @@@   
                                          @@                 @@@@     
                                          @@@@@@@@@@@@@@@@@@@         """

        lbl_art = Label(container, text=ascii_art, font=("Consolas", 6), bg="white", fg="black", justify=LEFT)
        lbl_art.pack(side=LEFT, padx=(0, 15))

        frame_info = Frame(container, bg="white")
        frame_info.pack(side=LEFT, fill=BOTH, expand=True)

        txt_info = "Desenvolvido por:\n\nTheo Santos\nEline Anjos\nHuney Oliveira"
        lbl_info = Label(frame_info, text=txt_info, font=("Arial", 9, "bold"), bg="white", fg="black", justify=LEFT, anchor="w")
        lbl_info.pack(side=TOP, fill=BOTH, expand=True)