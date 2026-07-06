class ValidadorCores:
    """Classe responsável estritamente pela validação e consistência das cores do sistema."""

    @staticmethod
    def validar(nome_atributo: str, valor: any) -> any:
        """Verifica se os dados de cor são válidos (Método Estático)."""
        if nome_atributo == "cor_borda":
            if not isinstance(valor, str):
                raise TypeError("A cor da borda deve ser um texto (string).")
            if valor.strip() == "":
                return "black"  # Valor padrão caso venha vazio(THÉO)
        elif nome_atributo == "cor_preenchimento":
            if not isinstance(valor, str):
                raise TypeError("A cor de preenchimento deve ser um texto (string).")
        return valor