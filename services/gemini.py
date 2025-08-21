import json
import google.generativeai as genai

class GeminiConnector:
    def __init__(self, config_file="credentials/gemini_env.json"):
        with open(config_file, "r") as f:
            config = json.load(f)

        self.api_key = config["gemini_api_key"]
        genai.configure(api_key=self.api_key)

        # cria um chat persistente
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.chat = self.model.start_chat(history=[])

    def enviar_mensagem(self, mensagem: str) -> str:
        resposta = self.chat.send_message(mensagem)
        return resposta.text
