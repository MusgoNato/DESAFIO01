# api_client.py (arquivo separado)
import aiohttp
from typing import Optional, Dict, Any, List

class APIClient:
    """Classe base para todas as requisições HTTP assíncronas"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.strip('/')
        self.api_key = api_key

    async def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """Método central para todas as requisições"""
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
