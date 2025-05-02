from quart import Quart, request
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from handlers.message_handler import MessageHandler
from handlers.callback_handler import CallbacksHandler
import asyncio
from services.pandas_score_client import PandaScoreClient
from telebot.types import BotCommand
from hypercorn.asyncio import serve
from hypercorn.config import Config
from utils.formatResponse import get_Curiosidades 

class TelegramBotClient:
    """Cliente para gerenciar um bot Telegram com suporte a webhooks.

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
        """

        # instancias necessarias para conexao com o bot, troca de mensagens por botoes inline e envio de mensagens
        self.bot = AsyncTeleBot(bot_token)
        self.callback_handler = CallbacksHandler(self.bot, pandas_client)
        self.handler = MessageHandler(self.bot)

        # inicialização para expor localmente e criar conexao webhook posteriormente
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
            """
            update = await request.get_json()
            await self.bot.process_new_updates([types.Update.de_json(update)])
            return '', 200

    # Registra os handlers para envio de mensagens
    def _register_handlers(self):
        """
        Registra manipuladores de mensagens para comandos do Telegram.

        Configura um manipulador para os comandos '/menu' e /curiosidade, que exibe o menu
        principal do bot usando o MessageHandler.

        Returns:
            None
        """
        @self.bot.message_handler(commands=['start', 'menu'])
        async def handle_start(message):
            """
            Processa os comandos /start e /menu, exibindo o menu principal.

            Args:
                message (telebot.types.Message): Objeto da mensagem recebida, contendo
                    informações sobre o chat e o usuário.

            Returns:
                None
            """
            await self.handler._send_main_menu(message)
            
        @self.bot.message_handler(commands=['curiosidade'])
        async def handle_message_text(message):
            """
            Manipulador para envio de curiosidades sobre a FURIA
            """
            curiosidade = get_Curiosidades()
            await self.bot.send_message(message.chat.id, text=curiosidade, parse_mode='Markdown')

    async def start(self):
        """
        Inicia o bot Telegram, configurando o webhook.

        Remove webhooks existentes, configura um novo webhook
        com a URL fornecida e inicia o servidor Quart com Hypercorn na porta 5000.

        Returns:
            None

        Notes:
            Requer as bibliotecas Quart e Hypercorn para o servidor webhook.
        """
        await asyncio.sleep(1) 
        await self.bot.remove_webhook()

        # Removo a slash antes do webhook para evitar problemas com a slash padrao que vem ao final da url gerada pelo ngrok
        full_url = f"{self.webhook_url}webhook/{self.bot.token}"
        
        # Seto a webhook
        print(f"⏳ Configurando webhook: {full_url}")
        await self.bot.set_webhook(url=full_url, allowed_updates=["message", "callback_query"])
        
        config = Config()

        # Localhost
        config.bind = ["0.0.0.0:5000"]
        await serve(self.app, config)
        
    async def set_BotConfig(self):
        """
        Função que realiza todas as configurações do BOT (Exceto mudança de foto de perfil, pois somente é possível manualmente)
        """
        try:
            await self.bot.set_my_name("FURIA CS BOT 🔥")
            await self.bot.set_my_description("Bot da FURIA exclusivo para CS 🔫. Acompanhe o time da FURIA 🐈‍⬛")
            await self.bot.set_my_short_description("Bot da Furia CS. Manda aquele /menu pra acessar o menu principal ou /curiosidade pra curiosidades sobre a FURIA fera 😎")
            await self.bot.set_my_commands([BotCommand("menu", "Menu principal"), BotCommand("curiosidade", "Curiosidades da FURIA")])
        except Exception as e:
            print(f"Problema em configurar o BOT: ERRO: {e}\n\n")


        
