# ChatBot Gemini + WhatsApp + Flask + PostgreSQL

Este projeto implementa um chatbot usando o **Gemini Connector** integrado ao **WhatsApp Business API**, com webhook em **Flask** e persistência de dados em **PostgreSQL**.

O objetivo é receber mensagens dos usuários via WhatsApp, enviar para o Gemini para gerar respostas, retornar a resposta ao usuário e gravar a conversa no banco de dados.

---

## 🔹 Funcionalidades

- Conexão com **Gemini** para processar mensagens.
- Envio e recebimento de mensagens via **WhatsApp Business API**.
- Webhook em **Flask** para receber POSTs do WhatsApp.
- Gravação das conversas em **PostgreSQL**.
- Logs de debug detalhados (opcional).
- Modularização de código: Gemini, WhatsApp, Webhook e Banco separados.

---

## 🛠️ Estrutura do projeto

chatbot/
│
├─ servicos/
│ ├─ gemini.py # Classe GeminiConnector
│ ├─ wpp.py # Classe WhatsAppChat
│ ├─ webhook.py # Classe WebhookService (Flask)
│ └─ db.py # Classe PostgresDB
│
├─ config.json # Configurações do WhatsApp
├─ main.py # Arquivo principal que inicializa tudo
└─ README.md

---

## ⚙️ Configuração

### 1. Dependências

pip install flask requests psycopg2-binary

### 2. Configuração do WhatsApp
Crie um arquivo config.json:

json
{
    "whatsapp_token": "SEU_TOKEN_DO_WHATSAPP",
    "phone_number_id": "ID_DO_NUMERO",
    "to_phone_number": "NUMERO_DO_DESTINATARIO"
}
Certifique-se que o webhook está registrado e verificado no Facebook Developers > WhatsApp > Webhooks.

### 3. Configuração do PostgreSQL
Crie a tabela conversas:

sql
CREATE TABLE conversas (
    id SERIAL PRIMARY KEY,
    from_number VARCHAR(20),
    message_text TEXT,
    response_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

### 4. Configuração do Webhook
O webhook Flask roda na porta 5000 por padrão.

Se estiver rodando localmente, use ngrok ou servidor público para expor a URL:

bash
ngrok http 5000
Adicione a URL gerada no painel do WhatsApp Developers e verifique com o token configurado.

#### 🚀 Executando o projeto

bash
python main.py
Com debug ativo (debug=True), você verá no console:

- Mensagens recebidas do WhatsApp.
- Resposta do Gemini.
- Status do envio para o WhatsApp.
- Gravação no banco de dados.
- Mensagens do WhatsApp real só funcionarão se:
- O número estiver autorizado (sandbox ou número real).
- O webhook estiver verificado e disponível publicamente.
- Eventos messages estiverem habilitados no webhook.

🔹 Como funciona

- Usuário envia mensagem no WhatsApp.
- WhatsApp envia POST para o webhook Flask.
- WebhookService processa o JSON:
- Captura número do remetente e mensagem.
- Envia a mensagem para o Gemini.
- Recebe resposta e envia para o WhatsApp.
- Grava mensagem e resposta no PostgreSQL.
- Logs de debug mostram a interação no terminal.

📦 Modularidade

- GeminiConnector (gemini.py) → Interface para o Gemini.
- WhatsAppChat (wpp.py) → Envio de mensagens via API do WhatsApp.
- WebhookService (webhook.py) → Recebe e processa mensagens do WhatsApp.
- PostgresDB (db.py) → Conexão e gravação no PostgreSQL.
- main.py → Inicializa tudo, conecta os serviços e roda o webhook.

⚠️ Observações

- No sandbox do WhatsApp, só mensagens de contatos autorizados chegam ao webhook.
- Para produção, utilize um servidor com URL pública e certificado HTTPS.
- O debug detalhado (debug=True) é útil para desenvolvimento, mas deve ser desativado em produção.