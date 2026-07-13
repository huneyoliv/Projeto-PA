from modelo.desenho import Desenho
from modelo.figura import Figura
from modelo.retangulo import Retangulo
from modelo.oval import Oval
from modelo.circulo import Circulo
from modelo.Linha import Linha
from modelo.MaoLivre import MaoLivre
from modelo.arquivo_desenho import ArquivoDesenho
from visao.janelaPaint import JanelaPaint
from controlador.controladorSelecao import ControladorSelecao


class ControladorPaint:
    # Controller: Centraliza a escuta de eventos e interações com o modelo e a visão
    def __init__(self, desenho: Desenho, visao: JanelaPaint):
        self.desenho = desenho
        self.visao = visao
        self.canvas = self.visao.canvas

        self.x_inicio = 0
        self.y_inicio = 0
        self.ult_x = 0
        self.ult_y = 0
        self.id_borracha_temp = None
        self.figura_atual = None  # guarda a mao livre em andamento

        # Instancia a classe de persistencia de arquivos
        self.arquivo = ArquivoDesenho()

        # Bind dos Eventos de Mouse no Canvas
        self.canvas.bind("<ButtonPress-1>", self.ao_clicar)
        self.canvas.bind("<B1-Motion>", self.ao_arrastar)
        self.canvas.bind("<ButtonRelease-1>", self.ao_soltar)
        self.canvas.bind("<Motion>", self.ao_mover)
        self.canvas.bind("<Leave>", self.ao_sair)

        # Bind dos Botões da View para o Controlador
        self.visao.btn_desfazer.config(command=self.desfazer)
        self.visao.btn_limpar.config(command=self.limpar_tudo)
        self.visao.btn_salvar.config(command=self.salvar)
        self.visao.btn_abrir.config(command=self.abrir)

        # Observa mudanças nas variáveis da visão para atualizar status
        self.visao.tipo_figura_var.trace_add("write", lambda *a: self._atualiza_status())
        self.visao.cor_borda_var.trace_add("write", lambda *a: self._atualiza_status())
        self.visao.cor_preenchimento_var.trace_add("write", lambda *a: self._atualiza_status())
        self._atualiza_status()

        # Instancia o controlador de selecao auxiliar
        self.controlador_selecao = ControladorSelecao(self.visao, self.desenho)

        # Atalhos de Teclado Globais no root para Arquivo e Edição
        root = self.visao.root
        root.bind("<Control-s>", lambda e: self.salvar())
        root.bind("<Control-S>", lambda e: self.salvar())
        root.bind("<Control-o>", lambda e: self.abrir())
        root.bind("<Control-O>", lambda e: self.abrir())
        root.bind("<Control-z>", lambda e: self.desfazer())
        root.bind("<Control-Z>", lambda e: self.desfazer())
        root.bind("<Control-n>", lambda e: self.limpar_tudo())
        root.bind("<Control-N>", lambda e: self.limpar_tudo())

        # Atalhos simples para seleção rápida de ferramentas
        root.bind("r", lambda e: self.visao.tipo_figura_var.set("retangulo"))
        root.bind("R", lambda e: self.visao.tipo_figura_var.set("retangulo"))
        root.bind("o", lambda e: self.visao.tipo_figura_var.set("oval"))
        root.bind("O", lambda e: self.visao.tipo_figura_var.set("oval"))
        root.bind("c", lambda e: self.visao.tipo_figura_var.set("circulo"))
        root.bind("C", lambda e: self.visao.tipo_figura_var.set("circulo"))
        root.bind("l", lambda e: self.visao.tipo_figura_var.set("linha"))
        root.bind("L", lambda e: self.visao.tipo_figura_var.set("linha"))
        root.bind("m", lambda e: self.visao.tipo_figura_var.set("maolivre"))
        root.bind("M", lambda e: self.visao.tipo_figura_var.set("maolivre"))
        root.bind("b", lambda e: self.visao.tipo_figura_var.set("borracha"))
        root.bind("B", lambda e: self.visao.tipo_figura_var.set("borracha"))
        root.bind("s", lambda e: self.visao.tipo_figura_var.set("selecao"))
        root.bind("S", lambda e: self.visao.tipo_figura_var.set("selecao"))

    def _atualiza_status(self):
        f = self.visao.tipo_figura_var.get().upper()
        b = self.visao.cor_borda_var.get().upper()
        p = self.visao.cor_preenchimento_var.get().upper()
        self.visao.atualiza_status(f"Ferramenta: {f} | Borda: {b} | Preenchimento: {p}")
        if self.visao.tipo_figura_var.get() != "borracha":
            self._limpar_indicador_borracha()
        if self.visao.tipo_figura_var.get() != "selecao":
            self.desenho.limpa_selecao()
            self.desenho.desenha_figuras(self.canvas)

    def ao_clicar(self, event):
        t = self.visao.tipo_figura_var.get()
        if t == "selecao":
            self.ult_x = event.x
            self.ult_y = event.y
            self.desenho.limpa_selecao()
            self.desenho.seleciona(event.x, event.y)
            self.desenho.desenha_figuras(self.canvas)
            return

        if t == "borracha":
            itens = self.canvas.find_overlapping(event.x - 3, event.y - 3, event.x + 3, event.y + 3)
            if itens:
                id_para_remover = itens[-1]
                if id_para_remover == self.id_borracha_temp and len(itens) > 1:
                    id_para_remover = itens[-2]
                if id_para_remover != self.id_borracha_temp:
                    self.desenho.figuras = [fig for fig in self.desenho.figuras if getattr(fig, "id", None) != id_para_remover]
                    self.desenho.desenha_figuras(self.canvas)
                    self.id_borracha_temp = None
                    self._atualizar_indicador_borracha(event.x, event.y)
            return

        self.x_inicio = event.x
        self.y_inicio = event.y

        if t == "maolivre":
            bc = self.visao.cor_borda_var.get()
            self.figura_atual = MaoLivre.a_partir_do_primeiro_ponto(event.x, event.y, bc)

    def ao_arrastar(self, event):
        t = self.visao.tipo_figura_var.get()
        if t == "selecao":
            fig_sel = self.desenho.selecionada()
            if fig_sel:
                fig_sel.mover(event.x - self.ult_x, event.y - self.ult_y)
                self.ult_x = event.x
                self.ult_y = event.y
                self.desenho.desenha_figuras(self.canvas)
            return

        if t == "borracha":
            self._atualizar_indicador_borracha(event.x, event.y)
            itens = self.canvas.find_overlapping(event.x - 3, event.y - 3, event.x + 3, event.y + 3)
            if itens:
                id_para_remover = itens[-1]
                if id_para_remover == self.id_borracha_temp and len(itens) > 1:
                    id_para_remover = itens[-2]
                if id_para_remover != self.id_borracha_temp:
                    self.desenho.figuras = [fig for fig in self.desenho.figuras if getattr(fig, "id", None) != id_para_remover]
                    self.desenho.desenha_figuras(self.canvas)
                    self.id_borracha_temp = None
                    self._atualizar_indicador_borracha(event.x, event.y)
            return

        bc = self.visao.cor_borda_var.get()
        pc = self.visao.cor_preenchimento_var.get()

        if t == "maolivre" and self.figura_atual:
            self.figura_atual.adicionar_ponto(event.x, event.y)
            self.desenho.desenha_figuras(self.canvas)
            self.figura_atual.desenha(self.canvas)
        else:
            self.desenho.desenha_figuras(self.canvas)
            if t == "retangulo":
                self.canvas.create_rectangle(self.x_inicio, self.y_inicio, event.x, event.y, outline=bc, fill=pc, dash=(4, 2))
            elif t == "oval":
                self.canvas.create_oval(self.x_inicio, self.y_inicio, event.x, event.y, outline=bc, fill=pc, dash=(4, 2))
            elif t == "circulo":
                raio = Figura.calcular_distancia(self.x_inicio, self.y_inicio, event.x, event.y)
                self.canvas.create_oval(self.x_inicio - raio, self.y_inicio - raio, self.x_inicio + raio, self.y_inicio + raio, outline=bc, fill=pc, dash=(4, 2))
            elif t == "linha":
                self.canvas.create_line(self.x_inicio, self.y_inicio, event.x, event.y, fill=bc, width=2, dash=(4, 2))

    def ao_soltar(self, event):
        t = self.visao.tipo_figura_var.get()
        if t == "selecao":
            return
        if t == "borracha":
            return

        figura_nova = None
        ki, yi = self.x_inicio, self.y_inicio
        bc = self.visao.cor_borda_var.get()
        pc = self.visao.cor_preenchimento_var.get()

        if t == "retangulo":
            figura_nova = Retangulo(ki, yi, bc, pc, event.x, event.y)
        elif t == "oval":
            figura_nova = Oval(ki, yi, bc, pc, event.x, event.y)
        elif t == "circulo":
            figura_nova = Circulo.a_partir_de_centro_e_ponto(ki, yi, event.x, event.y, bc, pc)
        elif t == "linha":
            figura_nova = Linha.a_partir_de_pontos(ki, yi, event.x, event.y, bc)
        elif t == "maolivre" and self.figura_atual:
            figura_nova = self.figura_atual
            self.figura_atual = None

        if figura_nova and not figura_nova.vazia():
            self.desenho.adiciona_figura(figura_nova)

        self.desenho.desenha_figuras(self.canvas)

    def ao_mover(self, event):
        if self.visao.tipo_figura_var.get() == "borracha":
            self._atualizar_indicador_borracha(event.x, event.y)
        else:
            self._limpar_indicador_borracha()

    def ao_sair(self, event):
        self._limpar_indicador_borracha()

    def _atualizar_indicador_borracha(self, x, y):
        r = 6
        if self.id_borracha_temp is None:
            self.id_borracha_temp = self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                outline="red", width=1, dash=(2, 2)
            )
        else:
            self.canvas.coords(self.id_borracha_temp, x - r, y - r, x + r, y + r)
            self.canvas.tag_raise(self.id_borracha_temp)

    def _limpar_indicador_borracha(self):
        if self.id_borracha_temp is not None:
            self.canvas.delete(self.id_borracha_temp)
            self.id_borracha_temp = None

    # Método para apagar o último desenho da tela (desfazer)
    def desfazer(self):
        if len(self.desenho.figuras) > 0:
            self.desenho.figuras.pop()  # remove o ultimo elemento da lista
            self.desenho.desenha_figuras(self.canvas)  # desenha de novo o que sobrou
            self.visao.atualiza_status("Última ação desfeita.")
        else:
            self.visao.atualiza_status("Nada para desfazer.")

    # Método para limpar a tela toda de uma vez
    def limpar_tudo(self):
        self.desenho.figuras.clear()  # esvazia a lista de figuras
        self.desenho.desenha_figuras(self.canvas)  # limpa a tela de fato
        self.visao.atualiza_status("Tela limpa com sucesso.")

    # Método para salvar o desenho atual em um arquivo .pkl
    def salvar(self):
        caminho = self.visao.pedir_caminho_salvar()  # pede o caminho para o usuario
        if caminho:  # se o usuario nao cancelou a janela
            import os
            self.arquivo.salvar(self.desenho.figuras, caminho)
            nome_arquivo = os.path.basename(caminho)  # extrai o nome do arquivo
            self.visao.definir_titulo(nome_arquivo)  # muda o titulo da janela para o nome do arquivo
            self.visao.atualiza_status(f"Desenho salvo com sucesso! Arquivo: {nome_arquivo}")

    # Método para carregar um desenho a partir de um arquivo .pkl
    def abrir(self):
        caminho = self.visao.pedir_caminho_abrir()  # pede o caminho para o usuario
        if caminho:  # se o usuario nao cancelou a janela
            import os
            self.desenho.figuras = self.arquivo.carregar(caminho)  # substitui a lista atual
            self.desenho.desenha_figuras(self.canvas)  # redesenha tudo na tela
            nome_arquivo = os.path.basename(caminho)  # extrai o nome do arquivo
            self.visao.definir_titulo(nome_arquivo)  # muda o titulo da janela para o nome do arquivo
            self.visao.atualiza_status(f"Desenho carregado com sucesso! Arquivo: {nome_arquivo}")
