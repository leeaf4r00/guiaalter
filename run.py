"""
Guia de Alter - Entry Point
Executa a aplicação Flask em modo desenvolvimento.
"""
import os
import sys

# Tenta carregar .env se existir
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv é opcional

from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Banner formatado
    debug_str = "Ativo" if debug else "Desativado"
    print(f"""
╔═══════════════════════════════════════════╗
║    🌴 GUIA DE ALTER - SERVER RUNNING      ║
╠═══════════════════════════════════════════╣
║  URL:   http://localhost:{port:<5}            ║
║  Debug: {debug_str:<10}                    ║
╚═══════════════════════════════════════════╝
    """)
    
    try:
        app.run(
            debug=debug,
            use_reloader=debug,  # Reloader só em debug
            host=host,
            port=port
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor encerrado pelo usuário.")
        sys.exit(0)

