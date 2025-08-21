import json
import requests
import google.generativeai as genai

# ===== Carregar Config =====
with open("config.json", "r") as f:
    config = json.load(f)

GEMINI_API_KEY = config["gemini_api_key"]
WHATSAPP_TOKEN = config["whatsapp_token"]
PHONE_NUMBER_ID = config["phone_number_id"]   # Ex: "123456789012345"
TO_PHONE_NUMBER = config["to_phone_number"]   # Ex: "5511999999999"

# ===== Configurar Gemini =====
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

# ===== Função para enviar mensagem no WhatsApp =====
def send_whatsapp_message(text):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": TO_PHONE_NUMBER,
        "type": "text",
        "text": {"body": text[:4096]}  # WhatsApp aceita até 4096 chars
    }

    print("\n=== Enviando mensagem para WhatsApp ===")
    print("➡️ URL:", url)
    print("➡️ Headers:", headers)
    print("➡️ Payload:", json.dumps(payload, indent=2, ensure_ascii=False))

    response = requests.post(url, headers=headers, json=payload)

    print("\n=== Resposta da API do WhatsApp ===")
    print("⬅️ Status:", response.status_code)
    print("⬅️ Resposta:", response.text)

    if response.ok:
        print("✅ Mensagem enviada com sucesso!")
    else:
        print("❌ Erro ao enviar mensagem!")

    return response


# ===== Loop do Chatbot =====
print("🤖 Chatbot iniciado! (digite 'sair' para encerrar)")

while True:
    user_input = input("Você: ")

    if user_input.lower() in ["sair", "exit", "quit"]:
        print("🤖 Chat encerrado.")
        break

    # Envia para Gemini
    response = chat.send_message(user_input)
    bot_reply = response.text.strip()

    print("Bot:", bot_reply)

    # Envia resposta para WhatsApp
    send_whatsapp_message(bot_reply)
