from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room
import random
import string
import requests
from flask_cors import CORS
from logica_jogo import validar_palpite, proximo_jogador

app = Flask(__name__)
app.config['SECRET_KEY'] = 'seusegredo'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

salas = {}

def gerar_codigo_sala():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route('/')
def index():
    return "Página inicial do jogo (você vai fazer o front separado)"

@app.route('/criar_sala', methods=['POST'])
def criar_sala():
    tema = request.json.get('tema', 'numeros')
    if tema not in ['numeros', 'matematica', 'geografia']:
        return jsonify({'erro': 'Tema inválido.'}), 400

    sala_id = gerar_codigo_sala()

    if tema == 'numeros':
        salas[sala_id] = {
            'jogadores': [],
            'numero_secreto': random.randint(1, 100),
            'vez': 0,
            'tentativas': {},
            'tema': tema,
        }
    else:
        resp = requests.get('https://opentdb.com/api.php?amount=1&type=multiple')
        pergunta = resp.json()['results'][0]['question']
        resposta_correta = resp.json()['results'][0]['correct_answer']
        salas[sala_id] = {
            'jogadores': [],
            'pergunta': pergunta,
            'resposta_correta': resposta_correta,
            'vez': 0,
            'tentativas': {},
            'tema': tema,
        }

    return jsonify({'sala_id': sala_id, 'tema': tema})

@socketio.on('entrar_sala')
def entrar_sala(data):
    sala_id = data['sala_id']
    nome_jogador = data['nome']

    if sala_id not in salas:
        emit('erro', {'mensagem': 'Sala não encontrada.'}, room=request.sid)
        return

    if not nome_jogador:
        emit('erro', {'mensagem': 'Nome do jogador não pode ser vazio.'}, room=request.sid)
        return

    if len(nome_jogador) > 20:
        emit('erro', {'mensagem': 'Nome muito grande, deve ter até 20 caracteres.'}, room=request.sid)
        return

    if nome_jogador.isnumeric():
        emit('erro', {'mensagem': 'O nome não pode ser apenas números.'}, room=request.sid)
        return

    if not any(c.isalpha() for c in nome_jogador):
        emit('erro', {'mensagem': 'O nome deve conter pelo menos uma letra.'}, room=request.sid)
        return

    if nome_jogador in [j['nome'] for j in salas[sala_id]['jogadores']]:
        emit('erro', {'mensagem': 'Nome já está em uso na sala, por favor escolha outro.'}, room=request.sid)
        return

    if len(salas[sala_id]['jogadores']) >= 5:
        emit('erro', {'mensagem': 'Sala cheia'}, room=request.sid)
        return

    salas[sala_id]['jogadores'].append({'nome': nome_jogador, 'sid': request.sid})
    join_room(sala_id)
    
    emit('jogador_entrar', {'nome': nome_jogador}, room=sala_id)
    
    # Enviar lista atualizada de jogadores para todos na sala
    nomes = [j['nome'] for j in salas[sala_id]['jogadores']]
    emit('lista_jogadores', {'jogadores': nomes}, room=sala_id)

    if len(salas[sala_id]['jogadores']) == 1:
        emit('sua_vez', {}, room=request.sid)

@socketio.on('palpite')
def fazer_palpite(data):
    sala_id = data['sala_id']
    palpite = data['palpite']
    sid = request.sid

    sala = salas.get(sala_id)
    if not sala:
        emit('erro', {'mensagem': 'Sala não encontrada.'}, room=sid)
        return

    tema = sala.get('tema')

    jogadores = sala['jogadores']
    vez = sala['vez']

    if not jogadores or jogadores[vez]['sid'] != sid:
        emit('erro', {'mensagem': 'Não é sua vez!'}, room=sid)
        return

    nome = jogadores[vez]['nome']
    sala['tentativas'][nome] = sala['tentativas'].get(nome, 0) + 1

    if tema == 'numeros':
        palpite_validado, erro = validar_palpite(palpite)
        if erro:
            emit('erro', {'mensagem': erro}, room=sid)
            return

        numero_secreto = sala['numero_secreto']
        if palpite_validado == numero_secreto:
            emit('numero_correto', {'mensagem': f'{nome} acertou em {sala["tentativas"][nome]} tentativas!'}, room=sala_id)
            emit('partida_finalizada', {'mensagem': 'Deseja jogar novamente? (s/n)'}, room=sala_id)
        else:
            dica = 'maior' if palpite_validado < numero_secreto else 'menor'
            emit('numero_incorreto', {'mensagem': f'O número é {dica}.', 'tentativas': sala['tentativas'][nome]}, room=sid)
            proximo_sid = proximo_jogador(sala)
            emit('sua_vez', {}, room=proximo_sid)
    else:
        resposta_correta = sala['resposta_correta']
        if palpite.strip().lower() == resposta_correta.strip().lower():
            emit('resposta_correta', {'mensagem': f'{nome} acertou a pergunta em {sala["tentativas"][nome]} tentativas!'}, room=sala_id)
            emit('partida_finalizada', {'mensagem': 'Deseja jogar novamente? (s/n)'}, room=sala_id)
        else:
            emit('resposta_incorreta', {'mensagem': 'Resposta incorreta. Tente novamente.', 'tentativas': sala['tentativas'][nome]}, room=sid)
            proximo_sid = proximo_jogador(sala)
            emit('sua_vez', {}, room=proximo_sid)

@socketio.on('resposta_reiniciar')
def resposta_reiniciar(data):
    sala_id = data['sala_id']
    resposta = data['resposta'].lower()
    if sala_id in salas:
        if resposta == 's':
            sala = salas[sala_id]
            sala['vez'] = 0
            sala['tentativas'] = {}
            if sala['tema'] == 'numeros':
                sala['numero_secreto'] = random.randint(1, 100)
            else:
                resp = requests.get('https://opentdb.com/api.php?amount=1&type=multiple')
                pergunta = resp.json()['results'][0]['question']
                sala['pergunta'] = pergunta
                sala['resposta_correta'] = resp.json()['results'][0]['correct_answer']
            emit('nova_partida', {}, room=sala_id)
            if sala['jogadores']:
                emit('sua_vez', {}, room=sala['jogadores'][0]['sid'])
        else:
            emit('fim_de_jogo', {'mensagem': 'Partida finalizada. Obrigado por jogar!'}, room=sala_id)

@socketio.on('disconnect')
def desconectar():
    sid = request.sid
    for sala_id, sala in list(salas.items()):
        jogadores = sala['jogadores']
        for i, jogador in enumerate(jogadores):
            if jogador['sid'] == sid:
                jogadores.pop(i)
                emit('jogador_sair', {'nome': jogador['nome']}, room=sala_id)
                
                nomes = [j['nome'] for j in jogadores]
                emit('lista_jogadores', {'jogadores': nomes}, room=sala_id)
                
                if not jogadores:
                    del salas[sala_id]
                else:
                    if i < sala['vez']:
                        sala['vez'] -= 1
                    if sala['vez'] >= len(jogadores):
                        sala['vez'] = 0
                    emit('sua_vez', {}, room=jogadores[sala['vez']]['sid'])
                break

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
