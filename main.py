import asyncio
import os
from dotenv import load_dotenv
from services.telegram_client import TelegramBotClient
from services.pandas_score_client import PandaScoreClient

async def main():
    """
    Inicializa e executa o bot Telegram com integração à API PandaScore.

    Carrega variáveis de ambiente, configura o cliente PandaScore e o bot Telegram com suporte a
    webhook. Esta função é o ponto de entrada principal da aplicação.

    Args:
        None

    Returns:
        None

    Example:
        >>> asyncio.run(main())
        # Carrega variáveis de ambiente, inicializa clientes e roda o bot.
        [{'opponents': [...], 'results': [...], 'winner': {...}, ...}]
    """
    # Carregamento e atribuição das variaveis de ambiente
    load_dotenv()
    
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    API_KEY_PANDAS_SCORE = os.getenv('API_KEY_PANDAS_SCORE')

    # Instanciacao para consultas a API
    clientPandas = PandaScoreClient(API_KEY_PANDAS_SCORE)

    # Instanciacao para consultas ao BOT
    client = TelegramBotClient(
        bot_token=BOT_TOKEN,
        webhook_url=WEBHOOK_URL,
        pandas_client=clientPandas
    )

    # Configura o BOT
    await client.set_BotConfig()

    # Roda o bot 
    await client.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Não foi possivel inicializar o bot : {e}")

