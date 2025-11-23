# 🪟 Guia de Alter - Aplicação Desktop

## 📋 Visão Geral

Este guia explica como executar o **Guia de Alter** como uma **aplicação desktop nativa do Windows**, sem precisar abrir o navegador.

## ✨ Características

- ✅ **Janela Nativa do Windows** - Aparência de aplicativo desktop real
- ✅ **Sem Navegador** - Não abre Chrome/Edge/Firefox
- ✅ **Interface Completa** - Todas as funcionalidades do dashboard
- ✅ **Gerenciamento de Usuários** - Controle total de usuários e parceiros
- ✅ **Configurações do Sistema** - Backup, logs, bloqueio de IP
- ✅ **Responsivo** - Redimensionável e adaptável

---

## 🚀 Como Iniciar

### Método 1: Usando o Script Automático (Recomendado)

1. **Dê duplo clique** no arquivo:
   ```
   run-desktop.bat
   ```

2. O script irá automaticamente:
   - ✅ Criar ambiente virtual (se não existir)
   - ✅ Instalar todas as dependências
   - ✅ Iniciar o servidor Flask
   - ✅ Abrir a janela do aplicativo

3. **Pronto!** A janela do dashboard irá abrir automaticamente.

---

### Método 2: Manual (Para Desenvolvedores)

#### Passo 1: Instalar Dependências

```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Instalar dependências (incluindo pywebview)
pip install -r requirements.txt
```

#### Passo 2: Executar Aplicação Desktop

```bash
python run_desktop.py
```

---

## 🎯 Primeira Execução

### 1. Login Inicial

Ao abrir a aplicação, você verá a tela de login:

**Credenciais Padrão:**
- **Usuário:** `admin`
- **Senha:** `admin123`

⚠️ **IMPORTANTE:** Altere a senha padrão imediatamente após o primeiro login!

### 2. Explorar o Dashboard

Após o login, você terá acesso a:

- 📊 **Dashboard Principal** - Estatísticas e visão geral
- 👥 **Gestão de Usuários** - Criar, editar, bloquear usuários
- 🤝 **Aprovação de Parceiros** - Aprovar/rejeitar cadastros
- 🔒 **Segurança** - Bloqueio de IPs, logs de auditoria
- ⚙️ **Sistema** - Backup, restauração, modo manutenção

---

## ⚙️ Configurações Avançadas

### Alterar Porta do Servidor

Edite o arquivo `run_desktop.py`:

```python
PORT = 5000  # Altere para a porta desejada
```

### Alterar Tamanho da Janela

Edite o arquivo `run_desktop.py`:

```python
WINDOW_WIDTH = 1280   # Largura em pixels
WINDOW_HEIGHT = 800   # Altura em pixels
```

### Modo Tela Cheia

Edite o arquivo `run_desktop.py`:

```python
fullscreen=True,  # Mude para True
```

### Ativar Modo Debug

Edite o arquivo `run_desktop.py`:

```python
DEBUG = True  # Para ver logs detalhados
```

---

## 🔧 Solução de Problemas

### Problema: "Porta já em uso"

**Solução:**
1. Feche qualquer instância do `run.py` que esteja rodando
2. Ou altere a porta no `run_desktop.py`

### Problema: "Módulo pywebview não encontrado"

**Solução:**
```bash
pip install pywebview
```

### Problema: Janela não abre

**Solução:**
1. Verifique se o Python está instalado corretamente
2. Execute manualmente:
   ```bash
   python run_desktop.py
   ```
3. Veja os logs de erro no terminal

### Problema: Tela branca na janela

**Solução:**
1. Aguarde alguns segundos (servidor Flask está iniciando)
2. Se persistir, verifique se a porta 5000 está disponível
3. Veja os logs no terminal

---

## 📱 Diferenças entre Modo Web e Desktop

| Característica | Modo Web (`run.py`) | Modo Desktop (`run_desktop.py`) |
|----------------|---------------------|----------------------------------|
| Interface | Navegador (Chrome, Edge, etc) | Janela nativa do Windows |
| Acesso Remoto | ✅ Sim (via IP ou Cloudflare) | ❌ Apenas local |
| Aparência | Aba do navegador | Aplicativo standalone |
| Atalhos | Atalhos do navegador | Atalhos do aplicativo |
| Barra de Endereço | ✅ Visível | ❌ Oculta |
| Melhor Para | Acesso remoto, múltiplos dispositivos | Uso local, aparência profissional |

---

## 🎨 Personalização

### Alterar Título da Janela

Edite `run_desktop.py`:

```python
APP_TITLE = "Seu Título Aqui"
```

### Alterar Cor de Fundo

Edite `run_desktop.py`:

```python
background_color='#1a1a1a'  # Código hexadecimal da cor
```

### Desabilitar Confirmação ao Fechar

Edite `run_desktop.py`:

```python
confirm_close=False,  # Não pergunta ao fechar
```

---

## 🔐 Segurança

### Modo Desktop vs Modo Web

- ✅ **Desktop:** Mais seguro para uso local (não expõe porta na rede)
- ✅ **Web:** Necessário para acesso remoto (use HTTPS via Cloudflare)

### Recomendações

1. **Use Desktop** para administração local
2. **Use Web** quando precisar acessar remotamente
3. **Nunca** exponha o servidor Flask diretamente na internet sem HTTPS
4. **Sempre** altere a senha padrão do admin

---

## 📊 Funcionalidades Disponíveis

### ✅ Gestão de Usuários

- Criar novos usuários (Admin, Parceiro, Usuário)
- Editar informações de usuários
- Bloquear/Desbloquear contas
- Ver histórico de login
- Filtrar por role e status

### ✅ Aprovação de Parceiros

- Ver cadastros pendentes
- Aprovar parceiros
- Rejeitar com motivo
- Notificar por email (se configurado)

### ✅ Segurança

- Bloquear IPs manualmente
- Ver logs de auditoria
- Rastrear todas as ações
- Exportar logs

### ✅ Sistema

- Criar backups do banco de dados
- Restaurar backups
- Ativar modo manutenção
- Ver estatísticas do sistema

---

## 🆚 Quando Usar Cada Modo

### Use o Modo Desktop (`run-desktop.bat`) quando:

- ✅ Estiver trabalhando no computador local
- ✅ Quiser uma aparência mais profissional
- ✅ Não precisar de acesso remoto
- ✅ Quiser economizar recursos (sem navegador)
- ✅ Preferir um aplicativo dedicado

### Use o Modo Web (`run.py`) quando:

- ✅ Precisar acessar de outro dispositivo
- ✅ Quiser usar no celular
- ✅ Precisar de acesso via internet (Cloudflare)
- ✅ Múltiplos administradores simultâneos
- ✅ Desenvolvimento e testes

---

## 🚀 Próximos Passos

1. **Primeiro Login**
   - Use `admin` / `admin123`
   - Altere a senha imediatamente

2. **Configurar Sistema**
   - Criar usuários administrativos adicionais
   - Configurar backup automático
   - Revisar configurações de segurança

3. **Gerenciar Parceiros**
   - Compartilhar link de cadastro: `http://localhost:5000/mobile-admin/register`
   - Aprovar cadastros pendentes
   - Configurar permissões

4. **Backup Regular**
   - Use a função de backup no dashboard
   - Ou copie manualmente `instance/database.db`

---

## 📞 Suporte

### Documentação Adicional

- **Sistema Completo:** `SISTEMA_COMPLETO.md`
- **Admin Mobile:** `README_MOBILE_ADMIN.md`
- **Portal Público:** `PORTAL_PUBLICO.md`
- **Desenvolvimento:** `DEVELOPMENT_GUIDE.md`

### Arquivos Importantes

- `run_desktop.py` - Launcher desktop
- `run.py` - Launcher web
- `run-desktop.bat` - Script automático desktop
- `run-with-cloudflare.bat` - Script com túnel Cloudflare

---

## ✅ Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] Ambiente virtual criado (`.venv`)
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Banco de dados migrado (`python migrate_db_simple.py`)
- [ ] Primeiro login realizado
- [ ] Senha padrão alterada
- [ ] Backup inicial criado

---

## 🎊 Conclusão

Agora você pode usar o **Guia de Alter** como uma aplicação desktop profissional do Windows!

**Vantagens:**
- ✅ Aparência nativa e profissional
- ✅ Sem necessidade de navegador
- ✅ Mais rápido e leve
- ✅ Interface dedicada
- ✅ Todas as funcionalidades disponíveis

**Para iniciar:**
```
Duplo clique em: run-desktop.bat
```

**Aproveite! 🌴**
