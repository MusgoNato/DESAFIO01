from telebot.async_telebot import AsyncTeleBot
from telebot import types

class MessageHandler:
    def __init__(self, bot: AsyncTeleBot):
        self.bot = bot


    async def _send_main_menu(self, message):
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
