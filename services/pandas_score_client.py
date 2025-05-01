from services.api_client import APIClient
import time

FURIA_ID = 124530 

class PandaScoreClient(APIClient):
    """
    Cliente para interagir com a API PandaScore para dados de partidas de CS:GO/CS2.

    Estende a classe APIClient para realizar requisições à API PandaScore, com suporte a
    autenticação via chave de API e cache para otimizar chamadas frequentes. Projetada para
    obter dados de partidas, como a última partida finalizada da FURIA (opponent_id: 124530).

    Attributes:
        base_url (str): URL base da API PandaScore para CS:GO/CS2
            ('https://api.pandascore.co/csgo').
        api_key (str): Chave de autenticação da API.
        _cache (Dict[str, Dict]): Cache interno para armazenar respostas de requisições,
            com dados e timestamp.
        _cache_ttl (int): Tempo de vida do cache em segundos (default: 300).
    """
    
    def __init__(self, api_key: str):
        """
        Inicializa o cliente PandaScore com a chave de API.

        Configura a URL base da API PandaScore para CS:GO/CS2 e inicializa o cache para
        evitar requisições redundantes à API.

        Args:
            api_key (str): Chave de autenticação da API PandaScore.

        """
        super().__init__("https://api.pandascore.co/csgo", api_key=api_key)

        # Cache para evitar multiplas requisições
        self._cache = {
            "ultima_partida": {"data": [], "cache_timestamp": 0},
            "proximas_partidas": {"data": [], "cache_timestamp": 0},
            "partida_andamento": {"data": [], "cache_timestamp": 0},
            "time_completo": {"data": [], "cache_timestamp": 0}
        }

        self._cache_ttl = 300

    async def get_UltimaPartida(self):
        """
        Obtém os dados da última partida finalizada da FURIA em CS:GO.

        Verifica se há dados válidos no cache (menos de 300 segundos). Se o cache estiver
        válido, retorna os dados armazenados. Caso contrário, faz uma requisição à API
        PandaScore para obter a última partida finalizada da FURIA (opponent_id: 124530),
        armazena o resultado no cache e o retorna.

        Returns:
            list: Lista contendo um dicionário com os dados da última partida, incluindo
                campos como 'opponents', 'results', 'winner', e 'streams_list'.

        Example:
            >>> client = PandaScoreClient("sua-chave")
            >>> partida = await client.get_Ultima_Partida()
            >>> print(partida)
            [{'opponents': [...], 'results': [...], 'winner': {...}, ...}]
        """
        if time.time() - self._cache["ultima_partida"]["cache_timestamp"] < self._cache_ttl:
            return self._cache["ultima_partida"]["data"]
        
        # Somente faço uma nova requisicao se caso nao tenha dado algum em cache
        try:

            dados = await self._request(
                method="GET",
                endpoint=f"/matches",
                params=
                {
                    "filter[status]": "finished",
                    
                    "filter[opponent_id]": FURIA_ID,
                    "sort": "-begin_at",
                    "page[size]": 1
                }
            )

            self._cache["ultima_partida"] = {"data": dados, "cache_timestamp": time.time()}
            return dados
        except Exception as e:
            print(f"Não foi possivel realizar a requisição a Ultima partida da Furia: ERRO {e}\n\n")
            return []
    
    async def get_ProximasPartidas(self):
        """Retorna a Proxima Partida da Furia"""
        if time.time() - self._cache["proximas_partidas"]["cache_timestamp"] < self._cache_ttl:
            return self._cache["proximas_partidas"]["data"]

        try:
            dados = await self._request(
                method="GET",
                endpoint="matches/upcoming",
                params=
                {
                    "filter[opponent_id]": FURIA_ID
                }
            )

            self._cache["proximas_partidas"] = {"data": dados, "cache_timestamp": time.time()}
        
            return dados
        except Exception as e:
            print(f"Nao foi possivel realizar a requisição a Proximas Partidas da Furia: ERRO {e}\n\n")
            return []

    async def get_PartidaEmAndamento(self):
        if time.time() - self._cache["partida_andamento"]["cache_timestamp"] < self._cache_ttl:
            return self._cache["partida_andamento"]["data"]
        
        try:
            dados = await self._request(
                method="GET",
                endpoint="matches/running",
                params=
                {
                    "filter[opponent_id]": FURIA_ID
                }
            )

            self._cache["partida_andamento"] = {"data": dados, "cache_timestamp": time.time()}

            return dados
        except Exception as e:
            print(f"Nao foi possivel fazer a requisição para partidas em andamento: ERRO {e}\n\n")
            return []
        
    async def get_Time(self):
        """
        Retorna a composição do time completo da FURIA
        """
        if time.time() - self._cache["time_completo"]["cache_timestamp"] < self._cache_ttl:
            return self._cache["time_completo"]["data"]
        try:

            dados = await self._request(
                method="GET",
                endpoint="/teams",
                params=
                {
                    "filter[id]": FURIA_ID
                }
            )

            self._cache["time_completo"] = {"data": dados, "cache_timestamp": time.time()}
            return dados
        except Exception as e:
            print(f"Nao foi possivel realizar a requisição a get_Team: ERRO {e}\n\n")
            return []