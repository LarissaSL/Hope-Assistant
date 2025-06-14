import webbrowser as wb

class ComandosPesquisa:

    def search(self, frase):
        # Usa o Navegador definido como Padrão
        wb.open('https://www.google.com/search?q=' + frase)

    def search_youtube(self, frase):
        # Usa o Navegador definido como Padrão
        wb.open('https://www.youtube.com/results?search_query=' + frase)
