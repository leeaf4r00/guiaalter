"""
Flask Dashboard API - Production Ready
Cloudflare Tunnel Architecture

Endpoints:
- / : Dashboard principal
- /api/vendas : Vendas do dia
- /api/caixa : Status do caixa
- /api/estoque : Produtos com estoque baixo
"""

from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
import secrets
import logging
from pathlib import Path
from datetime import datetime, timedelta
import os
import sys

# Configuração do Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from src.utils.crypto import verificar_senha

# Configurações
DB_PATH = BASE_DIR / "data" / "panificadora.db"
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))

# Aplicação Flask
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=12)

# SQLAlchemy Configuration
# Usando QueuePool para gerenciar conexões de forma eficiente
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30
)
db_session = scoped_session(sessionmaker(bind=engine))

# Logging estruturado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / 'logs' / 'dashboard_access.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Rate Limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# ==================== SECURITY ====================

@app.after_request
def set_security_headers(response):
    """Adiciona headers de segurança"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    # Removido 'unsafe-inline' de style-src
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self'; script-src 'self' 'unsafe-inline'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def login_required(f):
    """Decorator para rotas que requerem autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def format_currency(value):
    """Formata valor monetário"""
    if value is None:
        value = 0
    return f"R$ {value:.2f}".replace('.', ',')

# ==================== AUTHENTICATION ====================

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    """Login com rate limiting"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validação de entrada
        if not username or not password:
            logger.warning(f"Tentativa de login inválida: campos vazios")
            return render_template('login.html', error="Preencha todos os campos"), 400
        
        try:
            # Busca usuário usando SQLAlchemy - usando login e senha_hash conforme schema
            result = db_session.execute(
                text("SELECT id, login, senha_hash FROM usuarios WHERE login = :login LIMIT 1"),
                {"login": username}
            ).fetchone()
            
            # Em SQLAlchemy Core/Raw result, acesso pode ser por índice ou mapeamento dependendo da versão/driver
            # Convertendo para dict para segurança
            user = result._mapping if result else None
            
            if user and verificar_senha(password, user['senha_hash']):
                # Login bem-sucedido
                session.permanent = True
                session['user_id'] = user['id']
                session['username'] = user['login']
                logger.info(f"Login bem-sucedido: {username} (IP: {request.remote_addr})")
                return redirect(url_for('dashboard'))
            else:
                # Falha no login
                logger.warning(f"Falha no login: {username} (IP: {request.remote_addr})")
                return render_template('login.html', error="Usuário ou senha inválidos"), 401
                
        except Exception as e:
            logger.error(f"Erro no login: {e}", exc_info=True)
            return render_template('login.html', error="Erro interno"), 500
    
    # GET - mostra formulário de login
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout"""
    username = session.get('username', 'Unknown')
    session.clear()
    logger.info(f"Logout: {username}")
    return redirect(url_for('login'))

# ==================== DASHBOARD ====================

@app.route('/')
@login_required
def dashboard():
    """Dashboard principal"""
    try:
        # Vendas de hoje - Nota: vendas usa data_hora e total, não data_venda e valor_total
        hoje = datetime.now().strftime('%Y-%m-%d')
        vendas_hoje = db_session.execute(
            text("""
            SELECT COUNT(*) as total_vendas, COALESCE(SUM(total), 0) as total_valor
            FROM vendas
            WHERE DATE(data_hora) = :hoje
            """),
            {"hoje": hoje}
        ).fetchone()._mapping
        
        # Status do caixa - Nota: tabela é caixa_sessao (singular), não caixa_sessoes
        caixa_aberto_count = db_session.execute(
            text("SELECT COUNT(*) FROM caixa_sessao WHERE status = 'aberto'")
        ).scalar()
        
        # Produtos com estoque baixo
        estoque_baixo = db_session.execute(
            text("""
            SELECT COUNT(*) FROM produtos
            WHERE quantidade_estoque <= estoque_minimo
            AND ativo = 1
            """)
        ).scalar()
        
        return render_template(
            'dashboard.html',
            vendas_count=vendas_hoje['total_vendas'],
            vendas_valor=format_currency(vendas_hoje['total_valor']),
            caixa_aberto=caixa_aberto_count > 0,
            estoque_baixo=estoque_baixo
        )
    except Exception as e:
        logger.error(f"Erro no dashboard: {e}", exc_info=True)
        return render_template('error.html', error="Erro ao carregar dashboard"), 500

# ==================== API ENDPOINTS ====================

@app.route('/api/vendas')
@login_required
@limiter.limit("30 per minute")
def api_vendas():
    """API: Vendas do dia"""
    try:
        hoje = datetime.now().strftime('%Y-%m-%d')
        
        # Nota: vendas usa data_hora, não data_venda. Usuários tem login, não username.
        vendas = db_session.execute(
            text("""
            SELECT 
                v.id,
                v.data_hora,
                v.total as valor_total,
                v.forma_pagamento,
                u.login as vendedor
            FROM vendas v
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            WHERE DATE(v.data_hora) = :hoje
            ORDER BY v.data_hora DESC
            LIMIT 50
            """),
            {"hoje": hoje}
        ).fetchall()
        
        return jsonify([dict(v._mapping) for v in vendas])
    except Exception as e:
        logger.error(f"Erro API vendas: {e}", exc_info=True)
        return jsonify({'error': 'Erro ao buscar vendas'}), 500

@app.route('/api/caixa')
@login_required
@limiter.limit("30 per minute")
def api_caixa():
    """API: Status do caixa"""
    try:
        # Tabela é caixa_sessao, colunas são valor_ não saldo_
        caixa = db_session.execute(
            text("""
            SELECT 
                id,
                valor_abertura as saldo_inicial,
                valor_fechamento as saldo_atual,
                data_abertura,
                usuario_id as usuario_abertura_id
            FROM caixa_sessao
            WHERE status = 'aberto'
            LIMIT 1
            """)
        ).fetchone()
        
        if caixa:
            # Calcula saldo atual dinamicamente
            sessao_id = caixa['id']
            
            # Total vendas (dinheiro)
            vendas = db_session.execute(
                text("SELECT COALESCE(SUM(total), 0) FROM vendas WHERE caixa_sessao_id = :sessao_id AND forma_pagamento = 'dinheiro' AND status = 'ativa'"),
                {"sessao_id": sessao_id}
            ).scalar()
            
            # Suprimentos
            suprimentos = db_session.execute(
                text("SELECT COALESCE(SUM(valor), 0) FROM caixa_mov WHERE sessao_id = :sessao_id AND tipo = 'suprimento'"),
                {"sessao_id": sessao_id}
            ).scalar()
            
            # Sangrias
            sangrias = db_session.execute(
                text("SELECT COALESCE(SUM(valor), 0) FROM caixa_mov WHERE sessao_id = :sessao_id AND tipo = 'sangria'"),
                {"sessao_id": sessao_id}
            ).scalar()
            
            saldo_atual = caixa['saldo_inicial'] + vendas + suprimentos - sangrias
            
            # Atualiza o dict para retorno
            dados_caixa = dict(caixa._mapping)
            dados_caixa['saldo_atual'] = saldo_atual
            
            return jsonify(dados_caixa)
        else:
            return jsonify({'status': 'fechado'})
    except Exception as e:
        logger.error(f"Erro API caixa: {e}", exc_info=True)
        return jsonify({'error': 'Erro ao buscar caixa'}), 500

@app.route('/api/estoque')
@login_required
@limiter.limit("30 per minute")
def api_estoque():
    """API: Produtos com estoque baixo"""
    try:
        # Tabela produtos usa estoque_atual e unidade, não quantidade_estoque
        produtos = db_session.execute(
            text("""
            SELECT 
                nome,
                estoque_atual as quantidade_estoque,
                estoque_minimo,
                unidade as unidade_medida
            FROM produtos
            WHERE estoque_atual <= estoque_minimo
            AND ativo = 1
            ORDER BY estoque_atual ASC
            LIMIT 20
            """)
        ).fetchall()
        
        return jsonify([dict(p._mapping) for p in produtos])
    except Exception as e:
        logger.error(f"Erro API estoque: {e}", exc_info=True)
        return jsonify({'error': 'Erro ao buscar estoque'}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Página não encontrada"""
    return render_template('error.html', error="Página não encontrada"), 404

@app.errorhandler(500)
def internal_error(error):
    """Erro interno do servidor"""
    logger.error(f"Erro 500: {error}", exc_info=True)
    return render_template('error.html', error="Erro interno do servidor"), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    # Cria diretório de logs se não existir
    logs_dir = BASE_DIR / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    # Modo de produção
    logger.info("Iniciando Flask Dashboard em modo produção (0.0.0.0:8080)")
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False # Debug=False para produção e estabilidade
    )
