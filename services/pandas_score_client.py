from typing import Optional, Dict, Any
import aiohttp
from services.api_client import APIClient
import time

class PandaScoreClient(APIClient):
    """Classe para inicialização da API PandaScore"""
    
    def __init__(self, api_key: str):
        """Inicializa o cliente para a possivel autenticação com o Pandas Score"""
        super().__init__("https://api.pandascore.co/csgo", api_key=api_key)

        # Cache para evitar multiplas requisições
        self._cache = {"ultima_partida": {"data": None, "cache_timestamp": 0}}
        self._cache_ttl = 300

    async def get_Ultima_Partida(self):
        """"Retorno de ultima partida realizada no CS GO"""
        if time.time() - self._cache["ultima_partida"]["cache_timestamp"] < self._cache_ttl:
            print("Retornando dados em cache")
            return self._cache["ultima_partida"]["data"]
        
        print("Fazendo requisição a API novamente!")

        # Somente faço uma nova requisicao se caso nao tenha dado algum em cache
        dados = await self._request(
            method="GET",
            endpoint=f"/matches",
            params=
            {
                "filter[status]": "finished",
                "filter[opponent_id]": 124530,
                "sort": "-begin_at",
                "page[size]": 1
            }
        )

        self._cache["ultima_partida"] = {"data": dados, "cache_timestamp": time.time()}
        return dados