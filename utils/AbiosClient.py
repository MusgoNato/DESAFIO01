import requests
from typing import Optional, Dict, Any

class AbiosClient:
    """Classe para inicialização da API Abios Client"""
    
    def __init__(self, url: str, api_key: Optional[str] = None):
        """Inicializa o cliente para a possivel autenticação com o AbiosClient"""

        # Configura headers para autenticação
        self.url = url.strip('/')
        self.api_key = api_key
        self.session = requests.Session()

        # Atualização dos headers caso a api_key a cada requisição feita
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json"
            })

    def _request(self, method: str, endpoint: str, params: Optional[Dict]= None) -> Dict[str, Any]:
        """Metodo interno para execução de requisições"""
        
        # Montagem de minha endpoint para a API
        url = f"{self.url}/{endpoint.lstrip('/')}"
        
        # Tentativa para cada requisição
        try:
            response = self.session.request(
                method = method,
                url = url,
                params = params,
                timeout = 10
            )
            response.raise_for_status()
            
            # Retorna a requisição em formato json se bem sucedida
            return response.json()

        # Tratativa de exceções para erros que possam acontecer
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Erro na requisição : {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Falha na conexão : {str(e)}") 