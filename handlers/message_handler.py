from telebot.async_telebot import AsyncTeleBot
from telebot import types

class MessageHandler:
    """
    Gerencia mensagens recebidas pelo bot Telegram e exibe o menu principal.

    Responsável por processar comandos e mensagens do usuário, enviando respostas
    interativas, como o menu principal com botões inline. Integra-se com o bot
    Telegram assíncrono para enviar mensagens formatadas e imagens.

    Attributes:
        bot (AsyncTeleBot): Instância do bot Telegram para envio de mensagens e interações.
    """

    def __init__(self, bot: AsyncTeleBot):
        """
        Inicializa o manipulador de mensagens com o bot Telegram.

        Args:
            bot (AsyncTeleBot): Instância do bot Telegram configurada com token e webhook.
        """
        self.bot = bot


    async def _send_main_menu(self, message):
        """
        Envia o menu principal do bot Telegram com opções interativas.

        Cria um menu com botões inline para exibir o resultado da última partida da FURIA.
        Envia a logo oficial da FURIA como uma imagem para reforçar a identidade visual.
        A mensagem introdutória engaja os usuários e explica o propósito do botão.

        Args:
            message (telebot.types.Message): Objeto da mensagem recebida do Telegram.

        Returns:
            None
        """
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Última partida da FURIA 🐈‍⬛', callback_data="menu_ultimaPartida",),
        types.InlineKeyboardButton(text="Próximas Partidas 🎮📢", callback_data="menu_proximasPartidas"),
        types.InlineKeyboardButton(text="Partidas ao vivo 🔴", callback_data="menu_partidaEmAndamento"),
        types.InlineKeyboardButton(text="Time completo ℹ️", callback_data="menu_timeCompleto"))
        
        logo = "https://www.negitaku.org/wp-content/uploads/2019/06/furia.jpg"
        caption = (
            f"🔥 Bem-vindo à nação Fúria {message.from_user.first_name} 🔥\n"
            "👉 [Explore o universo Fúria no nosso site](https://furia.gg)\n"
            "👉 [Junte-se à comunidade no Discord](https://discord.gg/furia)\n"
            "👉 [Nos siga no Instagram](https://www.instagram.com/furiagg/)\n"
            "👉 [Assista as nossas lives na Roxinha Twitch](https://www.twitch.tv/furiatv)\n"
            "Escolha uma das opções abaixo e bora pro próximo level 🦾"
        )

        await self.bot.send_photo(
            chat_id=message.chat.id,
            photo=logo,
            caption=caption,
            parse_mode='Markdown',
            reply_markup=markup
        )
