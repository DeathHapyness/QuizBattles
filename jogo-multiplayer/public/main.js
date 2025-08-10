const socket = io('http://localhost:5000')

// Elementos da UI
const telaInicial = document.getElementById('telaInicial') // Você precisa criar isso no HTML
const gameSection = document.getElementById('game')
const codigoSalaSpan = document.getElementById('codigoSala')
const nomeJogadorSpan = document.getElementById('nomeJogador')
const listaJogadoresUl = document.getElementById('listaJogadores')
const chatMensagensDiv = document.getElementById('chatMensagens')
const inputPalpite = document.getElementById('inputPalpite')
const btnEnviarPalpite = document.getElementById('btnEnviarPalpite')
const btnSair = document.getElementById('btnSair')

const nomeInput = document.getElementById('nome')
const temaSelect = document.getElementById('tema')
const salaInput = document.getElementById('salaId')
const btnCriar = document.getElementById('btnCriar')
const btnEntrar = document.getElementById('btnEntrar')
const mensagemDiv = document.getElementById('mensagem')

let salaId = null
let nomeJogador = null

function mostrarMensagem(msg, onGameScreen = false) {
  if (onGameScreen) {
    chatMensagensDiv.textContent += msg + '\n'
    chatMensagensDiv.scrollTop = chatMensagensDiv.scrollHeight
  } else {
    mensagemDiv.textContent += msg + '\n'
    mensagemDiv.scrollTop = mensagemDiv.scrollHeight
  }
}

// Criar sala
btnCriar.onclick = async () => {
  const nome = nomeInput.value.trim()
  const tema = temaSelect.value

  if (!nome) {
    mostrarMensagem('Por favor, digite seu nome.')
    return
  }

  try {
    const res = await fetch('http://localhost:5000/criar_sala', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tema }),
    })
    const data = await res.json()
    if (res.ok) {
      mostrarMensagem(`Sala criada! Código: ${data.sala_id}. Entrando...`)
      entrarNaSala(data.sala_id, nome)
    } else {
      mostrarMensagem(`Erro: ${data.erro || 'Não foi possível criar a sala.'}`)
    }
  } catch {
    mostrarMensagem('Erro ao conectar com o servidor.')
  }
}

btnEntrar.onclick = () => {
  const nome = nomeInput.value.trim()
  const sala = salaInput.value.trim().toUpperCase()

  if (!nome) {
    mostrarMensagem('Por favor, digite seu nome.')
    return
  }
  if (!sala) {
    mostrarMensagem('Por favor, digite o código da sala.')
    return
  }

  entrarNaSala(sala, nome)
}

function entrarNaSala(sala, nome) {
  salaId = sala
  nomeJogador = nome

  codigoSalaSpan.textContent = salaId
  nomeJogadorSpan.textContent = nomeJogador

  gameSection.classList.remove('hidden')
  telaInicial.classList.add('hidden')

  socket.emit('entrar_sala', { sala_id: salaId, nome: nomeJogador })
}

btnEnviarPalpite.onclick = () => {
  const texto = inputPalpite.value.trim()
  if (!texto) return

  socket.emit('palpite', { sala_id: salaId, palpite: texto })

  mostrarMensagem(`Você: ${texto}`, true)

  inputPalpite.value = ''
  inputPalpite.focus()
}

btnSair.onclick = () => {
  gameSection.classList.add('hidden')
  telaInicial.classList.remove('hidden')

  salaId = null
  nomeJogador = null

  listaJogadoresUl.innerHTML = ''
  chatMensagensDiv.textContent = ''
  inputPalpite.value = ''
}

// Eventos do socket
socket.on('erro', (data) => mostrarMensagem(`Erro: ${data.mensagem}`, true))

socket.on('jogador_entrar', (data) =>
  mostrarMensagem(`Jogador ${data.nome} entrou na sala!`, true)
)

socket.on('lista_jogadores', (data) => {
  listaJogadoresUl.innerHTML = ''
  data.jogadores.forEach((j) => {
    const li = document.createElement('li')
    li.textContent = j.nome + (j.nome === nomeJogador ? ' (Você)' : '')
    listaJogadoresUl.appendChild(li)
  })
})

socket.on('lista_jogadores', (data) => {
  listaJogadoresUl.innerHTML = ''
  data.jogadores.forEach((nome) => {
    const li = document.createElement('li')
    li.textContent = nome
    listaJogadoresUl.appendChild(li)
  })
})

socket.on('numero_correto', (data) => mostrarMensagem(data.mensagem, true))
socket.on('numero_incorreto', (data) => mostrarMensagem(data.mensagem, true))
socket.on('resposta_correta', (data) => mostrarMensagem(data.mensagem, true))
socket.on('resposta_incorreta', (data) => mostrarMensagem(data.mensagem, true))
socket.on('partida_finalizada', (data) => mostrarMensagem(data.mensagem, true))
socket.on('nova_partida', () => mostrarMensagem('Nova partida iniciada!', true))
