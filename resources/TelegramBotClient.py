from telebot import TeleBot
from flask import Flask, request
from telebot import types
import os

class TelegramBotClient:
    def __init__(self, bot_token: str, webhook_url: str):
        
        self.bot_token = bot_token
        self.bot = TeleBot(bot_token)
        
        # Remove qualquer barra final da url
        self.webhook_url = webhook_url.rstrip('/')
        
        self.app = Flask(__name__)
        
        # Registro e configuração dos manipuladores para o bot
        self._register_handlers()
        self._configure_routes()

    def _configure_routes(self):
        """Configuração das rotas para acesso a webhook"""
        @self.app.route(f'/{self.bot_token}', methods=['POST'])
        def webhook():
            if request.is_json:
                try:
                    # Processamento das requisições feitas ao bot <-> user
                    json_data = request.get_json()
                    update = types.Update.de_json(json_data)
                    self.bot.process_new_updates([update])
                    return '', 200
                
                # Tratamento de exceções
                except Exception as e:
                    print(f"Erro no processamento: {e}")
                    return '', 500
            return '', 400

    def _register_handlers(self):
        """Registro de mensagens do bot em caso de respostas definidas pelo usuario"""

        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            """Responsavel pelo envio padrão do menu principal"""
            self._send_main_menu(message.chat.id)

         # Handler para botões do teclado
        @self.bot.callback_query_handler(func=lambda call: call.data.startswith('menu_'))
        def handle_menu_actions(call):
            action = call.data.split('_')[1]
            
            # Resposta para o usuario de acordo com o id do botao apertado
            self.bot.answer_callback_query(call.id)

            match(action):
                case "torneios":
                    self.bot.send_message(call.message.chat.id, "Ele escolheu Torneios") 

        @self.bot.message_handler(func=lambda message: True)
        def echo_all(message):
            self.bot.reply_to(message, "ℹ️ Use /start para ver as opções principais")
    
    def _send_main_menu(self, chat_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('📢 Últimos Torneios', callback_data="menu_torneios"))
        
        self.bot.send_message(chat_id, "Escolha uma opção:", reply_markup=markup)

    def start(self):
        """Inicialização do bot ao webhook"""
        try:
            # Remove qualquer webhook setada anteriormente e volta a inicializar com uma nova
            self.bot.remove_webhook()
            full_url = f"{self.webhook_url}/{self.bot_token}"
            print(f"⏳ Configurando webhook para: {full_url}")
            self.bot.set_webhook(url=full_url)
            
            # Modo para debugar
            self.app.run(host='0.0.0.0', port=5000, debug=os.getenv('DEBUG', 'False').lower() == 'true')
        
        except Exception as e:
            print(f"❌ Erro crítico: {e}")
            exit(1)