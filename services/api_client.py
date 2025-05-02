import aiohttp
from typing import Optional, Dict, Any

class APIClient:
    """
    Cliente base para requisições HTTP assíncronas a APIs externas.

    Fornece uma interface genérica para realizar requisições HTTP (GET, POST, etc.) usando
    aiohttp, com suporte a autenticação via chave de API e personalização de parâmetros e
    cabeçalhos. Projetada para ser estendida por classes específicas, como clientes para a
    API PandaScore.

    Attributes:
        base_url (str): URL base da API, sem barras finais.
        api_key (str, optional): Chave de autenticação da API, usada em cabeçalhos
            Authorization, se fornecida.
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Inicializa o cliente HTTP com a URL base e uma chave de API opcional.

        Args:
            base_url (str): URL base da API (ex.: 'https://api.pandascore.co').
            api_key (str, optional): Chave de autenticação da API. Se None, não adiciona
                cabeçalho Authorization. Defaults to None.
        """
        self.base_url = base_url.strip('/')
        self.api_key = api_key

    async def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Executa uma requisição HTTP assíncrona e retorna a resposta em JSON.

        Método central para realizar requisições HTTP com o método especificado (GET, POST,
        etc.), incluindo parâmetros de consulta e cabeçalhos personalizados. Adiciona
        automaticamente o cabeçalho Authorization se uma chave de API estiver configurada.
        Lida com erros de conexão e respostas HTTP inválidas.

        Args:
            method (str): Método HTTP (ex.: 'GET', 'POST').
            endpoint (str): Endpoint da API, relativo à URL base (ex.: 'matches').
            params (Dict, optional): Parâmetros de consulta a serem incluídos na URL.
                Defaults to None.
            headers (Dict, optional): Cabeçalhos HTTP adicionais. Mesclados com o cabeçalho
                Authorization, se aplicável. Defaults to None.

        Returns:
            Dict[str, Any]: Resposta da API parseada como dicionário JSON.

        Example:
            >>> client = APIClient('https://api.pandascore.co', 'sua-chave')
            >>> response = await client._request('GET', 'matches', params={'page': 1})
            >>> print(response)
            {'matches': [...]}
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Headers padrão + customizados
        final_headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        if headers:
            final_headers.update(headers)

        async with aiohttp.ClientSession(headers=final_headers) as session:
            try:
                async with session.request(
                    method=method,
                    url=url,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    response.raise_for_status()
                    return await response.json()
                    
            except aiohttp.ClientResponseError as e:
                raise Exception(f"Erro HTTP {e.status}: {e.message}")
            except aiohttp.ClientError as e:
                raise Exception(f"Erro de conexão: {str(e)}")
