from telebot.async_telebot import AsyncTeleBot
from services.pandas_score_client import PandaScoreClient
from utils.formatResponse import formatUltimaPartida, formatProximasPartidas, formatPartidaEmAndamento, format_player_page
from telebot import types

class CallbacksHandler:
    """Gerencia callbacks de botões inline no bot Telegram, integrando com a API PandaScore.

    Responsável por processar ações de botões inline, como exibir o resultado da última partida
    da FURIA, obtendo dados da API PandaScore e enviando respostas formatadas com imagens e texto.
    Registra manipuladores de callbacks durante a inicialização.

    Attributes:
        bot (AsyncTeleBot): Instância do bot Telegram para envio de mensagens e interações.
        pandas_client (PandaScoreClient): Cliente para chamadas à API PandaScore.
    """

    def __init__(self, bot: AsyncTeleBot, pandas_client: PandaScoreClient):
        """Inicializa o manipulador de callbacks com o bot Telegram e o cliente PandaScore.

        Args:
            bot (AsyncTeleBot): Instância do bot Telegram configurada com token e webhook.
            pandas_client (PandaScoreClient): Cliente configurado para acessar a API PandaScore.
        """
        self.bot = bot
        self.pandas_client = pandas_client
        self._registerCallbacks()

    def _registerCallbacks(self):
        """Registra manipuladores para processar callbacks de botões inline.

        Configura um manipulador genérico que processa todos os callbacks, verificando o
        `callback_data` para executar ações específicas, como exibir o resultado da última
        partida da FURIA. Usa um decorador do AsyncTeleBot para associar a função de callback.

        Returns:
            None
        """
        @self.bot.callback_query_handler(func=lambda call:True)
        async def handle_all_callbacks(call):
            """Processa todos os callbacks de botões inline recebidos.

            Verifica o valor de `callback_data` para determinar a ação. Para
            `menu_ultimaPartida`, obtém os dados da última partida via API PandaScore,
            formata a resposta e envia uma mensagem com a logo do vencedor e o resultado.
            Para outros valores, envia uma resposta padrão.

            Args:
                call (telebot.types.CallbackQuery): Objeto do callback, contendo informações
                    sobre o botão clicado (ex.: call.data, call.message.chat.id).

            Returns:
                None

            Raises:
                Exception: Se houver falha ao obter dados da API PandaScore, formatar a
                    mensagem ou enviar a resposta (ex.: URL da logo inválida, erro de rede).
            """
            match(call.data):
                case "menu_ultimaPartida":
                    response = await self.pandas_client.get_LastMatch()
                    message = formatUltimaPartida(response)
                    await self.bot.send_photo(
                        chat_id=call.message.chat.id,
                        photo=message['logo'],
                        caption=message['text'],
                        parse_mode='Markdown',
                    )

                case "menu_proximasPartidas":
                    response = await self.pandas_client.get_NextMatchesFuria()
                    message = formatProximasPartidas(response)
                    await self.bot.send_message(chat_id=call.message.chat.id, text=message, parse_mode='Markdown')

                case "menu_partidaEmAndamento":
                    response = await self.pandas_client.get_PartidaEmAndamento()
                    if not response:
                        message = "As partidas já acabaram meu furioso, mas fica ligado na nossa rede 😎" 
                    else:
                        message = formatPartidaEmAndamento(response)
                    await self.bot.send_message(chat_id=call.message.chat.id, text=message, parse_mode='Markdown')
                
                case "menu_timeCompleto":
                    response = await self.pandas_client.get_Team()
                    
                    players = response[0].get("players", [])
                    
                    player = players[0]
                    message = format_player_page(player, 0, len(players))
                    keyboard = create_navigation_buttons(0, len(players))

                    if player.get("image_url"):
                        await self.bot.send_photo(
                            chat_id=call.message.chat.id,
                            photo=player["image_url"],
                            caption=message,
                            reply_markup=keyboard,
                            parse_mode='Markdown'
                        )
                    else:
                        await self.bot.send_message(
                                    chat_id=call.message.chat.id,
                                    text=message,
                                    reply_markup=keyboard,
                                    parse_mode="Markdown"
                                )
                case str() if call.data.startswith("player_"):
                    player_index = int(call.data.split("_")[1])
                    response = await self.pandas_client.get_Team()
                    players = response[0].get("players", [])

                    player = players[player_index]
                    message = format_player_page(player, player_index, len(players))
                    keyboard = create_navigation_buttons(player_index, len(players))
                    
                    if player.get("image_url"):
                        await self.bot.edit_message_media(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            media=types.InputMediaPhoto(player["image_url"], caption=message),
                            reply_markup=keyboard
                        )
                    else:
                        DEFAULT_IMG_PLAYER = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn1.iconfinder.com%2Fdata%2Ficons%2Fuser-interface-664%2F24%2FUser-512.png&f=1&nofb=1&ipt=42b1085244d2f163e38bf3f65e2732a8b0f4459c30d1368f801704d50eb99e89"

                        media = types.InputMediaPhoto(
                            media=DEFAULT_IMG_PLAYER,
                            caption=message,
                            parse_mode='Markdown'
                        )

                        await self.bot.edit_message_media(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            reply_markup=keyboard,
                            media=media,
                        )

def create_navigation_buttons(current_index, total_players):
    """Cria botões de navegação (Anterior/Próximo)."""
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Botão "Anterior" (desabilitado se for o primeiro jogador)
    btn_prev = types.InlineKeyboardButton(
        text="◀️ Anterior",
        callback_data=f"player_{current_index - 1}" if current_index > 0 else "ignored"
    )
    
    # Botão "Próximo" (desabilitado se for o último jogador)
    btn_next = types.InlineKeyboardButton(
        text="Próximo ▶️",
        callback_data=f"player_{current_index + 1}" if current_index < total_players - 1 else "ignored"
    )
    
    keyboard.add(btn_prev, btn_next)
    return keyboard