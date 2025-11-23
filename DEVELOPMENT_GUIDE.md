# 📚 Guia de Desenvolvimento - Guia de Alter

## 🏛️ Arquitetura Modular

Este projeto foi construído com uma arquitetura modular para facilitar manutenção e escalabilidade.

## 📦 Componentes do Sistema

### 1. Template Base (`templates/base.html`)

O template base é o coração do sistema modular. Ele define a estrutura comum de todas as páginas.

**Blocos disponíveis:**

```jinja2
{% block title %}          # Título da página (meta tag)
{% block meta_description %}  # Descrição SEO
{% block meta_keywords %}   # Palavras-chave SEO
{% block og_title %}        # Open Graph title
{% block og_description %}  # Open Graph description
{% block extra_css %}       # CSS adicional
{% block header %}          # Header (pode ser sobrescrito)
{% block navigation %}      # Navbar (pode ser sobrescrito)
{% block content %}         # Conteúdo principal
{% block footer %}          # Footer (pode ser sobrescrito)
{% block extra_scripts %}   # JavaScript adicional
```

### 2. Componentes Reutilizáveis

#### Header (`templates/components/header.html`)

- Logo e branding
- Navegação de autenticação
- Status do usuário
- Responsivo

**Variáveis disponíveis:**
- `current_user.is_authenticated`
- `current_user.username`
- `current_user.is_admin`

#### Navbar (`templates/components/navbar.html`)

- Menu principal
- Menu hamburguer (mobile)
- Estados ativos automáticos
- Ícones Font Awesome

**Variáveis disponíveis:**
- `request.endpoint` (para estados ativos)

#### Footer (`templates/components/footer.html`)

- Informações de contato
- Links legais
- Redes sociais
- Copyright dinâmico

**Variáveis disponíveis:**
- `current_year` (injetado globalmente)

## 🎨 Sistema de CSS Modular

### Variáveis CSS Globais (`:root`)

Todas definidas em `static/css/main.css`:

```css
/* Gradientes */
--primary-gradient
--secondary-gradient
--tropical-gradient
--sunset-gradient
--forest-gradient

/* Cores */
--color-primary
--color-secondary
--color-accent
--color-text
--color-text-light
--color-bg
--color-white

/* Sombras */
--shadow-sm
--shadow-md
--shadow-lg
--shadow-xl

/* Transições */
--transition-fast
--transition-smooth
--transition-slow
```

### Arquivos CSS

1. **main.css** - Estilos globais, conteúdo principal
2. **header.css** - Estilos do header
3. **navbar.css** - Estilos da navegação
4. **footer.css** - Estilos do rodapé

## 🔧 Como Criar uma Nova Página

### Passo 1: Criar o Template

```jinja2
{% extends "base.html" %}

{% block title %}Minha Nova Página - Guia de Alter{% endblock %}

{% block meta_description %}
Descrição da minha página para SEO
{% endblock %}

{% block content %}
<section class="my-section">
    <h1>Minha Nova Página</h1>
    <p>Conteúdo aqui...</p>
</section>
{% endblock %}

{% block extra_css %}
<style>
    .my-section {
        padding: 60px 20px;
        max-width: 1200px;
        margin: 0 auto;
    }
</style>
{% endblock %}
```

### Passo 2: Criar a Rota

Em `app/routes.py`:

```python
@routes.route('/minha-pagina')
def minha_pagina():
    return render_template('minha_pagina.html')
```

### Passo 3: Adicionar ao Menu (opcional)

Em `templates/components/navbar.html`:

```html
<li class="nav-item">
    <a href="/minha-pagina" class="nav-link">
        <i class="fas fa-star"></i> Minha Página
    </a>
</li>
```

## 🎨 Padrões de Design

### Cards

```html
<div class="card">
    <h3>Título do Card</h3>
    <p>Descrição</p>
</div>

<style>
.card {
    background: white;
    padding: 30px;
    border-radius: 16px;
    box-shadow: var(--shadow-md);
    transition: var(--transition-smooth);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}
</style>
```

### Botões

```html
<!-- Botão Primário -->
<button class="btn-primary">
    <i class="fas fa-check"></i> Confirmar
</button>

<!-- Botão Secundário -->
<button class="btn-secondary">
    <i class="fas fa-times"></i> Cancelar
</button>

<style>
.btn-primary {
    padding: 15px 35px;
    background: var(--primary-gradient);
    color: white;
    border: none;
    border-radius: 50px;
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition-smooth);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}
</style>
```

### Formulários

```html
<form class="modern-form">
    <div class="form-group">
        <label for="campo">Nome do Campo</label>
        <div class="input-wrapper">
            <i class="fas fa-user"></i>
            <input type="text" 
                   class="form-control" 
                   id="campo" 
                   placeholder="Digite aqui">
        </div>
    </div>
</form>

<style>
.form-group {
    margin-bottom: 25px;
}

.input-wrapper {
    position: relative;
}

.input-wrapper i {
    position: absolute;
    left: 18px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--color-primary);
}

.form-control {
    width: 100%;
    padding: 15px 15px 15px 50px;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    transition: var(--transition-smooth);
}

.form-control:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
</style>
```

## 🔐 Autenticação

### Proteger uma Rota

```python
from flask_login import login_required, current_user

@routes.route('/pagina-protegida')
@login_required
def pagina_protegida():
    return render_template('protegida.html')
```

### Verificar Admin

```python
@routes.route('/admin-only')
@login_required
def admin_only():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    return render_template('admin.html')
```

### No Template

```jinja2
{% if current_user.is_authenticated %}
    <p>Olá, {{ current_user.username }}!</p>
{% else %}
    <a href="{{ url_for('routes.login') }}">Fazer Login</a>
{% endif %}
```

## 📱 Responsividade

### Breakpoints Padrão

```css
/* Mobile First */
@media (max-width: 480px) {
    /* Smartphones */
}

@media (max-width: 768px) {
    /* Tablets portrait */
}

@media (max-width: 992px) {
    /* Tablets landscape */
}

@media (max-width: 1200px) {
    /* Desktop pequeno */
}
```

### Função clamp() para Texto Responsivo

```css
h1 {
    font-size: clamp(2rem, 5vw, 3.5rem);
    /* min: 2rem, ideal: 5vw, max: 3.5rem */
}
```

## 🎭 Animações

### Animações Disponíveis

```css
/* Fade In Up */
.element {
    animation: fadeInUp 0.8s ease-out;
}

/* Slide In */
.element {
    animation: slideIn 0.6s ease-out;
}

/* Float (loop) */
.element {
    animation: float 20s ease-in-out infinite;
}
```

### Criar Nova Animação

```css
@keyframes myAnimation {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.my-element {
    animation: myAnimation 0.6s ease-out;
}
```

## 🗄️ Banco de Dados

### Criar um Novo Modelo

```python
# Em app/models/meu_modelo.py
from app import db

class MeuModelo(db.Model):
    __tablename__ = 'meus_modelos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    def __repr__(self):
        return f'<MeuModelo {self.nome}>'
```

### Criar Tabelas

```python
from app import app, db

with app.app_context():
    db.create_all()
```

## 📝 Boas Práticas

### 1. Sempre Use o Template Base

✅ Correto:
```jinja2
{% extends "base.html" %}
```

❌ Evite duplicar HTML completo

### 2. CSS Inline Apenas para Estilos Únicos

✅ Correto: Estilos específicos da página em `{% block extra_css %}`

❌ Evite: Estilos inline nas tags HTML

### 3. JavaScript no Final

✅ Correto: Use `{% block extra_scripts %}`

❌ Evite: Scripts no meio do HTML

### 4. Use Variáveis CSS

✅ Correto:
```css
color: var(--color-primary);
```

❌ Evite:
```css
color: #667eea;
```

### 5. Ícones Semânticos

✅ Correto:
```html
<i class="fas fa-home"></i> Início
```

❌ Evite: Ícones sem significado

## 🚀 Performance

### Lazy Loading para Iframes

```html
<iframe src="..." loading="lazy" title="Descrição"></iframe>
```

### Otimizar Imagens

- Use WebP quando possível
- Defina width e height
- Use lazy loading

```html
<img src="image.webp" 
     width="800" 
     height="600" 
     loading="lazy" 
     alt="Descrição">
```

## 🧪 Testes

### Testar em Diferentes Telas

1. Chrome DevTools (F12)
2. Responsive Design Mode
3. Testar em dispositivos reais

### Checklist antes de Deploy

- [ ] Todas as páginas herdam de `base.html`
- [ ] Todos os links funcionam
- [ ] Formulários validam corretamente
- [ ] Responsivo em mobile/tablet/desktop
- [ ] Meta tags SEO preenchidas
- [ ] Sem erros no console
- [ ] Imagens otimizadas
- [ ] Performance OK (Lighthouse)

## 📞 Suporte

Para dúvidas ou problemas:
- Consulte o README.md
- Verifique a estrutura de pastas
- Revise os componentes existentes
- Use os padrões estabelecidos

---

**Happy Coding! 🚀**
