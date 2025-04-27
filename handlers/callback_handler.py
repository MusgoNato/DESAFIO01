from telebot.async_telebot import AsyncTeleBot
from services.pandas_score_client import PandaScoreClient
from utils.formatResponse import formatUltimaPartida

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