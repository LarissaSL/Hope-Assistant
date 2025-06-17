import webbrowser as wb
import requests
from dotenv import load_dotenv
import os

class ComandosPesquisa:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")

    def search(self, frase):
        wb.open('https://www.google.com/search?q=' + frase)

    def search_youtube(self, frase):
        wb.open('https://www.youtube.com/results?search_query=' + frase)

    def search_model(self, frase):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [
                {"role": "system", "content": "Você é um assistente de busca útil e que apenas o que lhe foi perguntado. Com poucas frases, palavras e apenas o essencial."},
                {"role": "user", "content": f"O que você pode me dizer sobre: {frase}?"}
            ],
            "temperature": 0.7
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            resposta = response.json()['choices'][0]['message']['content']
            return resposta.strip()

        except Exception as e:
            print("❌ Erro ao consultar o modelo:", e)
            return None
