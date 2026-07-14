class ControladorSelecao:
    # Controlador auxiliar responsável pelos atalhos de teclado e cores da figura selecionada
    def __init__(self, visao, desenho):
        self.visao = visao
        self.desenho = desenho
        
        # Binds de Teclado no root para manipulação de camadas, cópia e deleção
        root = self.visao.root
        root.bind("<Up>", self._executar(self.desenho.selecionada_para_topo))
        root.bind("<Down>", self._executar(self.desenho.selecionada_para_fundo))
        root.bind("<Left>", self._executar(self.desenho.selecionada_para_tras))
        root.bind("<Right>", self._executar(self.desenho.selecionada_para_frente))
        root.bind("<Control-c>", self._executar(self.desenho.copiar_selecionada))
        root.bind("<Control-C>", self._executar(self.desenho.copiar_selecionada))
        root.bind("<Control-v>", self._executar(self.desenho.colar))
        root.bind("<Control-V>", self._executar(self.desenho.colar))
        root.bind("<Delete>", self._executar(self.desenho.apaga_selecionada))

        # Atualizações dinâmicas de cores via paleta ao mudar as variáveis
        self.visao.cor_borda_var.trace_add("write", lambda *a: self.atualiza_cor_linha())
        self.visao.cor_preenchimento_var.trace_add("write", lambda *a: self.atualiza_cor_preenchimento())

    def atualiza_cor_linha(self):
        f = self.desenho.selecionada()
        if f is not None:
            # Se for figura de contorno unico (MaoLivre, Linha) ela usa o atributo 'cor'
            if hasattr(f, "cor"):
                f.cor = self.visao.cor_borda_var.get()
            elif hasattr(f, "cor_borda"):
                f.cor_borda = self.visao.cor_borda_var.get()
            self.desenho.desenha_figuras(self.visao.canvas)

    def atualiza_cor_preenchimento(self):
        f = self.desenho.selecionada()
        if f is not None and hasattr(f, "cor_preenchimento"):
            f.cor_preenchimento = self.visao.cor_preenchimento_var.get()
            self.desenho.desenha_figuras(self.visao.canvas)

    def _executar(self, atua):
        def acao(event):
            atua()
            self.desenho.desenha_figuras(self.visao.canvas)
        return acao
