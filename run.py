"""
Guia de Alter - Entry Point
Executa a aplicação Flask
"""
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"""
╔═══════════════════════════════════════╗
║   🌴 GUIA DE ALTER - SERVER RUNNING   ║
╠═══════════════════════════════════════╣
║  URL: http://localhost:{port}         ║
║  Debug: {debug}                        ║
╚═══════════════════════════════════════╝
    """)
    
    app.run(
        debug=debug,
        use_reloader=True,
        host='0.0.0.0',
        port=port
    )
