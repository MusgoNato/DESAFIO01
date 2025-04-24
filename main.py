import os
import json
from dotenv import load_dotenv
from groq import Groq
from telebot import TeleBot
from resources.AbiosClient import AbiosClient
from resources.JsonData import getJsonData
from resources.TelegramClient import TelegramBotClient

# Main
if __name__ == "__main__":
    
    # Carrega variaveis de ambiente (.env)
    load_dotenv()

    # Atribuição das chaves apis
    BOT_TOKEN = os.getenv('API_KEY_BOT')
    API_IA = os.getenv('API_IA')
    API_KEY_PANDAS_SCORE = os.getenv('API_KEY_PANDAS_SCORE')    

    # Atribuição da url para consumo da API
    URL_API = os.getenv('URL_API')

    # # Retorno da requisição a API
    # client = AbiosClient(URL_API, API_KEY_PANDAS_SCORE)
    # response = client._request(method="GET", endpoint="matches")
    # print(response)

    # Retorno do arquivo json
    data = getJsonData()
    
    # Retorna a autenticação do usuario no bot do telegram
    client = TelegramBotClient(BOT_TOKEN) 

    # Pego o bot (Para uso de keyboards, etc) 
    bot = client.getBot()

    ### Lembrete    
        # Fix
            # Fazer o message handler (Colocar uma mensagem padrao para replicar, com botões sobre os torneios que estao tendo, talvez fazer uma paginação ou algo do tipo)
        # Exemplo de desenvolvimento:
            # Criar uma classe que vai direcionar uma mensagem padrao, depois criar uma classe ou otras funções que irao captar o input do usuario e direcionar a saida da informação com base na API (no caso o data no formato json)
            # Como o bot ja roda pelo client.startPolling, tratar os inputs do usuario em outros arquivos (classes/funções) não vai ser um problema 
    
    # Roda o bot
    client.startPolling()

    
    
    
