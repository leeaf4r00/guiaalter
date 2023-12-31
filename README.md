
# Guia de Alter

Este projeto é um aplicativo web Flask que fornece uma série de funcionalidades, incluindo autenticação de usuários, exibição de informações estáticas e dinâmicas, e gerenciamento de conteúdo.

## Estrutura do Projeto

O projeto está estruturado como um pacote Python com vários módulos. A estrutura básica é a seguinte:

guiadealter/
│
├──  **init** .py
├── app.py
├── database.py
├── models.py
└── routes.py



### Descrição dos Arquivos

-`__init__.py`: Um arquivo vazio que indica que o diretório é um pacote Python.
-`app.py`: Configura a aplicação Flask e o sistema de login.
-`database.py`: Contém funções para interagir com o banco de dados SQLite.
-`models.py`: Define o modelo `User` para o sistema de autenticação Flask-Login.
-`routes.py`: Define as rotas do aplicativo Flask.

## Configuração e Instalação

Para configurar e executar o projeto, siga estas etapas:

1.**Configuração do Ambiente Virtual:**

- Recomenda-se criar um ambiente virtual para o projeto.
- Execute `python -m venv venv` para criar um ambiente virtual.
- Ative o ambiente virtual com `source venv/bin/activate` (Linux/macOS) ou `venv\Scripts\activate` (Windows).

2.**Instalação de Dependências:**

- Instale as dependências necessárias com `pip install flask flask_login werkzeug`.

3.**Execução do Aplicativo:**

- Navegue até o diretório raiz do projeto e execute `python -m guiadealter.app`.
- Acesse o aplicativo através do navegador em `http://localhost:5000`.

## Funcionalidades

-**Autenticação de Usuários:**

- Login e logout de usuários.
  -**Gerenciamento de Conteúdo:**
- Visualização e interação com conteúdo dinâmico e estático.
  -**Roteamento:**
- Diversas rotas para diferentes funcionalidades do aplicativo.

## Contribuição

Contribuições para o projeto são bem-vindas. Para contribuir, por favor, siga as práticas padrão de desenvolvimento de software e faça pull requests para revisão.

## Licença
