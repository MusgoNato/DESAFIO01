import os
from dotenv import load_dotenv
from groq import Groq
from telebot import TeleBot
from resources.AbiosClient import AbiosClient


# # Conexao com a api do telegram para o bot
# bot = TeleBot(BOT_TOKEN)

# # Historico da IA e sua configuração.
# historico = [
#     {
#         "role": "system",
#         "content": "Todas as respostas devem ser respondidas em português para o usuário",
#     },
# ]

# # Controlador de mensagens
# @bot.message_handler(func=lambda message: message.chat.id)
# def handler_message(message):

#     # Conexao com a api para uso de uma IA
#     User = Groq(api_key=API_IA)
    
#     # Armazenando hostorico de mensagens
#     userResponse = message.text.strip()
#     historico.append({"role": "user", "content": userResponse})
    
#     # Criação do chat
#     chat = User.chat.completions.create(
#         messages=historico,
#         model="llama-3.1-8b-instant",
#         temperature=0,
#         stream=False,
#     )

#     # Conteudo da resposta da IA formatada
#     text_from_ia = chat.choices[0].message.content
#     text_from_ia = text_from_ia.split("</think>")[-1].strip()
#     historico.append({"role": "assistant", "content": text_from_ia})
    
#     # Bot respondendo
#     bot.send_message(message.chat.id, text_from_ia)

# # Roda o bot
# bot.infinity_polling()

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

    client = AbiosClient(URL_API, API_KEY_PANDAS_SCORE)
    response = client._request(method="GET", endpoint="matches")
    print(response)



