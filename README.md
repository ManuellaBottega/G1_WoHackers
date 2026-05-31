# G1_WoHackers# 🌿 Meu Jardim

Um jogo para que suas plantas reais deixem de ser monótonas e chatas, em vez de morrerem sem motivo aparente, suas plantas murcharão devido a ciúmes e brigas... Tente não se deixar levar pelos pedidos de suas plantas para não perder todo seu jardim!

## Funcionalidades

* **Gestão de Plantas:** Cadastre as plantas que tem em casa dentre as espécies mais comuns (Jiboia, Samambaia, Cacto, etc.), tire uma foto de sua planta para identificá-la.
* **Sistema de Afinidade:** As plantas irão interagir com quem divide o canteiro com elas, mas sendo um mero humano incapaz de ler rivalidades e amores trocados por raízes e partículas de umidade, terá que dar seus pulos para entender o que está acontecendo se não quiser um desestre botânico dentro de casa.
* **Dias e Pedidos:** A cada dia que passa, as plantas geram pedidos no painel. Elas podem pedir água, implorar por uma mudança de sol ou, se estiverem confortáveis, tramar para que a planta vizinha seja jogada pela janela.
* **Impacto das Decisões:** Suas escolhas ao atender pedidos afetam diretamente as pontuações de relacionamento entre as plantas no banco de dados, podendo fazer que elas deixem de se odiar ou amar, ou fazer como que essas relações se intensifiquem ainda mais.

## Aviso de Inutilidade
* **Por quê esse projeto não deveria existir:** Um jogo que mexe com a vida real de pobres plantas, fazendo com que elas tentem ao máximo diminuir a vida útil uma da outra... Me parece uma perda de tempo e dinheiro, embora os humanos adorem se entreter com o caos e sofrimento alheio, matar as próprias plantas por diversão em um jogo que pode durar dias e dias, realmente passa dos limites da falta do que fazer.

## 🛠️ Tecnologias Utilizadas

* **Back-end:** Python, Flask
* **Banco de Dados:** SQLite3 (nativo)
* **Front-end:** HTML5, CSS3, JavaScript (Vanilla API Fetch)

## 🚀 Como executar o projeto localmente (Windows)

Siga os passos abaixo no seu terminal (PowerShell ou CMD) para instalar e iniciar o servidor do jogo:

1. **Abra a pasta do projeto no terminal.**

2. **Crie um ambiente virtual:**
   ```cmd
   python -m venv venv

3. **Ative o ambiente virtual:**
    .\venv\Scripts\activate

4. **Instale as dependências necessárias:**
    pip install -r requirements.txt

5. **Inicie o servidor local:**
    python app.py

6. **Jogue:**
    Abra o seu navegador e acesse o endereço http://127.0.0.1:5000

## Estrutura do Código
* **app.py:** Servidor central Flask, interpretador de pedidos e rotas da API.

* **regras.py:** Motor lógico do jogo. Define dicionários de espécies, afinidades botânicas iniciais, geração de frases de turno e evolução do tempo.

* **banco.py:** Configuração e criação das tabelas de relacionamento e histórico no SQLite.

* **templates/index.html:** Interface visual interativa e responsiva.