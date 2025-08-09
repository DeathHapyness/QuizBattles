# Multiplayer Quiz Game

## Descrição

Este é um jogo multiplayer de perguntas e respostas com temas variados (números, matemática, geografia), desenvolvido em Python usando Flask e Flask-SocketIO para comunicação em tempo real.

Os jogadores podem criar salas, entrar nelas, e jogar turnos para tentar acertar números secretos ou responder perguntas. O sistema gerencia turnos, valida respostas, e permite reiniciar partidas.

## Funcionalidades

- Criação e gerenciamento de salas de jogo
- Suporte a múltiplos temas: números, matemática, geografia
- Validação de nomes de jogadores (únicos na sala, não vazios, etc.)
- Turnos para envio de palpites ou respostas
- Contagem de tentativas por jogador
- Indicação de acertos e dicas para números
- Recebimento de perguntas via API externa para temas de quiz
- Comunicação em tempo real via WebSocket
- Controle de desconexões e atualização de turnos
- Opção para reiniciar partida ou finalizar jogo

## Tecnologias Utilizadas

- Python 3.x
- Flask
- Flask-SocketIO
- Requests (para chamadas à API de perguntas)
- API externa de perguntas (Open Trivia Database)

## Estrutura do Projeto

/seu-projeto
|-- README.md
|-- multipayer/
|-- app.py
|-- logica_jogo.py
|-- outros arquivos
|-- requirements.txt

## Como Rodar

1. Clone este repositório

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

```

## Instale as dependências:

- pip install -r requirements.txt

## Execute o servidor Flask:

- python app.py

## Acesse o jogo no navegador em:

- http://localhost:5000
