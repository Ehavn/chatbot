from services.gemini import GeminiConnector
from services.wpp import WhatsAppChat
from services.webhook import WebhookService
import threading

if __name__ == "__main__":
    gemini = GeminiConnector()
    whatsapp = WhatsAppChat(debug=True)  # ativa logs detalhados do WhatsApp

    # Inicializa webhook em uma thread separada
    webhook = WebhookService(gemini, whatsapp, debug=True)
    threading.Thread(target=webhook.run, kwargs={"host": "0.0.0.0", "port": 5000}, daemon=True).start()

    print("🤖 Chat Gemini iniciado. Envie mensagens pelo WhatsApp ou teste no terminal.")

    # Loop opcional para teste direto no terminal
    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("🤖 Chat encerrado.")
            break

        resposta = gemini.enviar_mensagem(user_input)
        print("Gemini-Bot:", resposta)
        resultado = whatsapp.send_whatsapp_message(resposta)
        if resultado.get("success"):
            print("✅ Mensagem enviada pelo WhatsApp!")
        else:
            print("❌ Falha ao enviar pelo WhatsApp:", resultado.get("response"))
