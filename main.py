import asyncio
import os
from dotenv import load_dotenv
from utils.JsonData import getJsonData
from utils.TelegramBotClient import TelegramBotClient
from utils.AbiosClient import AbiosClient 
from utils.JsonData import getTorneios
from utils.getGanhadores import getGanhadores, jsonForObjects 

# Main
if __name__ == "__main__":
    
    # Carrega variaveis de ambiente (.env)
    load_dotenv()

    # Atribuição das chaves apis
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    API_IA = os.getenv('API_IA')
    API_KEY_PANDAS_SCORE = os.getenv('API_KEY_PANDAS_SCORE')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')    
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')

    # Atribuição da url para consumo da API
    URL_API = os.getenv('URL_API')

    # # Retorno da requisição a API
    # client = AbiosClient(URL_API, API_KEY_PANDAS_SCORE)
    # response = client._request(method="GET", endpoint="tournaments/running")
    # print(response)

    # Retorno do arquivo json
    # data = getJsonData()

    # Resposta da requisição a API
    resposeganhadoresJson = getGanhadores(API_KEY_PANDAS_SCORE)
    data = jsonForObjects(resposeganhadoresJson)
    

    if not BOT_TOKEN or not WEBHOOK_URL:
        print("❌ Variáveis de ambiente obrigatórias ausentes!")
        exit(1)

    # Retorna a autenticação do usuario no bot do telegram
    client = TelegramBotClient(BOT_TOKEN, WEBHOOK_URL, API_KEY_PANDAS_SCORE)

    client.start()