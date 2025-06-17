import os

class ComandosLembretes:

    def __init__(self, arquivo_lembretes='anotacao.txt'):
        self.arquivo_lembretes = arquivo_lembretes
        self._criar_arquivo_se_nao_existir()

    def _criar_arquivo_se_nao_existir(self):
        if not os.path.exists(self.arquivo_lembretes):
            with open(self.arquivo_lembretes, 'w', encoding='utf-8') as arquivo:
                arquivo.write('')

    def adicionar_lembrete(self, texto_lembrete):
        try:
            lembrete_formatado = f"{texto_lembrete.strip()}\n"

            with open(self.arquivo_lembretes, 'a', encoding='utf-8') as arquivo:
                arquivo.write(lembrete_formatado)
            return True

        except Exception as e:
            print(f"Erro ao salvar lembrete: {e}")
            return False

    def ler_lembretes(self):
        try:
            with open(self.arquivo_lembretes, 'r', encoding='utf-8') as arquivo:
                lembretes = arquivo.readlines()

            # Remove linhas vazias e quebras de linha desnecessárias
            lembretes = [lembrete.strip() for lembrete in lembretes if lembrete.strip()]
            return lembretes

        except Exception as e:
            print(f"Erro ao ler lembretes: {e}")
            return []

    def tem_lembretes(self):
        lembretes = self.ler_lembretes()
        return len(lembretes) > 0

    def contar_lembretes(self):
        return len(self.ler_lembretes())

    def limpar_lembretes(self):
        try:
            with open(self.arquivo_lembretes, 'w', encoding='utf-8') as arquivo:
                arquivo.write('')
            return True
        except Exception as e:
            print(f"Erro ao limpar lembretes: {e}")
            return False