from telebot.async_telebot import AsyncTeleBot
from telebot import types

class MessageHandler:
    """Gerencia mensagens recebidas pelo bot Telegram e exibe o menu principal.

    Responsável por processar comandos e mensagens do usuário, enviando respostas
    interativas, como o menu principal com botões inline. Integra-se com o bot
    Telegram assíncrono para enviar mensagens formatadas e imagens.

    Attributes:
        bot (AsyncTeleBot): Instância do bot Telegram para envio de mensagens e interações.
    """

    def __init__(self, bot: AsyncTeleBot):
        """Inicializa o manipulador de mensagens com o bot Telegram.

        Args:
            bot (AsyncTeleBot): Instância do bot Telegram configurada com token e webhook.
        """
        self.bot = bot


    async def _send_main_menu(self, message):
        """Envia o menu principal do bot Telegram com opções interativas.

        Cria um menu com botões inline para exibir o resultado da última partida da FURIA.
        Envia a logo oficial da FURIA como uma imagem para reforçar a identidade visual.
        A mensagem introdutória engaja os usuários e explica o propósito do botão.

        Args:
            message (telebot.types.Message): Objeto da mensagem recebida do Telegram.

        Returns:
            None

        Raises:
            Exception: Se houver falha ao enviar a imagem, a mensagem ou criar o markup.
        """
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            'Última partida da FURIA 🐈‍⬛', 
            callback_data="menu_ultimaPartida"
        ))
        
        logo = "https://images.steamusercontent.com/ugc/1009315379357635148/92002071318509F5E315603B7775EABBBBCD2517/?imw=637&imh=358&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true"
        caption = (
            f"🔥 Bem-vindo à nação Fúria {message.from_user.first_name} 🔥\n"
            "👉 [Explore o universo Fúria no nosso site](https://furia.gg)\n"
            "👉 [Junte-se à comunidade no Discord](https://discord.gg/furia)\n"
            "👉 [Nos siga no Instagram](https://www.instagram.com/furiagg/)\n"
            "Escolha uma das opções abaixo e bora pro próximo level 🦾\n"
        )

        await self.bot.send_photo(
            chat_id=message.chat.id,
            photo=logo,
            caption=caption,
            parse_mode='Markdown',
            reply_markup=markup
        )
