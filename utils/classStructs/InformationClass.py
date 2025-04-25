class Torneio:
    def __init__(self, id, nome, inicio, fim, premiacao, liga, serie, partidas):
        self.id = id
        self.nome = nome
        self.inicio = inicio
        self.fim = fim
        self.premiacao = premiacao
        self.liga = liga
        self.serie = serie
        self.partidas = partidas

class Partida:
    def __init__(self, id, nome, status, inicio, tipo, jogos, streams, vencedor):
        self.id = id
        self.nome = nome
        self.status = status
        self.inicio = inicio
        self.tipo = tipo
        self.jogos = jogos
        self.streams = streams
        self.vencedor = vencedor

class Stream:
    def __init__(self, idioma, url):
        self.idioma = idioma
        self.url = url

class Liga:
    def __init__(self, nome, slug):
        self.nome = nome
        self.slug = slug

class Serie:
    def __init__(self, nome, temporada, ano):
        self.nome = nome
        self.temporada = temporada
        self.ano = ano
