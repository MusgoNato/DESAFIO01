def formatUltimaPartida(data):
    """Formata os dados da última partida de Counter-Strike retornados pela API PandaScore.

    Extrai informações como nomes dos times, placar, vencedor, logo do vencedor e link do stream
    para criar uma mensagem formatada em Markdown, ideal para envio via Telegram.

    Args:
        data (list): Lista contendo um dicionário com os dados da partida, conforme retornado por
            `PandaScoreClient.get_Ultima_Partida()`. Espera campos como `opponents`, `results`,
            `winner`, e `streams_list`.

    Returns:
        dict: Dicionário com duas chaves:
            - text (str): Mensagem formatada em Markdown com detalhes da partida (times, placar,
              vencedor, link do stream).
            - logo (str or None): URL da logo do time vencedor ou None se não disponível.

    Raises:
        KeyError: Se os campos esperados em `data` (ex.: `opponents`, `winner`) estiverem ausentes
            ou malformados. Nesse caso, retorna um dicionário com uma mensagem de erro em `text`
            e `logo` como None.

    Example:
        >>> data = [{"opponents": [...], "results": [...], "winner": {...}, "streams_list": [...]}]
        >>> result = formatUltimaPartida(data)
        >>> print(result)
        {
            'text': '🔥 Última batalha da FURIA...',
            'logo': 'https://cdn.pandascore.co/images/team/image/3272/...'
        }
    """
    # nome dos times
    furia = data[0]["opponents"][0]["opponent"]["name"]
    timeAnonimo = data[0]["opponents"][1]["opponent"]["name"]

    # Score dos Times
    scoreFuria = data[0]["results"][0]["score"]
    scoreTimeAnonimo = data[0]["results"][1]["score"]

    # Nome do Vencedor e sua logo
    vencedor = data[0]["winner"]["name"]
    logoVencedor = data[0]["winner"]['image_url']

    # nome da Serie
    season = data[0]["serie"]['full_name']

    # Variavel personalizada para caso o time perca ou venca
    msgVencedor = "Parabéns ao adversário, mas a FURIA vai voltar mais forte!" if scoreFuria < scoreTimeAnonimo else "🔥SÓ VEM QUE A FURIA TÁ LIGADA!!!🔥"

    link_stream = None

    # Varrer a lista pelo ultimo elemento, reduz o tempo, pois eh comum que a stream official fique na ultima posicao (Porem pode mudar!)
    for stream in data[0]['streams_list'][::-1]:
        print(stream)
        if (stream['official'] == True) and (stream['language'] == 'en' or stream['language'] == 'br'):
            link_stream = stream['raw_url']
            print(link_stream)
            break
        else:
            # Sem streams para outra idioma
            link_stream = '#'

    # Construção da mensagem do bot
    message = (
        f"🔥 Última batalha da FURIA no {season}! 🐈‍⬛\n\n"
        f"{furia} ({scoreFuria}) VS {timeAnonimo} ({scoreTimeAnonimo})\n\n"
        f"🏆 Vitória dos {vencedor}! {msgVencedor} 💪\n\n"
        f"📺 [Assista aos melhores momentos!]({link_stream})\n\n"
        "#FURIA | #CS2"
    )
    
    # Para debug no console
    print(message)

    return {"text": message, "logo": logoVencedor}

        