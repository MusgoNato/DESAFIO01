# Funções uteis para retornos
import json

def getJsonData():
    """Cria um arquivo json e o retorna"""
    with open('dataAPIScore.json', 'r', encoding='utf-8') as f:
        return json.load(f)
