from telebot import TeleBot
from flask import Flask, request
from telebot import types
import os
from utils.getSeries import getSeries, jsonForObjects, getWinnerById

# Dicionário global para armazenar torneios por chat_id
TORNEIOS_POR_CHAT = {}

class TelegramBotClient:
    def __init__(self, bot_token: str, webhook_url: str, api_key: str):
        self.bot_token = bot_token
        self.api_key = api_key
        self.bot = TeleBot(bot_token)
        self.webhook_url = webhook_url.rstrip('/')
        self.app = Flask(__name__)
        self._register_handlers()
        self._configure_routes()

    def _configure_routes(self):
        """Configuração das rotas para acesso a webhook"""
        @self.app.route(f'/{self.bot_token}', methods=['POST'])
        def webhook():
            if request.is_json:
                try:
                    json_data = request.get_json()
                    update = types.Update.de_json(json_data)
                    self.bot.process_new_updates([update])
                    return '', 200
                except Exception as e:
                    print(f"Erro no processamento: {e}")
                    return '', 500
            return '', 400

    def _formatar_torneio(self, torneio):
        """Formata a mensagem de um torneio para exibição"""
        mensagem = f"🏆 *{torneio.nome}* - {torneio.serie.temporada if torneio.serie.temporada != None else 'A marcar'} {torneio.serie.ano}\n\n⚔️ *Partidas*:\n"

        for partida in torneio.partidas:
            vencedor = ""
            if partida.vencedor:
                timeVencedor = getWinnerById(self.api_key, partida.vencedor)
                vencedor += f"🏁 **Time Vencedor:** {timeVencedor[0]['name']}" 
            mensagem += f"{partida.nome} - {partida.status}{vencedor}\n"

        return mensagem

    def _criar_botoes_paginacao(self, index, total):
        """Cria botões de navegação para paginação"""
        botoes = []
        if index > 0:
            botoes.append(types.InlineKeyboardButton("⬅️ Anterior", callback_data=f"page_{index-1}"))
        if index < total - 1:
            botoes.append(types.InlineKeyboardButton("Próximo ➡️", callback_data=f"page_{index+1}"))
        return types.InlineKeyboardMarkup([botoes]) if botoes else None

    def _register_handlers(self):
        """Registro de mensagens do bot em caso de respostas por parte do usuario"""

        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            """Responsável pelo envio padrão do menu principal"""
            self._send_main_menu(message.chat.id)

        # Handler para botões do teclado
        @self.bot.callback_query_handler(func=lambda call: call.data.startswith('menu_'))
        def handle_menu_actions(call):
            action = call.data.split('_')[1]
            self.bot.answer_callback_query(call.id)

            match action:
                case "torneios":
                    torneios = jsonForObjects(getSeries(self.api_key))
                    if not torneios:
                        self.bot.send_message(call.message.chat.id, "Nenhum torneio encontrado.")
                        return

                    # Armazena os torneios no dicionário global
                    TORNEIOS_POR_CHAT[call.message.chat.id] = torneios

                    # Exibe o primeiro torneio
                    index = 0
                    mensagem = f"Torneio {index + 1} de {len(torneios)}\n\n" + self._formatar_torneio(torneios[index])
                    reply_markup = self._criar_botoes_paginacao(index, len(torneios))
                    self.bot.send_message(call.message.chat.id, mensagem, reply_markup=reply_markup)

        # Handler para botões de paginação
        @self.bot.callback_query_handler(func=lambda call: call.data.startswith('page_'))
        def handle_pagination(call):
            self.bot.answer_callback_query(call.id)

            # Extrai o índice do callback_data
            index = int(call.data.split('_')[1])
            chat_id = call.message.chat.id

            # Recupera os torneios do dicionário global
            torneios = TORNEIOS_POR_CHAT.get(chat_id, [])
            if not torneios or index >= len(torneios):
                self.bot.send_message(chat_id, "Torneio não encontrado.")
                return

            # Formata a mensagem do torneio atual
            mensagem = f"Torneio {index + 1} de {len(torneios)}\n\n" + self._formatar_torneio(torneios[index])
            reply_markup = self._criar_botoes_paginacao(index, len(torneios))

            # Edita a mensagem original
            try:
                self.bot.edit_message_text(
                    mensagem,
                    chat_id=chat_id,
                    message_id=call.message.message_id,
                    reply_markup=reply_markup
                )
            except Exception as e:
                print(f"Erro ao editar mensagem: {e}")
                self.bot.send_message(chat_id, mensagem, reply_markup=reply_markup)

        @self.bot.message_handler(func=lambda message: True)
        def echo_all(message):
            self.bot.reply_to(message, "ℹ️ Use /start para ver as opções principais")

    def _send_main_menu(self, chat_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('📢 Torneios Recentes', callback_data="menu_torneios"))
        
        logo = "https://duckduckgo.com/i/c33076bb294fef17.png"
        caption = (
            "🔥 Bem-vindo à nação Fúria 🔥\n"
            "👉 [Explore o universo Fúria no nosso site](https://furia.gg)\n"
            "👉 [Junte-se à comunidade no Discord](https://discord.gg/furia)\n"
            "👉 [Nos siga no Instagram](https://www.instagram.com/furiagg/)\n"
            "Escolha um botão abaixo e bora pro próximo level furioso 🦾\n"
        )

        # Envio da logo da furia juntamente com uma mensagem personalizada e os botões
        self.bot.send_photo(chat_id, logo, caption, parse_mode='Markdown', reply_markup=markup)

    def start(self):
        """Inicialização do bot ao webhook"""
        try:
            self.bot.remove_webhook()
            full_url = f"{self.webhook_url}/{self.bot_token}"
            print(f"⏳ Configurando webhook para: {full_url}")
            self.bot.set_webhook(url=full_url)
            self.app.run(host='0.0.0.0', port=5000, debug=os.getenv('DEBUG', 'False').lower() == 'true')
        except Exception as e:
            print(f"❌ Erro crítico: {e}")
            exit(1)