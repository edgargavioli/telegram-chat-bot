**TELEGRAM CHAT BOT**

**Estrutura de Diretórios**
-Abaixo está a estrutura do projeto, com uma explicação de cada diretório e arquivo principal:

-Descrição dos Diretórios e Arquivos:

**telegram-chat-bot**

├──**app**

│   ├──**` __init__.py `**        # Inicializa o aplicativo Flask e configurações gerais

│   ├──**` models.py   `**         # Modelos do banco de dados (ex.: SQLAlchemy)

│   ├── **`routes`**           # Diretório para rotas/endpoints

│   │   └──**` user.py  `**        # Exemplo de rota para gerenciamento de usuários

│   ├── **`services`**         # Lógica de negócio e interação com os modelos

│   │   └──**`user_service.py `** # Exemplo de serviço para usuários

│   ├──**`templates`**          # Arquivos HTML para renderização

│   │   └── **`base.html`**     # Template base reutilizável

│   ├──**static`**             # Arquivos estáticos (CSS, JS, imagens)

│   │   ├──**` style.css`**       # Estilização

│   │   └── **`script.js`**     # Lógica frontend

│   ├──**`forms.py`**             # Formulários (opcional, ex.: Flask-WTF)

│   └──**` config.py`**            # Configurações do aplicativo (ex.: variáveis de ambiente)

├── **`migrations`**             # Controla as migrações do banco de dados (Flask-Migrate)

├──**` tests`**                  # Testes unitários e de integração

├──**`venv`**                 # Ambiente virtual (não versionado)

├──**`.env`**                    # Variáveis de ambiente (não versionado)

├──**`.gitignore`**               # Arquivos/diretórios ignorados pelo Git

├──**` README.md `**               # Documentação do projeto

├── **`requirements.txt`**           # Lista de dependências do projeto

└── **`run.py`**                   # Ponto de entrada da aplicação


- **`migrations`**: Controla as migrações de banco de dados, permitindo modificar a estrutura do banco de forma controlada (usando Flask-Migrate).

- **`tests`**: Diretório para os testes unitários e de integração.
  - **`test_user.py`**: Exemplo de teste para a funcionalidade de usuários.

- **`venv`**: Diretório do ambiente virtual. **Não deve ser versionado**, pois pode ser recriado por qualquer desenvolvedor.

- **`.env`**: Arquivo com variáveis de ambiente (ex. credenciais e chaves secretas). **Não deve ser versionado**.

- **`.gitignore`**: Arquivo que lista os arquivos e diretórios que devem ser ignorados pelo Git, como `venv/`, `.env`, e outros arquivos temporários.

- **`README.md`**: Arquivo de documentação do projeto.

- **`requirements.txt`**: Lista de todas as dependências do projeto. Use `pip install -r requirements.txt` para instalar as bibliotecas necessárias.

- **`run.py`**: Ponto de entrada para rodar a aplicação. Executando `python run.py`, o servidor Flask será iniciado.

**`Como Configurar o Ambiente de Desenvolvimento`**

**`Passos para iniciar o projeto localmente:`**

1. **`Clonar o repositório`**:
   ```bash
   git clone https://github.com/edgargavioli/telegram-chat-bot.git
   cd telegram-chat-bot
   
2. **Crie e Ativar o Ambiente Virtual**:
   ```bash
   Windows:
   python3 -m venv .venv
   .venv\Scripts\activate
   Linux/Mac:
   python3 -m venv .venv
   source .venv/bin/activate
   
3. **Delete a pasta venv`**
  
4. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   
5. **Execute a aplicação**:
   ```bash
   flask run
   
6. **Modo Debug(Hot Reload)**:

    ```bash
  Windows (PowerShell):
  $env:FLASK_DEBUG = "1" //utilizar comando no vscode usando powershell
  flask run

  Linux e Mac
  $ export FLASK_APP=run.py
  $ export FLASK_DEBUG=1
  flask run

7.**`Testando o Projeto`**:

Acesse http://localhost:5000/users/greet //Para ver a página exemplo desse projeto.

Observações:

-Certifique-se de que o arquivo .env está configurado corretamente com as credenciais e chaves secretas necessárias.
-Não versione os diretórios venv/ e arquivos sensíveis como .env. Use o .gitignore para garantir isso.

8.**`DOCKER`**

-Rodar a aplicação em Docker

-Criar e rodar o container:
  docker-compose up --build


**`Passo a Passo para Configurar o Bot no Celular`**
  
Siga os passos abaixo para acessar e configurar o bot:
  
-Instalar o Telegram;

-Certifique-se de que o aplicativo Telegram está instalado no seu celular;

-Abrir o Telegram;

-Entre no aplicativo Telegram com sua conta;

-Acessar o BotFather;

-Procure pelo usuário @BotFather no Telegram e inicie uma conversa com ele;

-Criar um Bot;

Siga as instruções fornecidas pelo BotFather para criar um novo bot;

Obter o Token e o Username do Bot;

Após criar o bot, o BotFather fornecerá o Token e o Username;

Copie essas informações;

Configurar o Projeto
-Insira o Token e o Username no arquivo config.py e no .env, localizados na raiz do projeto.

-Exemplo de como o .env deve ficar:

BOT_TOKEN=seu_token_aqui
BOT_USERNAME=seu_username_aqui

Rodar o Projeto:

-Escolha uma das opções abaixo para rodar o projeto:

Pelo arquivo main.py:

python main.py

Pelo Docker Compose:

docker-compose up

Pronto! Seu bot está configurado e pronto para uso. 🎉
