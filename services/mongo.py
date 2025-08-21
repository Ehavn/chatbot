from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Substitua a string abaixo com a sua String de Conexão,
# colocando a senha do seu usuário no lugar de <db_password>
uri = "mongodb+srv://ehavn:1951@cluster-chatbot.npckgpy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-chatbot"

# Crie um novo cliente e conecte ao servidor
client = MongoClient(uri, server_api=ServerApi('1'))

# Tente enviar um ping para confirmar a conexão
try:
    client.admin.command('ping')
    print("Conexão bem-sucedida ao MongoDB!")
except Exception as e:
    print(e)