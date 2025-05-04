# FURIA CS BOT
![FURIA CS BOT Logo](https://arena.rtp.pt/wp-content/uploads/2021/01/furiagg_wallpaper_raian-860x507-1.jpg)

## Demonstração
[Assista ao vídeo](https://youtu.be/x7IyvGeUCUo)

## Linguagens Utilizadas
- **Python**: Utilizado para toda a lógica do bot e integração com APIs.

## Descrição do que o Bot Faz
O **FURIA CS BOT** é um bot projetado para a quem quer acompanhar de perto o time da FURIA no Counter-Strike (CS), com foco em fornecer funcionalidades úteis para jogadores, equipes e fãs do cenário competitivo. Suas principais funcionalidades incluem:
- **Relatório da última partida disputada**: Relatório mostrando a equipe vencedora da partida na série disputada, com link de stream para assistir aos melhores momentos.
- **Agenda de próximas Partidas**: Agenda de futuras partidas que serão realizadas pelo time da FURIA.
- **Partidas em jogo**: Relatório simples da partida ao vivo com link da live na Twitch.
- **Escalação do Time completo da Furia**

O bot é altamente configurável e foi projetado para ser escalável, permitindo a adição de novas funcionalidades conforme necessário.

## Instalação
Siga os passos abaixo para instalar e configurar o FURIA CS BOT localmente:

1. **Pré-requisitos**:
    - [Python 3.8 ou superior](https://www.python.org/)
    - [ngrok](https://ngrok.com/)
    - [git](https://git-scm.com/downloads)
    
    - **Bibliotecas Python utilizadas**
        -   `telegram` 
        -   `telebot`
        -   `aiohttp`
        -   `hypercorn`
        -   `quart`
        -   `dotenv`
        -   `datetime`
        -   `asyncio`
        -   `time`
        -   `typing`
        -   `random`
        -   `json`
        -   `datetime`
        -   `os`

2. **Clonar o Repositório**:
Vá no caminho desejado para o projeto, abra o terminal e execute o seguinte código:
```
git clone https://github.com/MusgoNato/DESAFIO01.git
```

3. **Configurar BOT no Telegram**:
    - Vá ao telegram e busque por `BotFather`
    - Após ter encontrado, entre na conversa e digite `/newbot`
    - Dê um nome ao bot (Será mostrado na lista de conversas do chat)
    - Dê o username ao bot (Será o identificador do bot. Ex: meuBot_bot)
    - Após as configurações acima, será gerado um token HTTP API (**GUARDE O TOKEN E NÃO COMPARTILHE**). Ex: `777123456:ABCef7Gh89ijkLmnopQ1rsTuvW-X_YZAbCD2`
    - Busque o bot pela barra de pesquisa Search pelo identicador que você deu ao bot: Ex: meuBot_bot

4. **Configurar ngrok para webhook**:
* É necessário configurar uma webhook para receber os eventos que acontecem no telegram e assim o bot se comunicar com a nossa aplicação, siga os passos abaixo:

    - Faça login na página do ngrok e busque por Setup & Installation
    - Vá a aba download e baixe a versão para o seu Windows
    - Abra o executável, copie a linha de comando encontrada na página do ngrok em `Your Authtoken` e cole no terminal ngrok aberto (**GUARDE O TOKEN E NÃO COMPARTILHE**). Ex da Command Line: `ngrok config add-authtoken seu_authtoken`
    - Após ter configurado o authtoken, execute o seguinte código no terminal do ngrok:
    ```
    ngrok http 5000.
    ```
    * Obs 1: Caso você queira executar em outra porta sem ser a 5000, por exemplo a 8080 ou 8000, você terá que modificar o arquivo .env para o devido funcionamento.
    
    * Obs 2: Para ter certeza que a url esta correta e que está configurada com o telegram, ao acessar a url do ngrok após expor seu localhost, deverá abrir uma página com a seguinte mensagem:
     ```
    Not Found
        
    The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
    ```

# Configuração de variáveis de ambientes
Renomeie o arquivo `.example.env` para `.env`, neste arquivo existem as seguintes variáveis de ambiente:
- `BOT_TOKEN` - Referente ao token do bot gerado no chat do BothFather 
- `API_KEY_PANDAS_SCORE` - Seu token para acesso a API da PandaScore
- `URL_API` - Referente a URL da API pandaScore para o jogo CS (**Não precisa ser modificado**)
- `WEBHOOK_URL`: Referente a URL gerada pelo ngrok após executar ngrok http 5000
- `HOST` : Host padrão (**Não precisa ser modificado**)
- `PORT` : Porta padrão (**Não precisa ser modificado**)

Cada variável deve ser preenchida de acordo com as especificações fornecidas.

# Rodar o bot
1. **Inicie um Ambiente Virutal (*Recomendado*)**

    Para inicializar um abiente virtual em python digite o seguinte código em seu terminal:
    ```
    python -m venv venv
    ```
    Logo após:
    ```
    venv\Scripts\activate
    ```
    Instale as dependências:
    ```
    pip install -r requirements.txt
    ```
    No terminal do ambiente virtual digite o seguinte para executar o bot:
    ```
    py main.py
    ```
    
    Você deverá ver a seguinte mensagem no terminal:
    ```
    ⏳ Configurando webhook: https://url_ngrok_gerada.ngrok-free.app/webhook/777123456:ABCef7Gh89ijkLmnopQ1rsTuvW-X_YZAbCD2

    [2025-04-28 11:24:56 -0400] [24048] [INFO] Running on http://0.0.0.0:5000 (CTRL + C to quit)
    ```

2. **Rodando no termial CMD padrão (Alternativo)**

Após as configurações serem preenchidas, entre na pasta do projeto clonado, abra o terminal (CMD) e digite o seguinte comando para rodar o bot:

```
py main.py
```

Você deverá ver a seguinte mensagem no terminal:
```
⏳ Configurando webhook: https://url_ngrok_gerada.ngrok-free.app/webhook/777123456:ABCef7Gh89ijkLmnopQ1rsTuvW-X_YZAbCD2

[2025-04-28 11:24:56 -0400] [24048] [INFO] Running on http://0.0.0.0:5000 (CTRL + C to quit)
```

# Comandos ao Bot
Comandos disponiveis ao bot:

- Para o menu principal: 
    ```
    /menu
    ```
- Para curiosidades:
    ```
    /curiosidade
    ```

# Erros
- Primeiro verifique todas as variáveis de ambiente se estão corretas:
    - Url gerada pelo ngrok
    - Token do bot Telegram
    - Token da API pandaScore

- *Error code: 429. Description: Too Many Requests: retry after 78751*
    - Esse erro ocorre em algumas ocasiões, quando o bot faz muitos envios a webhook ou por algum motivo relacionado a requisições, ocasionalmente o telegram bloqueia seu bot por um determinado tempo, caso você queira prosseguir terá que aguardar o fim do tempo de bloqueio ou criar um outro BOT no BotFather e modificar o arquivo `.env` 

- *Qualquer erro relacionado a bibliotecas ou módulos do python, veja se você instalou corretamente as dependências do arquivo requirements.txt, mesmo se já foi instalada as dependências continuar dando problemas, tente instalar manualmente cada biblioteca por meio do `pip install {nome_biblioteca}`*