"""
Guia de Alter - Desktop Application Launcher
Executa a aplicação Flask em uma janela nativa do Windows
Gerencia servidor local e túnel Cloudflare
"""
import webview
import threading
import time
import os
import sys
import sqlite3
import socket
import subprocess
import re
from app import create_app

# Configurações
PORT = 5000
DEBUG = False
APP_TITLE = "🌴 Guia de Alter - Central de Comando"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

# Variáveis globais
flask_app = None
server_thread = None
cloudflare_process = None
public_url = None

def get_local_ip():
    """Obtém o IP local da máquina na rede Wi-Fi"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def start_cloudflare():
    """Inicia o túnel Cloudflare e captura a URL pública"""
    global cloudflare_process, public_url
    
    print("☁️ Iniciando Cloudflare Tunnel...")
    try:
        # Verifica se cloudflared existe
        cmd = "cloudflared tunnel --url http://localhost:5000"
        
        # Inicia processo
        cloudflare_process = subprocess.Popen(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            encoding='utf-8'
        )
        
        # Thread para ler a saída e encontrar a URL
        def monitor_output():
            global public_url
            while True:
                if cloudflare_process.poll() is not None:
                    break
                
                # Lê linha por linha do stderr (onde o cloudflared joga os logs)
                line = cloudflare_process.stderr.readline()
                if line:
                    # Procura por URL trycloudflare.com
                    match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                    if match:
                        public_url = match.group(0)
                        print(f"✅ URL Pública encontrada: {public_url}")
                        # Define variável de ambiente para o Flask pegar
                        os.environ['CLOUDFLARE_URL'] = public_url
                        break
        
        t = threading.Thread(target=monitor_output, daemon=True)
        t.start()
        
    except Exception as e:
        print(f"❌ Erro ao iniciar Cloudflare: {e}")

def check_first_run():
    """Verifica se é a primeira execução (sem usuários no banco)"""
    try:
        db_path = os.path.join('instance', 'database.db')
        if not os.path.exists(db_path):
            return True
            
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verifica se tabela users existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            conn.close()
            return True
            
        # Verifica se tem usuários
        cursor.execute("SELECT count(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        
        return count == 0
    except Exception as e:
        print(f"Erro ao verificar primeira execução: {e}")
        return True

def start_flask_server():
    """Inicia o servidor Flask em uma thread separada"""
    global flask_app
    
    print("🚀 Iniciando servidor Flask...")
    
    # Define IP local no ambiente
    os.environ['LOCAL_IP'] = get_local_ip()
    
    flask_app = create_app()
    
    # Roda o Flask
    flask_app.run(
        debug=DEBUG,
        use_reloader=False,
        host='0.0.0.0', # Importante para acesso externo
        port=PORT,
        threaded=True
    )

def wait_for_server():
    """Aguarda o servidor Flask estar pronto"""
    import urllib.request
    import urllib.error
    
    max_attempts = 30
    for i in range(max_attempts):
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{PORT}/')
            print("✅ Servidor Flask pronto!")
            return True
        except urllib.error.URLError:
            if i == 0:
                print("⏳ Aguardando servidor Flask iniciar...")
            time.sleep(0.5)
    
    print("❌ Erro: Servidor Flask não iniciou a tempo")
    return False

def on_closing():
    """Callback quando a janela é fechada"""
    print("👋 Encerrando aplicação...")
    
    # Mata o processo do Cloudflare se existir
    if cloudflare_process:
        print("☁️ Encerrando Cloudflare...")
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(cloudflare_process.pid)])
        
    sys.exit(0)

def main():
    """Função principal que inicia a aplicação desktop"""
    
    local_ip = get_local_ip()
    
    print(f"""
╔═══════════════════════════════════════════════╗
║   🌴 GUIA DE ALTER - CENTRAL DE COMANDO       ║
╠═══════════════════════════════════════════════╣
║  IP Local: {local_ip}:{PORT}                  ║
║  Cloudflare: Iniciando...                     ║
╚═══════════════════════════════════════════════╝
    """)
    
    # 1. Inicia Cloudflare
    start_cloudflare()
    
    # 2. Inicia Flask
    server_thread = threading.Thread(target=start_flask_server, daemon=True)
    server_thread.start()
    
    if not wait_for_server():
        print("❌ Não foi possível iniciar o servidor.")
        return
    
    print("🪟 Abrindo janela do aplicativo...")
    
    # Decide qual URL abrir
    if check_first_run():
        initial_url = f'http://127.0.0.1:{PORT}/mobile-admin/setup'
    else:
        initial_url = f'http://127.0.0.1:{PORT}/mobile-admin/login'
    
    window = webview.create_window(
        title=APP_TITLE,
        url=initial_url,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        resizable=True,
        fullscreen=False,
        min_size=(800, 600),
        confirm_close=True,
        background_color='#1a1a1a'
    )
    
    webview.start(on_closing, debug=DEBUG)
    print("✅ Aplicação encerrada com sucesso!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        on_closing()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        on_closing()
