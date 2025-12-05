"""
Guia de Alter - Desktop Application Launcher
Executa a aplicação Flask em uma janela nativa do Windows.
Gerencia servidor local e túnel Cloudflare de forma resiliente, segura e não bloqueante.
"""
import atexit
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
from dataclasses import dataclass
from typing import Optional

# Tenta carregar .env se existir
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv é opcional

from app import create_app


# ==================== CONFIGURAÇÃO ====================

@dataclass
class Config:
    """Configurações centralizadas da aplicação"""
    PORT: int = int(os.getenv('PORT', 5000))
    DEBUG: bool = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    HOST: str = os.getenv('HOST', '0.0.0.0')
    
    WINDOW_WIDTH: int = int(os.getenv('WINDOW_WIDTH', 1280))
    WINDOW_HEIGHT: int = int(os.getenv('WINDOW_HEIGHT', 800))
    APP_TITLE: str = os.getenv('APP_TITLE', '🌴 Guia de Alter - Central de Comando')
    
    ENABLE_CLOUDFLARE: bool = os.getenv('ENABLE_CLOUDFLARE', 'True').lower() == 'true'
    CLOUDFLARED_URL: str = os.getenv(
        'CLOUDFLARED_URL',
        'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe'
    )
    
    DATABASE_PATH: str = os.getenv('DATABASE_PATH', 'instance/database.db')


config = Config()


# ==================== LOGGING ====================

log_file = Path("desktop_app.log")
logging.basicConfig(
    level=logging.DEBUG if config.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, mode='w', encoding='utf-8')
    ]
)
logger = logging.getLogger("Launcher")


# ==================== CLASSES DE GERENCIAMENTO ====================

class CloudflareTunnel:
    """Gerencia o ciclo de vida do túnel Cloudflare"""
    
    def __init__(self, port: int):
        self.port = port
        self.process: Optional[subprocess.Popen] = None
        self.public_url: Optional[str] = None
        self.stop_event = threading.Event()
        self.thread: Optional[threading.Thread] = None

    def _get_binary_path(self) -> Optional[str]:
        """Retorna caminho do executável, baixando se necessário"""
        bin_dir = Path("bin")
        bin_dir.mkdir(exist_ok=True)
        local_bin = bin_dir / "cloudflared.exe"
        
        if local_bin.exists():
            return str(local_bin)
            
        system_bin = shutil.which("cloudflared")
        if system_bin:
            return system_bin
            
        logger.info("⬇️ Cloudflared não encontrado. Baixando...")
        try:
            urllib.request.urlretrieve(config.CLOUDFLARED_URL, str(local_bin))
            logger.info("✅ Download concluído!")
            return str(local_bin)
        except (urllib.error.URLError, OSError) as e:
            logger.error(f"❌ Erro ao baixar cloudflared: {e}")
            return None

    def start(self) -> None:
        """Inicia o túnel em uma thread separada (não bloqueante)"""
        if not config.ENABLE_CLOUDFLARE:
            logger.info("☁️ Cloudflare Tunnel desativado nas configurações.")
            return
            
        self.thread = threading.Thread(target=self._run_tunnel, daemon=True, name="CloudflareTunnel")
        self.thread.start()

    def _run_tunnel(self) -> None:
        bin_path = self._get_binary_path()
        if not bin_path:
            return

        cmd = [bin_path, "tunnel", "--url", f"http://localhost:{self.port}"]
        
        # Flags de segurança para esconder janela no Windows
        creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        
        logger.info("☁️ Iniciando Cloudflare Tunnel...")
        
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
                
                line = self.process.stderr.readline()
                if not line:
                    continue
                    
                logger.debug(f"[CF] {line.strip()}")
                
                if not self.public_url:
                    match = re.search(r'https://[-a-zA-Z0-9]+\.trycloudflare\.com', line)
                    if match:
                        self.public_url = match.group(0)
                        logger.info(f"✅ URL PÚBLICA: {self.public_url}")
                        os.environ['CLOUDFLARE_URL'] = self.public_url

        except FileNotFoundError:
            logger.error("❌ Executável cloudflared não encontrado.")
        except PermissionError:
            logger.error("❌ Sem permissão para executar cloudflared.")
        except OSError as e:
            logger.error(f"❌ Erro de sistema ao iniciar túnel: {e}")

    def stop(self) -> None:
        """Para o túnel de forma segura"""
        self.stop_event.set()
        if self.process:
            logger.info("🛑 Parando Cloudflare Tunnel...")
            try:
                self.process.terminate()
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                logger.warning("⚠️ Forçando encerramento do Cloudflare...")
                self.process.kill()
            except OSError as e:
                logger.error(f"Erro ao parar processo: {e}")
            finally:
                self.process = None


class FlaskServer:
    """Gerencia o servidor Flask"""
    
    def __init__(self, port: int, host: str = '0.0.0.0'):
        self.port = port
        self.host = host
        self.app = None
        self.thread: Optional[threading.Thread] = None

    def get_local_ip(self) -> str:
        """Obtém IP local robusto"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except OSError:
            return "127.0.0.1"

    def start(self) -> bool:
        """Inicia o servidor em thread separada"""
        self.thread = threading.Thread(target=self._run_server, daemon=True, name="FlaskServer")
        self.thread.start()
        return self._wait_for_ready()

    def _run_server(self) -> None:
        logger.info("🚀 Iniciando servidor Flask...")
        os.environ['LOCAL_IP'] = self.get_local_ip()
        
        self.app = create_app()
        self.app.run(
            debug=config.DEBUG,
            use_reloader=False,  # Crítico para rodar em thread
            host=self.host,
            port=self.port,
            threaded=True
        )

    def _wait_for_ready(self, timeout: int = 30) -> bool:
        """Aguarda servidor estar respondendo"""
        start = time.time()
        while time.time() - start < timeout:
            try:
                urllib.request.urlopen(f'http://127.0.0.1:{self.port}/', timeout=2)
                logger.info("✅ Servidor Flask pronto!")
                return True
            except (urllib.error.URLError, OSError):
                time.sleep(0.5)
        logger.error("❌ Timeout: servidor Flask não iniciou")
        return False


class AppManager:
    """Gerenciador central do ciclo de vida da aplicação"""
    
    def __init__(self):
        self.server: Optional[FlaskServer] = None
        self.tunnel: Optional[CloudflareTunnel] = None
        self.window = None
        
        # Registra cleanup automático
        atexit.register(self.shutdown)

    def check_first_run(self) -> bool:
        """Verifica se é necessário setup inicial"""
        try:
            db_path = Path(config.DATABASE_PATH)
            if not db_path.exists():
                return True
            
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
                if not cursor.fetchone():
                    return True
                    
                cursor.execute("SELECT count(*) FROM users")
                return cursor.fetchone()[0] == 0
                
        except sqlite3.Error as e:
            logger.error(f"Erro ao verificar DB: {e}")
            return True

    def start(self) -> bool:
        """Inicializa todos os componentes"""
        logger.info("=== INICIANDO GUIA DE ALTER DESKTOP ===")
        
        # 1. Servidor Flask
        self.server = FlaskServer(config.PORT, config.HOST)
        if not self.server.start():
            logger.critical("Falha ao iniciar servidor. Abortando.")
            return False
        
        # 2. Cloudflare Tunnel (background)
        self.tunnel = CloudflareTunnel(config.PORT)
        self.tunnel.start()
        
        return True

    def get_start_url(self) -> str:
        """Retorna URL inicial baseado no estado do app"""
        base = f'http://127.0.0.1:{config.PORT}'
        if self.check_first_run():
            return f'{base}/mobile-admin/setup'
        return f'{base}/mobile-admin/login'

    def create_window(self) -> None:
        """Cria e exibe a janela principal"""
        start_url = self.get_start_url()
        logger.info(f"🪟 Abrindo janela em: {start_url}")
        
        self.window = webview.create_window(
            title=config.APP_TITLE,
            url=start_url,
            width=config.WINDOW_WIDTH,
            height=config.WINDOW_HEIGHT,
            resizable=True,
            confirm_close=True,
            background_color='#1a1a1a'
        )
        
        # Bloqueia até fechar a janela
        webview.start(debug=config.DEBUG)

    def shutdown(self) -> None:
        """Encerra todos os componentes de forma limpa"""
        logger.info("👋 Encerrando aplicação...")
        
        if self.tunnel:
            self.tunnel.stop()
            self.tunnel = None
            
        logger.info("✅ Shutdown completo.")

    def run(self) -> None:
        """Ponto de entrada principal"""
        if not self.start():
            sys.exit(1)
            
        try:
            self.create_window()
        finally:
            self.shutdown()


# ==================== MAIN ====================

def main():
    app_manager = AppManager()
    app_manager.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("⚠️ Interrupção pelo usuário (Ctrl+C)")
    except SystemExit:
        pass  # Exit normal

