from datetime import datetime
import json
import random

def format_UltimaPartida(data):
    """
    Formata os dados da última partida de Counter-Strike retornados pela API PandaScore.

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
        if (stream['official'] == True) and (stream['language'] == 'en' or stream['language'] == 'br'):
            link_stream = stream['raw_url']
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

    return {"text": message, "logo": logoVencedor}

        
def format_ProximasPartidas(data):
    """
        Formata dados de partidas futuras para uma mensagem amigável com marcação.
        Processa uma lista de partidas futuras da API PandaScore, extraindo informações relevantes
        (nomes dos times, data, links de transmissão) e formata em uma string pronta para exibição
        em aplicações de mensagens como Telegram ou Discord.

        Args:
            data (List[Dict]): Lista de dicionários contendo dados brutos de partidas da API.
                Campos esperados por partida:
                - name (str): Nome da partida/torneio
                - begin_at (str): Data/hora
                - opponents (List[Dict]): Lista de oponentes com detalhes dos times
                - streams_list (List[Dict]): Lista de streams de transmissão

        Returns:
            str: Mensagem formatada com:
            - Nomes dos times em formato "Time A vs Time B"
            - Nome do torneio/partida
            - Data/hora localizada formatada (DD/MM/AAAA HH:MM)
            - Links de transmissão relevantes
            - Mensagem padrão caso não haja partidas

        Example:
            >>> partidas = [{
            ...     "name": "BLAST Premier 2023",
            ...     "begin_at": "2023-12-15T19:00:00Z",
            ...     "opponents": [
            ...         {"opponent": {"name": "FURIA"}},
            ...         {"opponent": {"name": "Team Vitality"}}
            ...     ],
            ...     "streams_list": [
            ...         {"main": True, "language": "en", "raw_url": "https://twitch.tv/esl_csgo"}
            ...     ]
            ... }]
            >>> print(formatProximasPartidas(partidas))
            Vem torcer com a gente FURIOSO(A)🔥
            
            🎮 *FURIA vs Team Vitality* ⚔️
            🏆 **BLAST Premier 2023**
            📅 *15/12/2023 16:00*
            🔴 Assista ao vivo: https://twitch.tv/esl_csgo

        Notes:
            - Filtra streams principais em inglês, espanhol ou português
            - Mensagem padrão caso não haja partidas: "Infelizmente não tem partidas ainda 😭"
            - Formato de saída otimizado para Markdown (suporte a negrito/itálico)
        """

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

        for stream in partida.get("streams_list", []):
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

def format_PartidaAndamento(data):
    """
    Formata dados de partidas em andamento para mensagem do bot com marcação.

    Processa os dados de uma partida ativa para gerar uma mensagem formatada com informações
    essenciais: nome da partida, série/torneio, premiação e link de transmissão.

    Args:
        data (List[Dict]): Lista contendo pelo menos um item com dados da partida ativa.
            Campos esperados no primeiro item:
            - name (str): Nome da partida
            - serie (Dict): Dados da série/torneio com campo 'full_name'
            - tournament (Dict): Dados do torneio com campo 'prizepool'
            - streams_list (List[Dict]): Lista de streams de transmissão

    Returns:
        str: Mensagem formatada no padrão:
        - Nome da partida e série/torneio
        - Valor da premiação
        - Link de transmissão ativo (Markdown)
        
        Exemplo de retorno:
        "🏆 ESL Pro League S18 ESL Pro League 🏆
         🤑 $850,000
         🔴[Assista ao vivo](https://twitch.tv/esl_csgo)"

    Example:
        >>> partida = [{
        ...     "name": "ESL Pro League S18",
        ...     "serie": {"full_name": "ESL Pro League"},
        ...     "tournament": {"prizepool": "$850,000"},
        ...     "streams_list": [{"raw_url": "https://twitch.tv/esl_csgo"}]
        ... }]
        >>> print(formatPartidaEmAndamento(partida))
        🏆 ESL Pro League S18 ESL Pro League 🏆
        🤑 $850,000
        🔴[Assista ao vivo](https://twitch.tv/esl_csgo)

    Notes:
        - Assume que sempre existe pelo menos uma partida em andamento (lista não vazia)
        - Usa o primeiro link de transmissão disponível na lista
        - Formatação otimizada para Markdown (links clicáveis)
        - Trata campos inexistentes com valores padrão:
          "Nome indisponivel", "Serie indisponivel", etc.
    """
    
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

def format_PaginaJogador(player):
    """
    Formata os dados de um jogador em uma mensagem estruturada para o bot.

    Converte as informações de um jogador (como nome, idade, nacionalidade e data de nascimento)
    em uma mensagem formatada com emojis e marcação para melhor legibilidade em aplicações de chat.

    Args:
        player (Dict): Dicionário contendo dados do jogador. Campos suportados:
            - name (str): Nome completo/nickname do jogador
            - age (int/str): Idade do jogador
            - nationality (str): Nacionalidade (código de país ou nome completo)
            - birthday (str): Data de nascimento em qualquer formato

    Returns:
        str: Mensagem formatada no seguinte padrão:
        👤 *Nome do Jogador*
           - 🎂 Idade: X anos
           - 🏳️ Nacionalidade: País
           - 📅 Aniversário: Data
    """       
    message = (
        f"👤 *{player.get('name', 'Sem nome')}*\n"
        f"   - 🎂 Idade: {player.get('age', '?')} anos\n"
        f"   - 🏳️ Nacionalidade: {player.get('nationality', '?')}\n"
        f"   - 📅 Aniversário: {player.get('birthday', 'Não informado')}\n"
    )
    return message

def get_Curiosidades():
    """
    Retorna uma curiosidade aleatoriamente

    Args:
        Nenhum

    Returns:   
        str: curiosidade disponivel no arquivo curiosidades.json
    """
    with open('utils/data_curiosidade/curiosidades.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    indice = random.randint(0, len(data) - 1)

    return data[indice]["curiosidade"]