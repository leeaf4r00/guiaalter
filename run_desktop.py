"""
Guia de Alter - Desktop Application Launcher
Executa a aplicação Flask em uma janela nativa do Windows.
Gerencia servidor local e túnel Cloudflare de forma resiliente, segura e não bloqueante.
"""
import logging
import webview
import threading
import time
import os
import sys
import sqlite3
import socket
import subprocess
import re
import shutil
import urllib.request
from pathlib import Path
from app import create_app

# ==================== CONFIGURAÇÃO DE LOGGING ====================
# Cria logger padronizado que escreve no console e em arquivo
log_file = Path("desktop_app.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, mode='w', encoding='utf-8')
    ]
)
logger = logging.getLogger("Launcher")

# ==================== CONFIGURAÇÕES GERAIS ====================
PORT = 5000
DEBUG = False
APP_TITLE = "🌴 Guia de Alter - Central de Comando"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
CLOUDFLARED_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"

# ==================== CLASSES DE GERENCIAMENTO ====================

class CloudflareTunnel:
    """Gerencia o ciclo de vida do túnel Cloudflare"""
    def __init__(self, port):
        self.port = port
        self.process = None
        self.public_url = None
        self.stop_event = threading.Event()
        self.thread = None

    def _get_binary_path(self):
        """Retorna caminho do executável, baixando se necessário"""
        bin_dir = Path("bin")
        bin_dir.mkdir(exist_ok=True)
        local_bin = bin_dir / "cloudflared.exe"
        
        if local_bin.exists():
            return str(local_bin)
            
        if shutil.which("cloudflared"):
            return shutil.which("cloudflared")
            
        logger.info("⬇️ Cloudflared não encontrado. Baixando...")
        try:
            urllib.request.urlretrieve(CLOUDFLARED_URL, str(local_bin))
            logger.info("✅ Download concluído!")
            return str(local_bin)
        except Exception as e:
            logger.error(f"❌ Erro ao baixar cloudflared: {e}")
            return None

    def start(self):
        """Inicia o túnel em uma thread separada (não bloqueante)"""
        self.thread = threading.Thread(target=self._run_tunnel, daemon=True)
        self.thread.start()

    def _run_tunnel(self):
        bin_path = self._get_binary_path()
        if not bin_path:
            return

        cmd = [bin_path, "tunnel", "--url", f"http://localhost:{self.port}"]
        
        # Flags de segurança para esconder janela no Windows
        creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        
        logger.info(f"☁️ Iniciando Cloudflare Tunnel...")
        
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                encoding='utf-8',
                creationflags=creationflags
            )
            
            while not self.stop_event.is_set():
                if self.process.poll() is not None:
                    logger.warning(f"❌ Cloudflare encerrou inesperadamente (Código: {self.process.returncode})")
                    break
                
                # Lê output linha a linha sem bloquear
                line = self.process.stderr.readline()
                if not line:
                    continue
                    
                # LOGAR TUDO para debug no arquivo desktop_app.log
                logger.info(f"[CF] {line.strip()}")
                
                if not self.public_url:
                    # Regex ajustada para pegar a URL limpa
                    match = re.search(r'https://[-a-zA-Z0-9]+\.trycloudflare\.com', line)
                    if match:
                        self.public_url = match.group(0)
                        logger.info(f"✅ URL PÚBLICA ENCONTRADA: {self.public_url}")
                        os.environ['CLOUDFLARE_URL'] = self.public_url

        except Exception as e:
            logger.error(f"❌ Erro crítico no túnel: {e}")
        finally:
            self.stop()

    def stop(self):
        """Para o túnel de forma segura e limpa recursos"""
        self.stop_event.set()
        if self.process:
            logger.info("🛑 Parando Cloudflare Tunnel...")
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                logger.warning("⚠️ Forçando encerramento do Cloudflare...")
                self.process.kill()
            except Exception as e:
                logger.error(f"Erro ao parar processo: {e}")
            self.process = None

class FlaskServer:
    """Gerencia o servidor Flask"""
    def __init__(self, port):
        self.port = port
        self.app = None
        self.thread = None

    def get_local_ip(self):
        """Obtém IP local robusto (ignora VPNs se possível)"""
        try:
            # Tenta conectar a um DNS externo para ver qual interface é usada
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            logger.warning(f"Não foi possível obter IP local: {e}")
            return "127.0.0.1"

    def start(self):
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()
        return self._wait_for_ready()

    def _run_server(self):
        logger.info("🚀 Iniciando servidor Flask...")
        os.environ['LOCAL_IP'] = self.get_local_ip()
        self.app = create_app()
        # use_reloader=False é CRÍTICO para rodar em thread e pywebview
        self.app.run(debug=DEBUG, use_reloader=False, host='0.0.0.0', port=self.port, threaded=True)

    def _wait_for_ready(self, timeout=30):
        """Aguarda servidor estar respondendo"""
        start = time.time()
        while time.time() - start < timeout:
            try:
                urllib.request.urlopen(f'http://127.0.0.1:{self.port}/')
                logger.info("✅ Servidor Flask pronto e respondendo!")
                return True
            except Exception:
                time.sleep(0.5)
        logger.error("❌ Timeout aguardando servidor Flask iniciar")
        return False

# ==================== FUNÇÕES AUXILIARES ====================

def check_first_run():
    """Verifica se é necessário setup inicial (banco vazio)"""
    try:
        db_path = os.path.join('instance', 'database.db')
        if not os.path.exists(db_path):
            return True
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            conn.close()
            return True
            
        cursor.execute("SELECT count(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        return count == 0
    except Exception as e:
        logger.error(f"Erro verificação DB: {e}")
        return True

# ==================== MAIN ====================

tunnel = None

def on_closing():
    """Callback de fechamento da janela"""
    logger.info("👋 Encerrando aplicação...")
    if tunnel:
        tunnel.stop()
    sys.exit(0)

def main():
    global tunnel
    
    logger.info("=== INICIANDO GUIA DE ALTER DESKTOP ===")
    
    # 1. Inicia Servidor
    server = FlaskServer(PORT)
    if not server.start():
        logger.critical("Falha ao iniciar servidor. Abortando.")
        return
    
    # 2. Inicia Tunnel (Non-blocking - roda em background)
    tunnel = CloudflareTunnel(PORT)
    tunnel.start()
    
    # 3. Define URL inicial
    start_url = f'http://127.0.0.1:{PORT}/mobile-admin/setup' if check_first_run() else f'http://127.0.0.1:{PORT}/mobile-admin/login'
    
    logger.info(f"🪟 Abrindo janela em: {start_url}")
    
    # 4. Cria Janela
    window = webview.create_window(
        title=APP_TITLE,
        url=start_url,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        resizable=True,
        confirm_close=True,
        background_color='#1a1a1a'
    )
    
    # Inicia o loop da interface (bloqueia aqui até fechar a janela)
    webview.start(debug=DEBUG)
    
    # === LIMPEZA APÓS FECHAR A JANELA ===
    logger.info("👋 Janela fechada. Encerrando aplicação...")
    if tunnel:
        tunnel.stop()
    sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.critical(f"❌ Erro fatal na main: {e}", exc_info=True)
        on_closing()
