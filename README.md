# 🌴 Guia de Alter - Plataforma de Turismo

> Seu guia completo para explorar o Caribe Amazônico

[![Flask](https://img.shields.io/badge/Flask-3.0.1-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)

## 📋 Sobre o Projeto

Plataforma moderna e responsiva para guia de turismo em Alter do Chão, desenvolvida com Flask e design premium. O sistema oferece uma experiência completa para explorar passeios, hotéis, pacotes e muito mais no paraíso amazônico.

## ✨ Características

- **Design Moderno**: Interface premium com gradientes tropicais, glassmorphism e animações suaves
- **Arquitetura Modular**: Sistema organizado com templates base e componentes reutilizáveis
- **Responsivo**: 100% adaptável para desktop, tablet e mobile
- **Sistema de Autenticação**: Login seguro com Flask-Login
- **SEO Otimizado**: Meta tags, Open Graph e estrutura semântica
- **Performance**: Lazy loading, animações otimizadas e cache

## 🏗️ Estrutura do Projeto

```
guiaalter/
├── app/
│   ├── __init__.py
│   ├── routes.py              # Rotas principais
│   ├── routes_admin.py        # Rotas administrativas
│   ├── routes_tours.py        # Rotas de passeios
│   ├── models/
│   │   ├── users.py           # Modelo de usuários
│   │   └── clients.py         # Modelo de clientes
│   ├── forms.py               # Formulários WTForms
│   └── database.py            # Configuração do banco
├── templates/
│   ├── base.html              # Template base (herança)
│   ├── components/
│   │   ├── header.html        # Componente de cabeçalho
│   │   ├── navbar.html        # Componente de navegação
│   │   └── footer.html        # Componente de rodapé
│   ├── index.html             # Página inicial
│   ├── login.html             # Página de login
│   └── ...                    # Outras páginas
├── static/
│   ├── css/
│   │   ├── main.css           # Estilos principais
│   │   ├── header.css         # Estilos do header
│   │   ├── navbar.css         # Estilos da navbar
│   │   └── footer.css         # Estilos do footer
│   ├── js/
│   │   ├── script.js          # Scripts gerais
│   │   └── user.js            # Scripts de usuário
│   └── img/                   # Imagens
├── data/
│   └── database.db            # Banco de dados SQLite
├── app.py                     # Aplicação principal
├── requirements.txt           # Dependências
└── README.md                  # Este arquivo
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Virtualenv (recomendado)

### Passos

1. **Clone o repositório**
   ```bash
   git clone <repositório>
   cd guiaalter
   ```

2. **Crie e ative um ambiente virtual**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente (opcional)**
   ```bash
   # Crie um arquivo .env
   FLASK_DEBUG=True
   SECRET_KEY=sua_chave_secreta_aqui
   ```

5. **Inicialize o banco de dados**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

6. **Execute a aplicação**
   ```bash
   python app.py
   ```

7. **Acesse no navegador**
   ```
   http://localhost:5000
   ```

## 🎨 Sistema de Design

### Paleta de Cores

```css
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--tropical-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
--sunset-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
--forest-gradient: linear-gradient(135deg, #0ba360 0%, #3cba92 100%);
```

### Tipografia

- **Principal**: Inter (Google Fonts)
- **Títulos**: Poppins (Google Fonts)

### Efeitos

- Glassmorphism: `backdrop-filter: blur(10px)`
- Sombras suaves: `box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15)`
- Transições: `cubic-bezier(0.4, 0, 0.2, 1)`

## 📱 Componentes Modulares

### Template Base (`base.html`)

Template principal que define a estrutura padrão de todas as páginas:

```jinja2
{% extends "base.html" %}

{% block content %}
  <!-- Seu conteúdo aqui -->
{% endblock %}
```

### Componentes

- **Header**: Logo, branding e autenticação
- **Navbar**: Navegação principal com menu responsivo
- **Footer**: Contato, links e redes sociais

## 🔒 Autenticação

Sistema de login implementado com Flask-Login:

- Registro de usuários
- Login seguro com hash de senha
- Sessões persistentes
- Controle de acesso administrativo

## 🛠️ Tecnologias

- **Backend**: Flask 3.0.1
- **ORM**: Flask-SQLAlchemy
- **Autenticação**: Flask-Login
- **Formulários**: Flask-WTF, WTForms
- **Banco de Dados**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Ícones**: Font Awesome 6.4.0
- **Fontes**: Google Fonts (Inter, Poppins)

## 📝 Uso

### Criar uma Nova Página

1. Crie um template que herda de `base.html`:

```jinja2
{% extends "base.html" %}

{% block title %}Título da Página{% endblock %}

{% block content %}
  <h1>Conteúdo da Página</h1>
{% endblock %}
```

2. Adicione a rota em `app/routes.py`:

```python
@routes.route('/minha-pagina')
def minha_pagina():
    return render_template('minha_pagina.html')
```

### Adicionar CSS Customizado

```jinja2
{% block extra_css %}
<style>
  /* Seus estilos */
</style>
{% endblock %}
```

### Adicionar JavaScript

```jinja2
{% block extra_scripts %}
<script>
  // Seu código
</script>
{% endblock %}
```

## 🚀 Deploy

### Heroku

O projeto já está configurado com `Procfile` e `gunicorn`:

```bash
git push heroku main
```

### Outras Plataformas

Configure a variável de ambiente `PORT` e execute:

```bash
gunicorn app:app
```

## 📄 Licença

Este projeto é de código fechado. Todos os direitos reservados.

## 👥 Contato

- **WhatsApp**: (93) 99116-0523
- **Email**: guiadealter@contato.com

---

**Feito com ❤️ em Alter do Chão**
