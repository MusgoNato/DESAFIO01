from telebot import TeleBot


class TelegramBotClient:
    """Classe para autenticação do Usuario ao Telegram"""

    def __init__(self, api_token: str):
        self.bot = TeleBot(api_token)

    def getBot(self):
        """Retorna o robo criado na inicialização"""
        return self.bot
    
    def startPolling(self, **kwargs):
        """Inicializa o polling do bot"""
        self.bot.polling(**kwargs)
        