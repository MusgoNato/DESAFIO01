# Funções uteis para retornos
import json

def getJsonData():
    """Le o arquivo criado"""
    with open('partidas.json', 'r', encoding='utf-8') as fPartidas:
        return json.load(fPartidas)

def makeJsonTorneios(response):
    """Cria o arquivo da enpoint de Torneios de CS"""
    with open('torneios.json', 'w', encoding='utf-8') as fTorneio:
        json.dump(response, fTorneio, ensure_ascii=False, indent=4)
    
def getTorneios():
    """Retorna o arquivo lido criado anteriormente com makejsonTorneios"""
    with open('torneios.json', 'r', encoding='utf-8') as file:
        return json.load(file)