# logica basica do jogo no modo multiplayer
def validar_palpite(palpite):
    try:
        palpite = int(palpite)
        if 1 <= palpite <= 100:
            return palpite, None
        else:
            return None, 'O palpite deve ser entre 1 e 100.'
    except (ValueError, TypeError):
        return None, 'Palpite inválido. Digite um número inteiro.'

def proximo_jogador(sala):
    sala['vez'] = (sala['vez'] + 1) % len(sala['jogadores'])
    return sala['jogadores'][sala['vez']]['sid']