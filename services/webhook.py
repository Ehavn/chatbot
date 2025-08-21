from flask import Flask, request, jsonify

class WebhookService:
    def __init__(self, gemini, whatsapp, debug=False):
        self.app = Flask(__name__)
        self.gemini = gemini
        self.whatsapp = whatsapp
        self.debug = debug
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/webhook", methods=["GET", "POST"])
        def webhook():
            if request.method == "GET":
                # Verificação do webhook pelo WhatsApp
                verify_token = "MEU_TOKEN_DE_VERIFICACAO"
                mode = request.args.get("hub.mode")
                token = request.args.get("hub.verify_token")
                challenge = request.args.get("hub.challenge")
                if mode and token:
                    if mode == "subscribe" and token == verify_token:
                        return challenge, 200
                    else:
                        return "Token inválido", 403
                return "OK", 200

            if request.method == "POST":
                # Captura o corpo da requisição
                data = request.get_json()

                if self.debug:
                    print("\n=== Webhook recebido ===")
                    print("Headers:", dict(request.headers))
                    print("Body (JSON):", data)
                    print("Body (raw):", request.data.decode())

                # Processa a mensagem
                self.handle_message(data)
                return jsonify({"status": "received"}), 200

    def handle_message(self, data):
        try:
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    for message in messages:
                        from_number = message.get("from")
                        text = message.get("text", {}).get("body", "N/A")

                        if self.debug:
                            print(f"Mensagem recebida de {from_number}: {text}")

                        # Aqui é a mensagem do usuário via WhatsApp que vai para o Gemini
                        resposta = self.gemini.enviar_mensagem(text)

                        # Envia resposta pelo WhatsApp
                        resultado = self.whatsapp.send_whatsapp_message(resposta)

                        if self.debug:
                            print(f"Resposta do Gemini: {resposta}")
                            print(f"Status envio WhatsApp: {resultado}")

        except Exception as e:
            print("Erro ao processar mensagem:", e)

    def run(self, host="0.0.0.0", port=5000):
        # use_reloader=False evita erro de signal no Windows quando rodando em thread
        self.app.run(host=host, port=port, debug=self.debug, use_reloader=False)
