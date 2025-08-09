#imports
import random
from colorama import init, Fore, Style

init(autoreset=True)

# Declaracao de variáveis
tentativas = 0
palpite = None
recorde = None
recorde = None
jogador_atual = 0


#boas vindas ao jogador
print("-" * 55)
print(Fore.CYAN + " BEM-VINDO AO JOGO DA ADIVINHAÇÃO ".center(55, "-"))
print("-" * 55 + "\n")

nome = input(Fore.YELLOW + "Qual é o seu nome? ").strip().title()

print("\n" + "-" * 55)
print(Fore.GREEN + f"Olá {nome}, vamos começar o jogo!".center(55))
print(Fore.YELLOW + "-" * 55 + "\n")

print(Fore.MAGENTA + "ESCOLHA O MODO DE JOGO:\n")
print(Fore.BLUE + "[1] MODO MULTIPLAYER")
print(Fore.BLUE + "[2] MODO SINGLEPLAYER\n")

while True:
    opcao = input("Digite a opção desejada (1 ou 2): ").strip()
    if opcao == '1':
        print("Você escolheu o MODO MULTIPLAYER.")
        num_jogadores = int(input("Quantos jogadores vão participar? ").strip())
        if num_jogadores > 5:
            print(Fore.RED + "Número máximo de jogadores é 5.!!!!")
            num_jogadores = 5
        nomes_jogadores = []
        for i in range(num_jogadores):
            while True:
                nome_jogador = input(f"Digite o nome do jogador {i + 1}: ").strip().title()
                if len(nome_jogador) == 0:
                    print(Fore.RED + "Nome inválido. Por favor, digite um nome válido.")
                elif len(nome_jogador) > 20:
                    print(Fore.RED + "Nome muito longo. Por favor, digite um nome com até 20 caracteres.")
                elif nome_jogador in nomes_jogadores:
                    print(Fore.RED + "Nome já utilizado. Por favor, escolha outro nome.")
                elif nome_jogador.isnumeric():
                    print(Fore.RED + "O nome não pode ser apenas números.")
                elif not any(c.isalpha() for c in nome_jogador):
                    print(Fore.RED + "O nome deve conter pelo menos uma letra.")
                else:
                    print(Fore.GREEN + f"Bem-vindo {nome_jogador} ao jogo!")
                    nomes_jogadores.append(nome_jogador)
                    break
        break
    elif opcao == '2':
        print("Você escolheu o MODO SINGLEPLAYER.")
        break
    else:
        print("Opção inválida. Por favor, escolha 1 para multiplayer ou 2 para singleplayer.")

numero_secreto = random.randint(1, 100)

# Nivel de dificuldade 
nivel = input("Escolha o nível de dificuldade (1-Fácil, 2-Médio, 3-Difícil): ")
match nivel:
    case '1':
        tentativas_max = 20
    case '2':
        tentativas_max = 10
    case '3':
        tentativas_max = 5
    case _:
        print("Nível inválido. Usando nível fácil por padrão.")
        tentativas_max = 20

#lista de tentativas de cada jogador
if 'num_jogadores' in locals() and num_jogadores > 1:
    tentativas_jogadores = [0] * num_jogadores
else:
    tentativas_jogadores = None
while True:
    numero_secreto = random.randint(1, 100)
    tentativas = 0
    jogador_atual = 0
    while True:
        if tentativas_jogadores:
            print(f"Vez de {nomes_jogadores[jogador_atual]}")
        while True:
            try:
                palpite = int(input("Digite um número entre 1 e 100: "))
                if 1 <= palpite <= 100:
                    break
            except ValueError:
                print("Inválido. Por favor, digite um número inteiro.")

        tentativas += 1
        if tentativas_jogadores:
            tentativas_jogadores[jogador_atual] += 1

        if palpite < numero_secreto:
            print("Mais alto!")
        elif palpite > numero_secreto:
            print("Mais baixo!")
        else:
            if tentativas_jogadores:
                print(f"Parabéns {nomes_jogadores[jogador_atual]}! Você acertou o número secreto em {tentativas_jogadores[jogador_atual]} tentativas.")
                print("Tentativas de cada jogador:")
                for idx, nome in enumerate(nomes_jogadores):
                    print(f"{nome}: {tentativas_jogadores[idx]} tentativas")
            else:
                print(f"Parabéns {nome}! Você acertou o número secreto em {tentativas} tentativas.")

            # Comparativo do recorde
            if recorde is None or tentativas < recorde:
                recorde = tentativas
                print(f"Novo recorde! Seu melhor resultado é {recorde} tentativas.")
            else:
                print(f"Seu recorde atual é {recorde} tentativas.")
            break
        if tentativas >= tentativas_max:
            print(f"Você atingiu o número máximo de tentativas ({tentativas_max}). O número secreto era {numero_secreto}.")
            break
        # Alterna o jogador se multiplayer
        if tentativas_jogadores:
            jogador_atual = (jogador_atual + 1) % num_jogadores
    print("jogar novamente? (s/n)")
    if input().strip().lower() != 's':
        print("Obrigado por jogar!")
        break

