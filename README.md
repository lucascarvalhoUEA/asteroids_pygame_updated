<div align="center">
  <h1>🌌 Asteroids Atualizado</h1>
  <p>Uma versão nova, acelerada e cheia de desafios modernos do jogo clássico Asteroids feito em Pygame.</p>
</div>

---

## 📖 Sobre o Projeto
O jogo original Asteroids foi um dos grandes sucessos da história dos videogames. Neste projeto, **Asteroids Atualizado**, nós reconstruímos aquele sentimento clássico da "tela infinita" (onde se você passa do limite esquerdo da tela, você sai pelo direito). No entanto, injetamos um ritmo muito mais frenético e criamos regras novas para deixar o jogo divertido e te forçar a tomar decisões rápidas o tempo todo!

## ✨ Novidades no Jogo (Features)
A navegação continua fluida: você anda no "vácuo" do espaço deslizando livremente e precisa guiar sua nave com muito cuidado. Mas para deixar a experiência contemporânea, adicionamos 5 novas mecânicas de destaque:

- 👾 **Inimigos Perigosos (UFOs):** Pequenos e grandes Discos Voadores cruzarão o mapa de tempos em tempos tentando destruir sua nave.

- ⚡ **[NOVO] Arrancada de Emergência (Dash):** O antigo salto no hiperespaço sumiu. Agora, você pode acionar uma arrancada extrema para escapar rápido ou passar por asteroides sem sofrer dano nenhum por um curto momento. **Atenção:** Dar o Dash consome sua Pontuação Atual. Esse preço fica cada vez mais caro se você usar o Dash repetidas vezes na mesma "vida". Reflita antes de gastar sua pontuação inteira para sobreviver!

- 🎯 **[NOVO] Combos e Multiplicação:** Quanto melhor você jogar, mais rápida sobe a sua pontuação. Destruir coisas em uma sequência veloz enche seu contador de Combo. Com sorte e precisão, você chegará no nível "x5", podendo ganhar até cinco vezes mais pontos!

- 🔴 **[NOVO] Asteróides Voláteis (Avermelhados):** Se ver uma grande rocha vermelha vindo em sua direção, fuja ou atire com muito cuidado. Elas não se quebram em pequenas pedrinhas como as normais. Quando destruídas, explodem jogando disparos de chumbo perigosos em 8 direções ao mesmo tempo. 

- 🎁 **[NOVO] Itens Especiais (Power-Ups):** Ao quebrar asteroides de tamanho Grande, alguma recompensa solta pode flutuar rumo ao vácuo. Se você pegar a **Esfera Verde** você ativará um Tiro Triplo devastador por alguns segundos. Se for a **Esfera Azul**, sua nave ativará um Escudo. Ele aguenta exatamente **1 batida**, te salvando gratuitamente de perder de vez uma Vida — mas lembre-se: ele desliga sozinho sempre que você avança para uma Nova Onda. 

- 🕳️ **[NOVO] Buracos Negros:** A partir da Onda 2, o espaço corre risco de se abrir. Um Buraco Negro começará pequeno, sugando com pouca força, mas irá encher e alargar a sua visão e perigo nos próximos 15 longos segundos atraindo os discos voadores inimigos, fragmentos de rocha rolando e os canhões dos seus próprios tiros direto pro fosso dele. Mantenha distância máxima!

## ⚙️ Pré-requisitos
Para jogar na sua própria máquina, você precisará ter instalado:
* O [Python 3.10](https://www.python.org/downloads/) (ou alguma versão superior).
* A biblioteca de jogos [Pygame](https://www.pygame.org/) (versão 2.x).

## 🚀 Como instalar e jogar
Para iniciar sua "Run" e mergulhar para dentro das novas mecânicas de forma funcional via terminal, proceda assim passos:

1. Clone ou baixe a pasta do repositório inteiro.
2. (Opcional, porém sugerido por boas práticas) Crie e ative um ambiente novo vazio e limpo do Python usando o comando do terminal:
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
3. Instale localmente dentro da pasta nossa dependência de jogos:
   ```bash
   pip install pygame
   ```
4. Navegue via terminal até a raiz dessa exata e rode o comando pra abrir o game:
   ```bash
   python src/main.py
   ```

## 🎮 Controles da Nave
Sem truques e customizações. Esses são de fácil aprendizado:

| Tecla de Teclado | Como usar a Navegaçao |
| :--- | :--- |
| **Seta Direita / Seta Esquerda** | Aponta o bico de metralhadora da nave para a direita ou esquerda. |
| **Seta Para Cima (Up)** | Liga as turbinas de foguete e acelera a nave pra frente. |
| **Barra de Espaço** | Atira tiros para onde a nave apontar. |
| **Shift Esquerdo (Shift)** | **O Dash:** Usa a arrancada para se desviar de perigos. |
| **Botão ESC (Esquerdo)** | Encerra o jogo instantanemamente. |

## 📁 Entendendo como a Pasta de Código foi montada
Para você que estuda código, deixamos os arquivos bem separados e arrumados em uma hierarquia de funções:
- **`config.py`**: Um arquivo central em formato focado que guarda cores, o quanto custa o Dash e o tempo do Power Up.
- **`game.py`**: É o grande Maestro da Interface. O painel visual que entende se estamos perdidos no Menu ou na partida, etc.
- **`main.py`**: O inicializador do Python, rodando o Pygame Window Display base.
- **`sprites.py`**: As identidades de quem briga pelo espaço (Nave, Meteoros, Bolinhas Azuis/Verde, Tiros) estão configuradas nele com as animações.
- **`systems.py`**: O Juiz do Universo. Ele faz os calculos e define toda hora que a Nave esbarrou no Asteroide vermelho ou tomou um ponto extra no Combo, o que ele dispara como punições ou recompensas.
- **`utils.py`**: As mini rotinas de conta matemática pra quebrar as pedras nas quinas pros calculos de geometria.
