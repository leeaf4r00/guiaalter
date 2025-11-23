# 📱 Dashboard Administrativo Mobile

Dashboard mobile-friendly para gerenciar o Guia de Alter via celular, com acesso local e externo.

## ✨ Funcionalidades

- ✅ **Autenticação Segura:** Login com usuário e senha (apenas admins)
- ✅ **Interface Mobile-First:** Otimizada para telas de celular
- ✅ **Estatísticas em Tempo Real:** Usuários, tours, admins
- ✅ **Listas Dinâmicas:** Usuários e tours recentes
- ✅ **3 Formas de Acesso:**
  - 🏠 **Local:** Navegador do PC (`http://localhost:5000/mobile-admin`)
  - 📱 **Wi-Fi:** Celular na mesma rede (`http://[IP-DO-PC]:5000/mobile-admin`)
  - 🌐 **Internet:** Via Cloudflare Tunnel (de qualquer lugar)

## 🚀 Início Rápido

### 1. Criar Usuário Admin (Primeira Vez)

Se você ainda não tem um usuário admin, crie um:

```python
# No terminal Python
python

>>> from app import create_app, db
>>> from app.models.users import User
>>> from werkzeug.security import generate_password_hash
>>> 
>>> app = create_app()
>>> with app.app_context():
...     # Criar admin
...     admin = User(
...         username='admin',
...         email='admin@guiaalter.com',
...         password=generate_password_hash('senha123'),
...         is_admin=True
...     )
...     db.session.add(admin)
...     db.session.commit()
...     print("Admin criado com sucesso!")
```

**Credenciais padrão:**
- Usuário: `admin`
- Senha: `senha123`

⚠️ **IMPORTANTE:** Altere a senha após o primeiro login!

### 2. Iniciar Servidor

```bash
python run.py
```

### 3. Acessar Dashboard

**No navegador do PC:**
```
http://localhost:5000/mobile-admin/login
```

**No celular (mesma rede Wi-Fi):**
1. Descubra o IP do PC:
   - Windows: `ipconfig` (procure por IPv4)
   - Linux/Mac: `ifconfig` ou `ip addr`
2. No celular, acesse:
   ```
   http://[IP-DO-PC]:5000/mobile-admin/login
   ```
   Exemplo: `http://192.168.1.100:5000/mobile-admin/login`

## 🌐 Acesso Externo (Cloudflare Tunnel)

Para acessar de qualquer lugar via internet:

### Opção 1: Script Automático (Recomendado)

```bash
run-with-cloudflare.bat
```

O script irá:
1. Verificar/instalar dependências
2. Iniciar servidor Flask
3. Iniciar Cloudflare Tunnel
4. Mostrar URL pública

### Opção 2: Manual

1. **Instalar Cloudflared:**
   ```bash
   winget install --id Cloudflare.cloudflared
   ```

2. **Iniciar servidor:**
   ```bash
   python run.py
   ```

3. **Em outro terminal, iniciar tunnel:**
   ```bash
   cloudflared tunnel --url http://localhost:5000
   ```

4. **Copiar URL gerada** (ex: `https://abc-123.trycloudflare.com`)

5. **Acessar no celular:**
   ```
   https://abc-123.trycloudflare.com/mobile-admin/login
   ```

📖 **Guia Completo:** Veja [docs/cloudflare-tunnel-setup.md](docs/cloudflare-tunnel-setup.md)

## 📊 API Endpoints

Todos os endpoints requerem autenticação de admin.

### Autenticação

- `GET /mobile-admin/login` - Página de login
- `POST /mobile-admin/login` - Processar login (JSON)
- `GET /mobile-admin/logout` - Logout

### Dashboard

- `GET /mobile-admin/` - Dashboard principal
- `GET /mobile-admin/dashboard` - Alias para dashboard

### API (JSON)

- `GET /mobile-admin/api/stats` - Estatísticas gerais
  ```json
  {
    "users": {"total": 10, "admins": 2, "recent": 3},
    "tours": {"total": 25, "active": 20, "inactive": 5},
    "system": {"timestamp": "2024-11-23T12:00:00", "admin_name": "admin"}
  }
  ```

- `GET /mobile-admin/api/users?limit=10&offset=0` - Lista de usuários
- `GET /mobile-admin/api/tours?limit=10&offset=0` - Lista de tours
- `GET /mobile-admin/api/activity` - Atividade recente

## 🔒 Segurança

- ✅ **Autenticação obrigatória:** Todas as rotas protegidas
- ✅ **Apenas admins:** Verificação de `is_admin=True`
- ✅ **Rate limiting:** Proteção contra força bruta
- ✅ **HTTPS:** Cloudflare Tunnel fornece SSL automático
- ✅ **Senhas hash:** Werkzeug security (bcrypt)

### Boas Práticas

1. **Altere senhas padrão** imediatamente
2. **Use senhas fortes** (min. 12 caracteres)
3. **Não compartilhe** URLs do Cloudflare publicamente
4. **Monitore logs** regularmente
5. **Mantenha** servidor atualizado

## 🎨 Interface

### Login
- Design gradient moderno
- Inputs touch-friendly (grandes)
- Feedback visual de erros
- Loading states

### Dashboard
- Cards de estatísticas coloridos
- Listas scrolláveis
- Pull-to-refresh (arraste para baixo)
- Botão de atualização flutuante
- Responsivo (mobile e desktop)

## 🐛 Troubleshooting

### "Acesso negado. Apenas administradores."
**Solução:** Seu usuário não é admin. Verifique:
```python
python
>>> from app import create_app, db
>>> from app.models.users import User
>>> app = create_app()
>>> with app.app_context():
...     user = User.query.filter_by(username='SEU_USUARIO').first()
...     print(f"É admin? {user.is_admin}")
...     # Para tornar admin:
...     user.is_admin = True
...     db.session.commit()
```

### "Usuário ou senha incorretos"
**Soluções:**
1. Verifique se digitou corretamente
2. Senhas são case-sensitive
3. Tente resetar senha (veja seção "Criar Usuário Admin")

### Celular não acessa via Wi-Fi
**Soluções:**
1. Verifique se estão na mesma rede
2. Desative firewall temporariamente (teste)
3. Use IP correto (não use 127.0.0.1)
4. Servidor deve rodar em `0.0.0.0` (já configurado)

### Cloudflare Tunnel não conecta
**Soluções:**
1. Verifique se servidor Flask está rodando
2. Aguarde 1-2 minutos após iniciar
3. Tente reiniciar o tunnel
4. Veja logs para erros

## 📱 Testando

### Checklist Completo

**Acesso Local:**
- [ ] Servidor inicia sem erros
- [ ] Login abre em `http://localhost:5000/mobile-admin/login`
- [ ] Login funciona com credenciais admin
- [ ] Dashboard carrega estatísticas
- [ ] Listas de usuários aparecem
- [ ] Listas de tours aparecem
- [ ] Logout funciona

**Acesso Wi-Fi:**
- [ ] Celular e PC na mesma rede
- [ ] IP do PC descoberto
- [ ] Login abre no celular
- [ ] Interface responsiva (mobile-friendly)
- [ ] Touch funciona corretamente

**Acesso Externo:**
- [ ] Cloudflared instalado
- [ ] Tunnel inicia sem erros
- [ ] URL gerada copiada
- [ ] Acesso via dados móveis funciona
- [ ] HTTPS ativo (cadeado verde)

## 🔄 Atualizações Futuras

Possíveis melhorias:

- [ ] Edição de usuários via mobile
- [ ] Edição de tours via mobile
- [ ] Gráficos de estatísticas
- [ ] Notificações push
- [ ] Dark mode
- [ ] Suporte a múltiplos idiomas
- [ ] Exportar relatórios

## 📞 Suporte

Problemas ou dúvidas?
1. Veja [docs/cloudflare-tunnel-setup.md](docs/cloudflare-tunnel-setup.md)
2. Verifique logs do servidor
3. Abra uma issue no repositório

---

**Desenvolvido com ❤️ para Guia de Alter**
