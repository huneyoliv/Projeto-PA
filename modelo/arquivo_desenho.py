import pickle

class ArquivoDesenho:
    # Classe responsável por ler e gravar arquivos usando a biblioteca pickle

    def salvar(self, figuras, caminho):
        # abre o arquivo no caminho escolhido em modo de escrita binaria ("wb")
        with open(caminho, "wb") as arquivo:
            # salva a lista de figuras inteira dentro do arquivo
            pickle.dump(figuras, arquivo)

    def carregar(self, caminho):
        # abre o arquivo no caminho escolhido em modo de leitura binaria ("rb")
        with open(caminho, "rb") as arquivo:
            # le e retorna a lista de figuras desserializada
            return pickle.load(arquivo)
