import requests
from utils.classStructs.InformationClass import Liga, Torneio, Stream, Partida, Serie

def getSeries(api_key: str):
    """Retorna uma lista dos ganhadores com base no nome do jogador"""

    url = "https://api.pandascore.co/csgo/tournaments?filter[series]="
    params = {
        'page[size]': 10,
        'token': api_key  # Adicione a chave de API como parâmetro
    }

    try:
        response = requests.get(url, params)
        response.raise_for_status()
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Ërro em fazer essa requisição {e}")
        return []
    
def getWinnerById(api_key: str, TeamWinner_id: str):
    """Retorna as informações do time de acordo com o seu ID"""
    url = f"https://api.pandascore.co/csgo/teams?filter[id]={TeamWinner_id}"
    params = {
        'page[size]': 10,
        'token': api_key
    }

    try:
        response = requests.get(url, params)
        response.raise_for_status()
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Ërro em fazer essa requisição {e}")
        return None
    
def jsonForObjects(data):
    """Converte o JSON da API em objetos Python"""
    if not data:
        return []

    objetos_torneio = []
    
    for torneio_data in data:
        # Processar partidas
        partidas = []
        for partida_data in torneio_data.get('matches', []):
            streams = [
                Stream(
                    idioma=stream.get('language'),
                    url=stream.get('raw_url')
                ) for stream in partida_data.get('streams_list', [])
            ]
            
            partidas.append(
                Partida(
                    id=partida_data.get('id'),
                    nome=partida_data.get('name'),
                    status=partida_data.get('status'),
                    inicio=partida_data.get('begin_at'),
                    tipo=partida_data.get('match_type'),
                    jogos=partida_data.get('number_of_games'),
                    streams=streams,
                    vencedor=partida_data['winner_id'] if partida_data['winner_id'] != None else '' 
                )
            )

        # Criar objetos da liga e série
        liga = Liga(
            nome=torneio_data.get('league', {}).get('name'),
            slug=torneio_data.get('league', {}).get('slug')
        )
        
        serie = Serie(
            nome=torneio_data.get('serie', {}).get('name'),
            temporada=torneio_data.get('serie', {}).get('season'),
            ano=torneio_data.get('serie', {}).get('year')
        )

        # Criar objeto do torneio
        torneio = Torneio(
            id=torneio_data.get('id'),
            nome=torneio_data.get('name'),
            inicio=torneio_data.get('begin_at'),
            fim=torneio_data.get('end_at'),
            premiacao=torneio_data.get('prizepool'),
            liga=liga,
            serie=serie,
            partidas=partidas
        )

        objetos_torneio.append(torneio)
    
    return objetos_torneio