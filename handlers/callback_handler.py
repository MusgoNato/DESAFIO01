from telebot.async_telebot import AsyncTeleBot
from services.pandas_score_client import PandaScoreClient
from utils.formatResponse import formatUltimaPartida

class CallbacksHandler:
    def __init__(self, bot: AsyncTeleBot, pandas_client: PandaScoreClient):
        self.bot = bot
        self.pandas_client = pandas_client
        self._registerCallbacks()

    def _registerCallbacks(self):
        @self.bot.callback_query_handler(func=lambda call:True)
        async def handle_all_callbacks(call):
            if call.data == "menu_ultimaPartida":
                response = await self.pandas_client.get_Ultima_Partida()
                message = formatUltimaPartida(response)
                await self.bot.send_photo(
                    chat_id=call.message.chat.id,
                    photo=message['logo'],
                    caption=message['text'],
                    parse_mode='Markdown',
                )
            else:
                await self.bot.answer_callback_query(call.id, "Outra coisa!")