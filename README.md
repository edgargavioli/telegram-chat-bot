# **Telegram Chat Bot**

## **Estrutura de Diretórios**

O projeto de **Telegram Chat Bot** segue a estrutura abaixo para organizar os arquivos de forma modular, facilitando o desenvolvimento e manutenção.

```
telegram-chat-bot/
├── api/                        # Controladores e modelos da API
│   ├── controllers/            # Controladores da API
│   │   ├── categories_controller.py  # Controlador para categorias
│   │   ├── clients_controller.py    # Controlador para clientes
│   │   ├── orders_controller.py     # Controlador para pedidos
│   │   ├── orders_items_controller.py # Controlador para itens de pedidos
│   │   ├── products_controller.py   # Controlador para produtos
│   │   ├── user_controller.py       # Controlador para usuários
│   │   └── messages_controller.py   # Controlador para mensagens
│   └── models/                  # Modelos do banco de dados
│       └── categories.py        # Modelo de categorias
│       └── clients.py           # Modelo de clientes
│       └── db.py                # Instancia do SQLAlchemy
│       └── messages.py          # Modelo de mensagens
│       └── order_items.py       # Modelo de Produtos e Pedidos
│       └── orders.py            # Modelo de Pedidos
│       └── products.py          # Modelo de Produtos
│       └── users.py             # Modelo de Usuários
├── app/                         # Aplicação Flask (configurações, rotas, serviços)
│   ├── __init__.py              # Inicializa o aplicativo Flask
│   ├── config.py                # Configurações gerais do aplicativo
│   ├── forms.py                 # Formulários (opcional, ex.: Flask-WTF)
│   ├── routes/                  # Rotas/endpoints da aplicação
│   ├── services/                # Lógica de negócios (interação com modelos)
│   ├── static/                  # Arquivos estáticos (CSS, JS, imagens)
│   └── templates/               # Templates HTML para renderização
├── bot/                         # Lógica do bot do Telegram
│   ├── commands/                # Comandos do bot
│   │   └── <command_files>.py   # Definições de comandos para o bot
│   ├── config.py                # Configurações específicas do bot
│   ├── Dockerfile               # Arquivo Docker para o bot
│   ├── main.py                  # Arquivo principal que inicia o bot
│   ├── requirements.txt         # Dependências do bot
│   └── wait-for-it.sh           # Script para esperar por serviços dependentes
├── instance/                    # Arquivos específicos da instância (ex.: banco de dados SQLite)
├── migrations/                  # Migrações do banco de dados (Flask-Migrate)
│   ├── alembic.ini              # Arquivo de configuração do Alembic
│   ├── env.py                   # Configuração do ambiente de migração
│   ├── README                   # Documentação das migrações
│   ├── script.py.mako           # Template para scripts de migração
│   └── versions/                # Versões das migrações
├── tests/                       # Testes unitários e de integração
│   ├── __init__.py              # Inicializa o pacote de testes
│   └── test_user.py             # Exemplo de teste para a funcionalidade de usuários
├── .env                         # Variáveis de ambiente (ex.: credenciais e chaves secretas)
├── .gitignore                   # Arquivos/diretórios a serem ignorados pelo Git (ex. venv/, .env)
├── docker-compose.yml           # Arquivo Docker Compose para orquestração de containers
├── Dockerfile                   # Arquivo Docker para a aplicação
├── init.sql                     # Script SQL para inicializar o banco de dados
├── main.py                      # Ponto de entrada da aplicação
├── README.md                    # Documentação do projeto
└── requirements.txt             # Lista de dependências do projeto
```
## **Como Configurar o Ambiente de Desenvolvimento**

### **Passos para Iniciar o Projeto Localmente**

1. **Clonar o Repositório**
   ```bash
   git clone https://github.com/edgargavioli/telegram-chat-bot.git
   cd telegram-chat-bot
   ```

2. **Criar e Ativar o Ambiente Virtual**
   - **Windows**:
     ```bash
     python3 -m venv .venv
     .venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instalar as Dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar o Arquivo `.env`**
   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:
   
   **Exemplo de `.env`**:
   ```bash
   SECRET_KEY=mysecretkey
   DATABASE_URL=mysql+pymysql://root:root@db:3306/telegram_bot_db
   TELEGRAM_TOKEN=TOKEN_DO_SEU_BOT
   ```

5. **Configurar o Arquivo `config.py`**
   
   No arquivo `app/config.py`, insira o token do seu bot e outras informações relevantes:

   **Exemplo de `config.py`**:
   ```python
   from typing import Final

   TOKEN: Final = "TOKEN_DO_SEU_BOT"
   BOT_USERNAME = "@NOME_DO_SEU_BOT"
   API_URL = "http://web:5000/api"
   IMG_PREFIX = "http://web:5000/static/img/produtos/"

   cart = {}
   waiting_city = {}
   waiting_address = {}
   waiting_number = {}
   ```

6. **Executar a Aplicação**
   Após configurar os arquivos necessários, execute o servidor Flask:

   ```bash
   flask run
   ```

7. **Testando a Aplicação**
   Acesse [http://localhost:5000/](http://localhost:5000/) para ver a página de login.

   **Criando um usuário padrão no MySQL**:
   Execute o seguinte comando no MySQLWorkbench:
   ```sql
   use telegram_bot_db;
   insert into users (name, username, password, role) values ("adm","adm","scrypt:32768:8:1$ZjnHI75BJDnhP1XU$d6196d74f79f5354c99b9b573226576b3825012ea72eec782b9f956ad9594e3ddb582f4afa62ad66f17ee884137ceb466d92af1729327857be81abd570f4d7c6","Admin");
   ```

   - Após isso, faça login com:
     - **Usuário**: `adm`
     - **Senha**: `adm`

---

## **Como Rodar o Bot**

1. **Entrar no Diretório do Bot**
   ```bash
   cd bot
   ```

2. **Instalar as Dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar o Bot**
   ```bash
   python main.py
   ```

---

## **Como Rodar com Docker**

1. **Configurar `.env` e `config.py` do Bot**
   Certifique-se de que o token do seu bot está configurado corretamente nos arquivos `.env` e `config.py`.

   **Exemplo de `config.py`**:
   ```python
   TOKEN: Final = "{TOKEN_DO_SEU_BOT}"
   BOT_USERNAME = "@{NOME_DO_SEU_BOT}"
   API_URL = "http://web:5000/api"
   IMG_PREFIX = "http://web:5000/static/img/produtos/"
   ```

   **Exemplo de `.env`**:
   ```bash
   SECRET_KEY=mysecretkey
   DATABASE_URL=mysql+pymysql://root:root@db:3306/telegram_bot_db
   TELEGRAM_TOKEN=TOKEN_DO_SEU_BOT
   ```

2. **Construir e Rodar o Docker**
   Se você deseja usar Docker, execute o seguinte comando para construir e rodar os containers:
   ```bash
   docker-compose up --build
   ```

---

### **Observações Finais**

- **Arquivo `.env`**: Não versionado, contém informações sensíveis como credenciais. Crie seu próprio `.env` baseado no `.example.env`.
- **Gitignore**: Certifique-se de que os diretórios `venv/` e arquivos como `.env` estão listados no `.gitignore` para evitar que sejam versionados.

# Informações sobre o desenvolvimento:

- Trabalhamos com hash de senha dos usuários do admin painel
- Rotas protegidas que só podem ser acessadas com o token de segurança
- Rotas sem proteção para que o bot possa acesa-la
- WebSocket para a maior parte da conversação direta do bot com o front
