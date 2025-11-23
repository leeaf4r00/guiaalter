# Cloudflare Tunnel - Acesso Externo ao Dashboard

Este guia mostra como configurar acesso externo (via internet) ao dashboard administrativo usando Cloudflare Tunnel.

## 📋 O que é Cloudflare Tunnel?

Cloudflare Tunnel permite expor seu servidor local para a internet de forma segura, sem precisar:
- Abrir portas no roteador
- Configurar port forwarding
- Ter IP público fixo
- Configurar DNS manualmente

**Vantagens:**
- ✅ HTTPS automático (certificado SSL grátis)
- ✅ Proteção DDoS do Cloudflare
- ✅ Acesso de qualquer lugar do mundo
- ✅ Fácil de configurar

---

## 🚀 Instalação do Cloudflared

### Windows

**Opção 1: Via winget (recomendado)**
```powershell
winget install --id Cloudflare.cloudflared
```

**Opção 2: Download manual**
1. Baixe: https://github.com/cloudflare/cloudflared/releases/latest
2. Procure por: `cloudflared-windows-amd64.exe`
3. Renomeie para `cloudflared.exe`
4. Mova para `C:\Windows\System32\` ou adicione ao PATH

### Linux
```bash
# Ubuntu/Debian
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Outras distros
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
```

### macOS
```bash
brew install cloudflare/cloudflare/cloudflared
```

**Verificar instalação:**
```bash
cloudflared --version
```

---

## ⚡ Quick Tunnel (Modo Rápido)

**Melhor para:** Testes, uso temporário, sem necessidade de login.

### Passo a Passo

1. **Inicie o servidor Flask:**
   ```bash
   python run.py
   ```
   O servidor estará rodando em `http://localhost:5000`

2. **Em outro terminal, inicie o tunnel:**
   ```bash
   cloudflared tunnel --url http://localhost:5000
   ```

3. **Copie a URL gerada:**
   ```
   2024-11-23 12:00:00 INF +--------------------------------------------------------------------------------------------+
   2024-11-23 12:00:00 INF |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
   2024-11-23 12:00:00 INF |  https://abc-123-xyz.trycloudflare.com                                                     |
   2024-11-23 12:00:00 INF +--------------------------------------------------------------------------------------------+
   ```

4. **Acesse no celular:**
   - Abra o navegador
   - Digite: `https://abc-123-xyz.trycloudflare.com/mobile-admin/login`
   - Faça login com suas credenciais de admin

**⚠️ Importante:**
- A URL muda toda vez que você reinicia o tunnel
- O tunnel fecha quando você fecha o terminal
- Ideal para testes rápidos

---

## 🔐 Named Tunnel (Modo Permanente)

**Melhor para:** Uso contínuo, URL fixa, produção.

### Pré-requisitos
- Conta Cloudflare (grátis)
- Domínio próprio (opcional, mas recomendado)

### Passo a Passo

#### 1. Login no Cloudflare
```bash
cloudflared tunnel login
```
- Abrirá o navegador
- Faça login na sua conta Cloudflare
- Autorize o acesso

#### 2. Criar o Tunnel
```bash
cloudflared tunnel create guiaalter
```

Saída esperada:
```
Tunnel credentials written to: C:\Users\SeuUsuario\.cloudflared\<UUID>.json
Created tunnel guiaalter with id <UUID>
```

#### 3. Configurar DNS (se tiver domínio)
```bash
cloudflared tunnel route dns guiaalter admin.seudominio.com
```

Substitua:
- `guiaalter` → nome do seu tunnel
- `admin.seudominio.com` → subdomínio desejado

#### 4. Criar arquivo de configuração

Crie o arquivo: `C:\Users\SeuUsuario\.cloudflared\config.yml`

```yaml
tunnel: guiaalter
credentials-file: C:\Users\SeuUsuario\.cloudflared\<UUID>.json

ingress:
  - hostname: admin.seudominio.com
    service: http://localhost:5000
  - service: http_status:404
```

#### 5. Executar o Tunnel
```bash
cloudflared tunnel run guiaalter
```

#### 6. Acessar
- Com domínio: `https://admin.seudominio.com/mobile-admin/login`
- Sem domínio: Use a URL do dashboard Cloudflare

---

## 🛠️ Scripts Auxiliares

### Windows: `run-with-cloudflare.bat`

Crie o arquivo na raiz do projeto:

```batch
@echo off
echo ========================================
echo   Guia de Alter - Servidor + Tunnel
echo ========================================
echo.

REM Inicia o servidor Flask em nova janela
echo [1/2] Iniciando servidor Flask...
start "Guia Alter Server" cmd /k "python run.py"

REM Aguarda 5 segundos para o servidor iniciar
echo [2/2] Aguardando servidor iniciar...
timeout /t 5 /nobreak >nul

REM Inicia o Cloudflare Tunnel
echo [2/2] Iniciando Cloudflare Tunnel...
echo.
echo IMPORTANTE: Copie a URL que aparecer abaixo!
echo.
cloudflared tunnel --url http://localhost:5000

pause
```

**Uso:**
```bash
run-with-cloudflare.bat
```

### Linux/Mac: `run-with-cloudflare.sh`

```bash
#!/bin/bash

echo "========================================"
echo "  Guia de Alter - Servidor + Tunnel"
echo "========================================"
echo ""

# Inicia servidor Flask em background
echo "[1/2] Iniciando servidor Flask..."
python3 run.py &
SERVER_PID=$!

# Aguarda 5 segundos
echo "[2/2] Aguardando servidor iniciar..."
sleep 5

# Inicia Cloudflare Tunnel
echo "[2/2] Iniciando Cloudflare Tunnel..."
echo ""
echo "IMPORTANTE: Copie a URL que aparecer abaixo!"
echo ""
cloudflared tunnel --url http://localhost:5000

# Cleanup ao sair
trap "kill $SERVER_PID" EXIT
```

**Tornar executável:**
```bash
chmod +x run-with-cloudflare.sh
./run-with-cloudflare.sh
```

---

## 🔒 Segurança

### Boas Práticas

1. **Senhas Fortes:**
   - Use senhas complexas para contas admin
   - Mínimo 12 caracteres
   - Combine letras, números e símbolos

2. **HTTPS Obrigatório:**
   - Cloudflare Tunnel já fornece HTTPS automaticamente
   - Nunca use HTTP em produção

3. **Rate Limiting:**
   - O código já implementa limite de 5 tentativas/minuto no login
   - Protege contra ataques de força bruta

4. **Monitoramento:**
   - Verifique logs regularmente
   - Cloudflare Dashboard mostra tráfego e tentativas de acesso

5. **Firewall:**
   - Mantenha firewall ativo no servidor
   - Apenas Cloudflare precisa acessar a porta 5000

### Cloudflare Access (Opcional - Camada Extra)

Para adicionar autenticação antes mesmo de chegar ao login:

```bash
# Instalar Cloudflare Access
cloudflared access login

# Proteger rota
cloudflared access protect https://admin.seudominio.com
```

---

## 🐛 Troubleshooting

### Erro: "cloudflared: command not found"
**Solução:** Cloudflared não está instalado ou não está no PATH.
- Reinstale seguindo as instruções acima
- Verifique com `cloudflared --version`

### Tunnel não conecta
**Soluções:**
1. Verifique se o servidor Flask está rodando (`http://localhost:5000`)
2. Verifique firewall (pode estar bloqueando)
3. Tente reiniciar o tunnel

### URL não abre no celular
**Soluções:**
1. Aguarde 1-2 minutos (DNS pode demorar)
2. Verifique se copiou a URL completa (com `https://`)
3. Tente em modo anônimo do navegador
4. Limpe cache do navegador

### "Bad Gateway" ou erro 502
**Solução:** Servidor Flask não está respondendo.
- Verifique se `python run.py` está rodando
- Veja logs do servidor para erros

### Tunnel fecha sozinho
**Solução:** Terminal foi fechado.
- Use `screen` ou `tmux` no Linux
- Use serviço do Windows para rodar em background

---

## 📱 Testando no Celular

### Checklist de Teste

1. **Acesso Local (Wi-Fi):**
   - [ ] Servidor rodando: `python run.py`
   - [ ] Descobrir IP: `ipconfig` (Windows) ou `ifconfig` (Linux)
   - [ ] Celular na mesma rede
   - [ ] Acessar: `http://[IP]:5000/mobile-admin/login`

2. **Acesso Externo (Internet):**
   - [ ] Tunnel rodando: `cloudflared tunnel --url http://localhost:5000`
   - [ ] Copiar URL gerada
   - [ ] Celular pode usar dados móveis
   - [ ] Acessar: `https://abc-123.trycloudflare.com/mobile-admin/login`

3. **Funcionalidades:**
   - [ ] Login funciona
   - [ ] Dashboard carrega
   - [ ] Estatísticas aparecem
   - [ ] Listas de usuários/tours funcionam
   - [ ] Logout funciona

---

## 💡 Dicas

1. **Salve a URL:** Adicione aos favoritos do celular para acesso rápido
2. **Atalho na Home:** No celular, use "Adicionar à tela inicial" para criar ícone
3. **Notificações:** Configure alertas no Cloudflare Dashboard
4. **Backup:** Mantenha backup do arquivo de credenciais (`~/.cloudflared/*.json`)

---

## 📚 Recursos Adicionais

- [Documentação Oficial Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [Cloudflare Dashboard](https://dash.cloudflare.com/)
- [GitHub Cloudflared](https://github.com/cloudflare/cloudflared)

---

## ❓ Suporte

Problemas? Entre em contato ou abra uma issue no repositório do projeto.
