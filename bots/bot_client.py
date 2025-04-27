from telebot import TeleBot
from handlers.message_handler import MessageHandler

class BotClient:
    def __init__(self, token: str):
        self.bot = TeleBot(token)
        self.handler = MessageHandler()
        
        # Injeta a instância do bot no handler
        self.handler.bot = self.bot
        
        self._register_handlers()

    def _register_handlers(self):
        @self.bot.message_handler(commands=['start', 'menu'])
        def handle_start(message):
            self.handler._send_main_menu(message.chat.id)

    def start(self):
        self.bot.infinity_polling()
