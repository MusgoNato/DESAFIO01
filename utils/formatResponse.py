from datetime import datetime

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
        f"🟣 [Assista aos melhores momentos!]({link_stream})\n\n"
        "#FURIA | #CS2"
    )
    
    # Para debug no console
    print(message)

    return {"text": message, "logo": logoVencedor}

        
def formatProximasPartidas(data):
    """Extrai os dados e constroi a mensagem personalizada com as proximas partidas"""
    mensagens = []

    for partida in data:
        # Dados básicos com tratamento de erros
        nome_partida = partida.get("name", "Partida sem nome")
        dataPartida = partida.get("begin_at", "Data desconhecida")
        
        # Processamento dos times
        opponents = partida.get("opponents", [])
        times = [opponent.get("opponent", {}).get("name", "Time desconhecido") for opponent in opponents]
        timesVS = " vs ".join(times) if len(times) > 1 else f"{times[0]} (Adversário não definido)" if times else "Partida sem times definidos"
    
        linkStream = []
        for stream in partida.get("streams_list", []):  # Usar streams da partida atual
            # Aceitar streams principais em inglês, espanhol ou português
            if stream.get("main", False) and stream.get("language") in ["en", "es", "br"]:
                linkStream.append(stream["raw_url"])

        utc_time = datetime.fromisoformat(dataPartida)
        dataLimpa = utc_time.strftime("%d/%m/%Y %H:%M")

        # Construção da mensagem formatada
        mensagem = (
            f"🎮 *{timesVS}* ⚔️\n"
            f"🏆 **{nome_partida}**\n"
            f"📅 *{dataLimpa}*\n"
            f"🔴 Assista ao vivo: {', '.join(linkStream)}\n"
        )
        
        mensagens.append(mensagem)

    # Junta todas as mensagens e adiciona cabeçalho
    return "\n".join([f"Vem torcer com a gente FURIOSO(A)🔥\n"] + mensagens) if mensagens else "Infelizmente não tem partidas ainda 😭"

def formatPartidaEmAndamento(data):
    """Retorno das informações formatadas para mensagem do bot, para partidas em andamento"""
    
    # indices diretos em data pois ao ter uma partida rodando, o valor da API
    nomePartida = data[0].get("name", "Nome indisponivel")
    nomeSerie = data[0]["serie"].get("full_name", "Serie indisponivel")
    valorPartida = data[0]["tournament"].get("prizepool", "Valor não disponivel")
    stream = data[0]["streams_list"][0].get("raw_url", "Link indisponivel")

    message = (
        f"🏆 {nomePartida} {nomeSerie} 🏆\n"
        f"🤑 {valorPartida}\n"
        f"🔴[Assista ao vivo]({stream})"
    )

    return message

def format_player_page(player):
    """Formata a mensagem de uma página (um jogador)."""        
    message = (
        f"👤 *{player.get('name', 'Sem nome')}*\n"
        f"   - 🎂 Idade: {player.get('age', '?')} anos\n"
        f"   - 🏳️ Nacionalidade: {player.get('nationality', '?')}\n"
        f"   - 📅 Aniversário: {player.get('birthday', 'Não informado')}\n"
    )
    return message