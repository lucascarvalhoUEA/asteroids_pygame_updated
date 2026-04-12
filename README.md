<div align="center">
  <h1>🌌 Asteroids Atualizado</h1>
  <p>Uma versão nova, acelerada e cheia de desafios modernos do jogo clássico Asteroids feito em Pygame.</p>
</div>

---

## 📖 Sobre o Projeto
O jogo original Asteroids foi um dos grandes sucessos da história dos videogames. Neste projeto, **Asteroids Atualizado**, criamos um ritmo um pouco mais acelerado e mecânicas novas para deixar o jogo mais divertido e te forçar a tomar decisões mais rápidas o tempo todo!

## ✨ Novidades no Jogo (Features)
A navegação continua fluida: você navega no vácuo do espaço deslizando livremente e precisa guiar sua nave com muito cuidado. Mas, para deixar a experiência mais interessante, adicionamos 5 novas mecânicas de destaque:

- ⚡ **Arrancada de Emergência (Dash):** O antigo salto no hiperespaço sumiu. Agora, você pode acionar uma arrancada extrema para escapar rápido ou passar por asteroides sem sofrer dano nenhum por um curto momento. **Atenção:** Dar o dash consome uma parte de sua pontuação atual. Esse preço fica cada vez mais caro se você usar o dash repetidas vezes na mesma vida.

- 🎯 **Combos e Multiplicação:** Quanto melhor você jogar, mais rápida sobe a sua pontuação. Destruir coisas em uma sequência veloz enche seu contador de Combo. Com sorte e precisão, você chegará no nível "x5", podendo ganhar até cinco vezes mais pontos!

- 🔴 **Asteróides Vermelhos:** Se ver uma grande rocha vermelha vindo em sua direção, fuja ou atire com muito cuidado. Elas não se quebram em pequenas pedrinhas como as normais. Quando destruídas, explodem jogando disparos de chumbo perigosos em 8 direções ao mesmo tempo. 

- 🎁 **Itens Especiais (Power-Ups):** Ao quebrar asteroides de tamanho Grande, alguma recompensa solta pode flutuar rumo ao vácuo. Se você pegar a **Esfera Verde** você ativará um Tiro Triplo devastador por alguns segundos. Se for a **Esfera Azul**, sua nave ativará um Escudo. Ele aguenta exatamente **1 batida**, te salvando gratuitamente de perder de vez uma vida, mas lembre-se: ele é perdido sempre que você avança para uma nova onda. 

- 🕳️ **Buracos Negros:** A partir da Onda 2, o espaço corre risco de se abrir. Um Buraco Negro começará pequeno, sugando com pouca força, mas irá encher e alargar a sua visão e perigo nos próximos 15 longos segundos atraindo os discos voadores inimigos, fragmentos de rocha rolando e os canhões dos seus próprios tiros direto pro centro dele. Mantenha distância máxima!

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

| Tecla de Teclado | Como usar a Navegaçao |
| :--- | :--- |
| **Seta Direita / Seta Esquerda** | Aponta o bico de metralhadora da nave para a direita ou esquerda. |
| **Seta Para Cima (Up)** | Liga as turbinas de foguete e acelera a nave pra frente. |
| **Barra de Espaço** | Atira tiros para onde a nave apontar. |
| **Shift Esquerdo (Shift)** | **O Dash:** Usa a arrancada para se desviar de perigos. |
| **Botão ESC (Esquerdo)** | Encerra o jogo instantanemamente. |

## 📁 Entendendo como a Pasta de Código foi montada
- **`config.py`**: Um arquivo com as configurações gerais do jogo.
- **`game.py`**: É responsável pela exibição da interface do jogo.
- **`main.py`**: O inicializador do Python, responsável por rodar o jogo.
- **`sprites.py`**: As identidades dos elementos do jogo (Nave, Meteoros, Bolinhas Azuis/Verde, Tiros) estão configuradas nele com as animações.
- **`systems.py`**: As mecânicas do jogo. Responsável por fazer os cálculos e definir toda hora que a Nave esbarrou no Asteroide vermelho ou tomou um ponto extra no Combo, o que ele dispara como punições ou recompensas.
- **`utils.py`**: Arquivo de utilidades para operações matemáticas e geométricas.
