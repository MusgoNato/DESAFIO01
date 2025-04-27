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
    """Cliente para gerenciar um bot Telegram com suporte a webhooks e integração com PandaScore.

    Configura um bot Telegram assíncrono usando AsyncTeleBot, registra manipuladores de mensagens
    e callbacks, e inicia um servidor webhook com Quart e Hypercorn. Integra-se com a API
    PandaScore para fornecer dados de partidas de CS:GO/CS2, como resultados da FURIA.

    Attributes:
        bot (AsyncTeleBot): Instância do bot Telegram configurada com o token.
        callback_handler (CallbacksHandler): Manipulador de callbacks de botões inline.
        handler (MessageHandler): Manipulador de mensagens e comandos do usuário.
        app (Quart): Aplicação Quart para gerenciar rotas do webhook.
        webhook_url (str): URL base do webhook (ex.: 'https://d1c8-45-187-27-161.ngrok-free.app/').
    """
    def __init__(self, bot_token: str, webhook_url: str, pandas_client: PandaScoreClient):
        """Inicializa o cliente do bot Telegram com token, URL do webhook e cliente PandaScore.

        Args:
            bot_token (str): Token de autenticação do bot fornecido pelo @BotFather.
            webhook_url (str): URL base para o webhook (ex.: 'https://d1c8-45-187-27-161.ngrok-free.app/').
            pandas_client (PandaScoreClient): Cliente configurado para acessar a API PandaScore.

        Raises:
            ValueError: Se o bot_token ou webhook_url forem vazios ou inválidos.
        """
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
        """Registra a rota do webhook para receber atualizações do Telegram.

        Configura uma rota POST no formato '/webhook/<bot_token>' para processar atualizações
        enviadas pelo Telegram. As atualizações são passadas ao bot para processamento assíncrono.

        Returns:
            None
        """
        @self.app.route(f'/webhook/{self.bot.token}', methods=['POST'])
        async def webhook():
            """Processa atualizações recebidas via webhook.

            Recebe dados JSON do Telegram, converte em um objeto Update e passa para o bot
            processar mensagens ou callbacks.

            Returns:
                tuple: Resposta HTTP com corpo vazio e status 200.

            Raises:
                Exception: Se houver falha ao processar o JSON ou as atualizações.
            """
            update = await request.get_json()
            await self.bot.process_new_updates([types.Update.de_json(update)])
            return '', 200

    # Registra os handlers para envio de mensagens
    def _register_handlers(self):
        """Registra manipuladores de mensagens para comandos do Telegram.

        Configura um manipulador para os comandos '/start' e '/menu', que exibe o menu
        principal do bot usando o MessageHandler.

        Returns:
            None
        """
        @self.bot.message_handler(commands=['start', 'menu'])
        async def handle_start(message):
            """Processa os comandos /start e /menu, exibindo o menu principal.

            Args:
                message (telebot.types.Message): Objeto da mensagem recebida, contendo
                    informações sobre o chat e o usuário.

            Returns:
                None
            """
            await self.handler._send_main_menu(message)

    async def start(self):
        """Inicia o bot Telegram, configurando o webhook ou usando polling no modo debug.

        No modo debug (DEBUG=True), usa polling para testar o bot localmente (desativado
        por padrão). Em produção, remove webhooks existentes, configura um novo webhook
        com a URL fornecida e inicia o servidor Quart com Hypercorn na porta 5000.

        Returns:
            None

        Raises:
            ValueError: Se a URL do webhook for inválida ou malformada.
            Exception: Se houver falha ao configurar o webhook ou iniciar o servidor.

        Notes:
            Requer as bibliotecas Quart e Hypercorn para o servidor webhook. O ambiente
            deve definir a variável DEBUG para ativar o modo debug.
        """
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
