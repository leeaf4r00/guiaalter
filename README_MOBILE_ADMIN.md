# 📱 Dashboard Mobile Administrativo

Sistema de dashboard administrativo mobile-friendly para o Guia de Alter, com suporte para acesso local e externo via Cloudflare Tunnel.

## ✨ Funcionalidades

- 🔐 **Autenticação Segura:** Login integrado com banco de dados existente
- 📊 **Estatísticas em Tempo Real:** Visualize métricas de usuários, tours e atividades
- 📱 **Mobile-First:** Interface otimizada para celular (mas funciona em desktop também)
- 🌐 **Acesso Local:** Via Wi-Fi na mesma rede
- 🚀 **Acesso Externo:** Via internet usando Cloudflare Tunnel
- 🔄 **Atualização Automática:** Pull-to-refresh e botão de atualização

## 🚀 Início Rápido

### 1. Criar Usuário Admin

Primeiro, você precisa ter um usuário administrador no banco de dados.

**Opção A: Via Python (Recomendado)**

Crie o arquivo `create_admin.py` na raiz do projeto:

```python
from app import create_app, db
from app.models.users import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Verificar se admin já existe
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print("❌ Usuário 'admin' já existe!")
    else:
        # Criar novo admin
        admin = User(
            username='admin',
            email='admin@guiadealter.com',
            password=generate_password_hash('admin123'),  # MUDE ESTA SENHA!
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuário admin criado com sucesso!")
        print("   Username: admin")
        print("   Senha: admin123")
        print("   ⚠️  IMPORTANTE: Mude a senha após o primeiro login!")
```

Execute:
```bash
python create_admin.py
```

**Opção B: Via Flask Shell**

```bash
python
>>> from app import create_app, db
>>> from app.models.users import User
>>> from werkzeug.security import generate_password_hash
>>> app = create_app()
>>> with app.app_context():
...     admin = User(username='admin', email='admin@guiadealter.com', 
...                  password=generate_password_hash('admin123'), is_admin=True)
...     db.session.add(admin)
...     db.session.commit()
>>> exit()
```

### 2. Iniciar o Servidor

```bash
python run.py
```

O servidor estará rodando em: `http://localhost:5000`

### 3. Acessar o Dashboard

**No computador:**
```
http://localhost:5000/mobile-admin/login
```

**No celular (mesma rede Wi-Fi):**
1. Descubra o IP do seu computador:
   - Windows: `ipconfig` (procure por IPv4)
   - Linux/Mac: `ifconfig` ou `ip addr`
2. No celular, acesse: `http://[SEU-IP]:5000/mobile-admin/login`
   - Exemplo: `http://192.168.1.100:5000/mobile-admin/login`

**Credenciais padrão:**
- Username: `admin`
- Senha: `admin123` (ou a que você definiu)

## 🌐 Acesso Externo (Cloudflare Tunnel)

Para acessar o dashboard de qualquer lugar via internet:

### Método Rápido (Quick Tunnel)

1. **Inicie o servidor:**
   ```bash
   python run.py
   ```

2. **Em outro terminal, inicie o tunnel:**
   ```bash
   cloudflared tunnel --url http://localhost:5000
   ```

3. **Copie a URL gerada** (algo como `https://abc-123.trycloudflare.com`)

4. **Acesse no celular:**
   ```
   https://abc-123.trycloudflare.com/mobile-admin/login
   ```

### Método Automático (Script)

**Windows:**
```bash
run-with-cloudflare.bat
```

**Linux/Mac:**
```bash
chmod +x run-with-cloudflare.sh
./run-with-cloudflare.sh
```

### Configuração Permanente

Para URL fixa e configuração avançada, veja: [docs/cloudflare-tunnel-setup.md](docs/cloudflare-tunnel-setup.md)

## 📱 Usando no Celular

### Adicionar à Tela Inicial (PWA-like)

**iPhone (Safari):**
1. Abra o dashboard no Safari
2. Toque no ícone de compartilhar (quadrado com seta)
3. Role e toque em "Adicionar à Tela de Início"
4. Dê um nome (ex: "Admin Guia Alter")
5. Toque em "Adicionar"

**Android (Chrome):**
1. Abra o dashboard no Chrome
2. Toque nos três pontos (⋮)
3. Toque em "Adicionar à tela inicial"
4. Dê um nome
5. Toque em "Adicionar"

Agora você terá um ícone na tela inicial do celular!

### Gestos

- **Pull-to-refresh:** Arraste para baixo no topo da página para atualizar
- **Botão de atualização:** Toque no botão flutuante (🔄) no canto inferior direito

## 🔒 Segurança

### Boas Práticas

1. **Mude a senha padrão imediatamente**
2. **Use senhas fortes:** Mínimo 12 caracteres, letras, números e símbolos
3. **HTTPS em produção:** Cloudflare Tunnel já fornece automaticamente
4. **Rate limiting:** Sistema já implementado (5 tentativas/minuto)
5. **Apenas admins:** Somente usuários com `is_admin=True` podem acessar

### Proteção de Rotas

Todas as rotas do dashboard exigem:
- ✅ Login válido (`@login_required`)
- ✅ Permissão de admin (`@admin_required`)

Tentativas de acesso não autorizado retornam erro 403.

## 📊 API Endpoints

Todos os endpoints requerem autenticação de admin.

### GET `/mobile-admin/api/stats`
Retorna estatísticas gerais do sistema.

**Resposta:**
```json
{
  "users": {
    "total": 42,
    "admins": 3,
    "recent": 5
  },
  "tours": {
    "total": 15,
    "active": 12,
    "inactive": 3
  },
  "system": {
    "timestamp": "2024-11-23T12:00:00",
    "admin_name": "admin"
  }
}
```

### GET `/mobile-admin/api/users?limit=10&offset=0`
Lista usuários cadastrados.

**Parâmetros:**
- `limit` (opcional): Número de resultados (padrão: 10)
- `offset` (opcional): Paginação (padrão: 0)

**Resposta:**
```json
{
  "users": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "is_admin": true,
      "created_at": "2024-11-23T10:00:00"
    }
  ],
  "total": 42,
  "limit": 10,
  "offset": 0
}
```

### GET `/mobile-admin/api/tours?limit=10&offset=0`
Lista tours cadastrados.

### GET `/mobile-admin/api/activity`
Retorna atividade recente (últimos usuários e tours criados).

## 🛠️ Estrutura de Arquivos

```
guiaalter/
├── app/
│   ├── routes_mobile_admin.py      # Blueprint do dashboard mobile
│   └── __init__.py                  # Registro do blueprint
├── templates/
│   └── mobile_admin/
│       ├── login.html               # Página de login mobile
│       └── dashboard.html           # Dashboard principal
├── docs/
│   └── cloudflare-tunnel-setup.md   # Guia completo Cloudflare
├── run-with-cloudflare.bat          # Script Windows
└── README_MOBILE_ADMIN.md           # Este arquivo
```

## 🐛 Troubleshooting

### Não consigo fazer login
- ✅ Verifique se criou um usuário admin
- ✅ Confirme username e senha
- ✅ Verifique se `is_admin=True` no banco de dados

### Dashboard não carrega no celular (Wi-Fi)
- ✅ Servidor está rodando? (`python run.py`)
- ✅ Celular na mesma rede Wi-Fi?
- ✅ IP correto? Use `ipconfig` (Windows) ou `ifconfig` (Linux/Mac)
- ✅ Firewall bloqueando? Libere porta 5000

### Cloudflare Tunnel não funciona
- ✅ Cloudflared instalado? (`cloudflared --version`)
- ✅ Servidor rodando antes do tunnel?
- ✅ Aguardou 1-2 minutos após iniciar?
- ✅ Veja: [docs/cloudflare-tunnel-setup.md](docs/cloudflare-tunnel-setup.md)

### Erro 403 (Forbidden)
- ✅ Usuário é admin? Verifique `is_admin=True` no banco
- ✅ Fez login corretamente?

### API retorna erro 500
- ✅ Verifique logs do servidor
- ✅ Banco de dados está acessível?
- ✅ Modelos User e Tour existem?

## 📚 Documentação Adicional

- [Cloudflare Tunnel Setup](docs/cloudflare-tunnel-setup.md) - Guia completo de configuração
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Cloudflare Tunnel Docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)

## 💡 Dicas

1. **Favoritos:** Salve a URL nos favoritos do celular
2. **Tela Inicial:** Adicione ícone na home do celular (veja seção acima)
3. **Modo Escuro:** Use o modo escuro do navegador para melhor visualização
4. **Notificações:** Configure alertas no Cloudflare Dashboard
5. **Backup:** Mantenha backup das credenciais do Cloudflare

## 🎯 Próximos Passos

Sugestões de melhorias futuras:
- [ ] Gráficos de estatísticas (Chart.js)
- [ ] Notificações push
- [ ] Modo offline (Service Worker)
- [ ] Edição de usuários/tours
- [ ] Logs de atividade detalhados
- [ ] Exportação de relatórios

## 📞 Suporte

Problemas ou dúvidas? Abra uma issue no repositório do projeto.

---

**Desenvolvido para Guia de Alter** 🌴
