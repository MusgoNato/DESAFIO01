# services/webhook.py
import os
from quart import Quart, request
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from handlers.message_handler import MessageHandler
from handlers.callback_handler import CallbacksHandler
import asyncio
from services.pandas_score_client import PandaScoreClient

class TelegramBotClient:
    def __init__(self, bot_token: str, webhook_url: str, pandas_client: PandaScoreClient):
        self.bot = AsyncTeleBot(bot_token)
        self.callback_handler = CallbacksHandler(self.bot, pandas_client)

        self.handler = MessageHandler(self.bot)

        self.app = Quart(__name__)
        self.webhook_url = webhook_url

        # Registro de rotas e handlers
        self._register_routes()
        self._register_handlers()

    # Registra a rota da minha webhook
    def _register_routes(self):
        @self.app.route(f'/webhook/{self.bot.token}', methods=['POST'])
        async def webhook():
            update = await request.get_json()
            await self.bot.process_new_updates([types.Update.de_json(update)])
            return '', 200

    # Registra os handlers para envio de mensagens
    def _register_handlers(self):
        @self.bot.message_handler(commands=['start', 'menu'])
        async def handle_start(message):
            await self.handler._send_main_menu(message)

    async def start(self):
        """Inicialização de minha webhook"""
        if os.getenv('DEBUG') == 'True':
            print("🔍 Modo debug: usando polling")
            # await self.bot.infinity_polling() 
        else:
            await asyncio.sleep(1) 
            await self.bot.remove_webhook()
            full_url = f"{self.webhook_url}webhook/{self.bot.token}" # Removendo a slash, antes deu b.o
            
            print(f"⏳ Configurando webhook: {full_url}")
            await self.bot.set_webhook(url=full_url, allowed_updates=["message", "callback_query"])
            
            # importação das bibliotecas somente aonde irei usar
            from hypercorn.asyncio import serve
            from hypercorn.config import Config
            
            config = Config()
            config.bind = ["0.0.0.0:5000"]
            await serve(self.app, config)
