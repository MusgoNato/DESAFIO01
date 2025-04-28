import asyncio
import os
from dotenv import load_dotenv
from services.telegram_client import TelegramBotClient
from services.pandas_score_client import PandaScoreClient
from bots.bot_client import BotClientConfiguration


async def main():
    """Inicializa e executa o bot Telegram com integração à API PandaScore.

    Carrega variáveis de ambiente, configura o cliente PandaScore e o bot Telegram com suporte a
    webhook. Esta função é o ponto de entrada principal da aplicação.

    Args:
        None

    Returns:
        None

    Raises:
        KeyError: Se as variáveis de ambiente (BOT_TOKEN, WEBHOOK_URL, API_KEY_PANDAS_SCORE)
            não estiverem definidas no arquivo .env.
        Exception: Qualquer erro durante a inicialização do cliente PandaScore, do bot
            Telegram ou na chamada à API PandaScore.

    Example:
        >>> asyncio.run(main())
        # Carrega variáveis de ambiente, inicializa clientes e roda o bot.
        [{'opponents': [...], 'results': [...], 'winner': {...}, ...}]
    """

    load_dotenv()
    
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    API_KEY_PANDAS_SCORE = os.getenv('API_KEY_PANDAS_SCORE')

    clientPandas = PandaScoreClient(API_KEY_PANDAS_SCORE)

    client = TelegramBotClient(
        bot_token=BOT_TOKEN,
        webhook_url=WEBHOOK_URL,
        pandas_client=clientPandas
    )

    # Inicializando configurações do BOT
    await client.bot.set_my_description(description="Bot da FURIA exclusivo para CS 🔫. Acompanhe o time da FURIA 🐈‍⬛")
    await client.bot.set_my_short_description(short_description="Bot da Furia CS. Manda aquele /start ou /menu pra acessar o menu principal fera 😎")

    # Roda o bot
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
