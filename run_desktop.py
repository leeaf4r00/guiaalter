"""
Guia de Alter - Desktop Application Launcher
Executa a aplicação Flask em uma janela nativa do Windows
"""
import webview
import threading
import time
import os
import sys
from app import create_app

# Configurações
PORT = 5000
DEBUG = False
APP_TITLE = "🌴 Guia de Alter - Dashboard Administrativo"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

# Variável global para o app Flask
flask_app = None
server_thread = None


def start_flask_server():
    """Inicia o servidor Flask em uma thread separada"""
    global flask_app
    
    print("🚀 Iniciando servidor Flask...")
    flask_app = create_app()
    
    # Roda o Flask sem abrir navegador
    flask_app.run(
        debug=DEBUG,
        use_reloader=False,  # Importante: desabilita reloader para evitar problemas
        host='127.0.0.1',
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
    # O Flask será encerrado automaticamente quando o processo terminar
    sys.exit(0)


def main():
    """Função principal que inicia a aplicação desktop"""
    
    print(f"""
╔═══════════════════════════════════════════════╗
║   🌴 GUIA DE ALTER - DESKTOP APPLICATION      ║
╠═══════════════════════════════════════════════╣
║  Modo: Desktop Window (Janela Nativa)         ║
║  Porta: {PORT}                                ║
║  Resolução: {WINDOW_WIDTH}x{WINDOW_HEIGHT}    ║
╚═══════════════════════════════════════════════╝
    """)
    
    # Inicia o servidor Flask em uma thread separada
    server_thread = threading.Thread(target=start_flask_server, daemon=True)
    server_thread.start()
    
    # Aguarda o servidor estar pronto
    if not wait_for_server():
        print("❌ Não foi possível iniciar o servidor. Verifique se a porta está disponível.")
        return
    
    # Cria a janela do aplicativo
    print("🪟 Abrindo janela do aplicativo...")
    
    # URL inicial - pode ser a tela de login ou dashboard
    initial_url = f'http://127.0.0.1:{PORT}/mobile-admin/login'
    
    # Cria a janela com pywebview
    window = webview.create_window(
        title=APP_TITLE,
        url=initial_url,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        resizable=True,
        fullscreen=False,
        min_size=(800, 600),
        confirm_close=True,  # Pergunta antes de fechar
        background_color='#1a1a1a'
    )
    
    # Inicia a aplicação (bloqueia até a janela ser fechada)
    webview.start(on_closing, debug=DEBUG)
    
    print("✅ Aplicação encerrada com sucesso!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Aplicação interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
