# TELEGRAM CHAT BOT

## Estrutura de Diretórios
Abaixo está a estrutura do projeto, com uma explicação de cada diretório e arquivo principal:

### Descrição dos Diretórios e Arquivos:
- **`app/`**: Contém todo o código relacionado à aplicação Flask.
  - **`__init__.py`**: Arquivo que inicializa a aplicação, registrando as rotas, extensões e configurando o app.
  - **`models.py`**: Contém os modelos do banco de dados (usando SQLAlchemy, por exemplo).
  - **`routes/`**: Diretório para organizar as rotas/endpoints da aplicação.
    - **`user.py`**: Exemplo de arquivo de rotas relacionado a usuários.
  - **`services/`**: Lógica de negócio e funções que interagem com os modelos.
    - **`user_service.py`**: Exemplo de serviço de usuários.
  - **`templates/`**: Arquivos HTML utilizados para renderização no Flask (separação entre backend e frontend).
    - **`base.html`**: Template base que pode ser herdado por outros templates.
  - **`static/`**: Contém arquivos estáticos como CSS, imagens e JavaScript.
    - **`style.css`**: Exemplo de arquivo CSS para estilização.
    - **`script.js`**: Exemplo de arquivo JavaScript.
  - **`forms.py`**: Contém os formulários da aplicação (caso use Flask-WTF).
  - **`config.py`**: Arquivo com configurações da aplicação (como variáveis de ambiente).

- **`migrations/`**: Controla as migrações de banco de dados, permitindo modificar a estrutura do banco de forma controlada (usando Flask-Migrate).

- **`tests/`**: Diretório para os testes unitários e de integração.
  - **`test_user.py`**: Exemplo de teste para a funcionalidade de usuários.

- **`venv/`**: Diretório do ambiente virtual. **Não deve ser versionado**, pois pode ser recriado por qualquer desenvolvedor.

- **`.env`**: Arquivo com variáveis de ambiente (ex. credenciais e chaves secretas). **Não deve ser versionado**.

- **`.gitignore`**: Arquivo que lista os arquivos e diretórios que devem ser ignorados pelo Git, como `venv/`, `.env`, e outros arquivos temporários.

- **`README.md`**: Arquivo de documentação do projeto.

- **`requirements.txt`**: Lista de todas as dependências do projeto. Use `pip install -r requirements.txt` para instalar as bibliotecas necessárias.

- **`run.py`**: Ponto de entrada para rodar a aplicação. Executando `python run.py`, o servidor Flask será iniciado.

## Como Configurar o Ambiente de Desenvolvimento

### Passos para iniciar o projeto localmente:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/edgargavioli/telegram-chat-bot.git
   cd telegram-chat-bot
2. **Crie um ambiente virtual .venv**:
   ```bash
   python3 -m venv .venv
   .venv\Scripts\activate
3. **Delete a pasta venv**
4. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
5. **Execute a aplicação**:
   ```bash
   flask run
6. **Para executar a aplicação em debug mode(hotreload)**:
  ```bash
  $env:FLASK_DEBUG = "1" //utilizar comando no vscode usando powershell
  // --------------------------
  // Linux e Mac
  $ export FLASK_APP=run.py
  $ export FLASK_DEBUG=1
Acesse http://localhost:5000/users/greet para ver a página exemplo desse projeto.