"""
Routes - Rotas principais da aplicação
"""
from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models.users import User, get_user_by_username, get_user_by_email, create_user
from app.models.tours import Tour
import os

routes = Blueprint('routes', __name__)


@routes.route('/favicon.ico')
def favicon():
    """Serve o favicon"""
    return send_from_directory(
        os.path.join(routes.root_path, '..', 'static'),
        'favicon.ico',
        mimetype='image/x-icon'
    )


@routes.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')


@routes.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'GET':
        return render_template('login.html')
    
    # POST - processar login
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Usuário e senha são obrigatórios"}), 400

    user = get_user_by_username(username)

    if user and check_password_hash(user.password, password):
        login_user(user, remember=True)
        
        if user.is_admin:
            return jsonify({"success": True, "redirect": url_for('routes_admin.painel')}), 200
        else:
            return jsonify({"success": True, "redirect": url_for('routes.index')}), 200
    else:
        return jsonify({"message": "Usuário ou senha incorretos"}), 401


@routes.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if request.method == 'GET':
        return render_template('cadastro.html')
    
    # POST - processar registro
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Validações
    if not username or not email or not password:
        return jsonify({"message": "Todos os campos são obrigatórios"}), 400
    
    if len(password) < 6:
        return jsonify({"message": "A senha deve ter no mínimo 6 caracteres"}), 400
    
    # Verifica se usuário já existe
    if get_user_by_username(username):
        return jsonify({"message": "Nome de usuário já existe"}), 400
    
    if get_user_by_email(email):
        return jsonify({"message": "E-mail já cadastrado"}), 400
    
    # Cria usuário
    hashed_password = generate_password_hash(password)
    user = create_user(username, email, hashed_password)
    
    if user:
        return jsonify({"success": True, "message": "Conta criada com sucesso!"}), 201
    else:
        return jsonify({"message": "Erro ao criar conta. Tente novamente."}), 500


@routes.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('routes.index'))


@routes.route('/perfil')
@login_required
def perfil():
    """Página de perfil do usuário"""
    return render_template('perfil.html')


@routes.route('/busca')
def busca():
    """Rota de busca"""
    query = request.args.get('q', '')
    results = []
    if query:
        # Busca case-insensitive por título ou descrição
        results = Tour.query.filter(
            (Tour.title.ilike(f'%{query}%')) | 
            (Tour.description.ilike(f'%{query}%'))
        ).all()
    
    return render_template('busca.html', query=query, results=results)


# Páginas de conteúdo
@routes.route('/reservas')
def reservas():
    return render_template('reservas.html')


@routes.route('/pacotes')
def pacotes():
    return render_template('Pacotes.html')


@routes.route('/buffets')
def buffets():
    return render_template('buffets.html')


@routes.route('/hotels')
def hotels():
    return render_template('hotels.html')


@routes.route('/passeios')
def passeios():
    return render_template('passeios.html')


@routes.route('/contato')
def contato():
    return render_template('contato.html')


@routes.route('/veiculos')
def veiculos():
    lanchas = Tour.query.filter_by(category='veiculo_lancha', is_active=True).all()
    barcos = Tour.query.filter_by(category='veiculo_barco', is_active=True).all()
    transfers = Tour.query.filter_by(category='veiculo_transfer', is_active=True).all()
    return render_template('veiculos.html', lanchas=lanchas, barcos=barcos, transfers=transfers)


@routes.route('/sobrenos')
def sobrenos():
    return render_template('sobrenos.html')


@routes.route('/conhecaalter')
def conhecaalter():
    return render_template('conheca_alter.html')


@routes.route('/souvenir')
def souvenir():
    return render_template('souvenir.html')


@routes.route('/sejanossoparceiro')
def sejanossoparceiro():
    return render_template('sejanossoparceiro.html')


@routes.route('/rotas')
def rotas():
    destinos = [
        {
            "id": "vila",
            "name": "Vila de Alter do Chão",
            "coords": [-2.5031, -54.9554],
            "desc": "O ponto de partida para todas as aventuras.",
            "details": "A vila é o coração de Alter. Aqui você encontra a orla, restaurantes, lojas de artesanato e o terminal de barcos.",
            "img": "/static/img/alterdochao.jpg",
            "type": "cidade"
        },
        {
            "id": "ilhadoamor",
            "name": "Ilha do Amor",
            "coords": [-2.5015, -54.9575],
            "desc": "O cartão postal mais famoso.",
            "details": "Uma faixa de areia branca banhada pelo Rio Tapajós de um lado e pelo Lago Verde do outro. Acesso via catraia (R$ 5-10).",
            "img": "/static/img/alterdochao_hero.jpg",
            "type": "praia"
        },
        {
            "id": "piraoca",
            "name": "Morro da Piraoca",
            "coords": [-2.4960, -54.9600],
            "desc": "A melhor vista panorâmica da região.",
            "details": "Uma caminhada de 40 minutos leva ao topo, de onde se vê o Rio Tapajós, o Lago Verde e a imensidão da floresta.",
            "img": "/static/img/topo1.jpg",
            "type": "natureza"
        },
        {
            "id": "lagoverde",
            "name": "Lago Verde (Floresta Encantada)",
            "coords": [-2.5100, -54.9450],
            "desc": "Águas mágicas que mudam de cor.",
            "details": "Lar da Floresta Encantada, onde árvores ficam submersas. Ideal para passeios de canoa e caiaque.",
            "img": "/static/img/lagoverde/florestaencantada.jpg",
            "type": "natureza"
        },
        {
            "id": "pontacururu",
            "name": "Ponta do Cururu",
            "coords": [-2.4700, -54.9700],
            "desc": "O melhor pôr do sol.",
            "details": "Uma ponta de areia que entra no rio, famosa pela aparição de botos e pelo espetáculo do sol se pondo.",
            "img": "/static/img/descendoorio/pontadocururu1.jpg",
            "type": "praia"
        },
        {
            "id": "pindobal",
            "name": "Praia do Pindobal",
            "coords": [-2.5550, -54.9650],
            "desc": "Tranquilidade e restaurantes.",
            "details": "Praia com boa infraestrutura, águas calmas e restaurantes que servem peixes frescos na beira do rio.",
            "img": "/static/img/subindoorio/pindobal1.jpg",
            "type": "praia"
        },
        {
            "id": "pontadepedras",
            "name": "Ponta de Pedras",
            "coords": [-2.3900, -54.8900],
            "desc": "Formações rochosas únicas.",
            "details": "Diferente das outras praias, aqui as pedras compõem o cenário, criando piscinas naturais dependendo do nível do rio.",
            "img": "/static/img/descendoorio/pontadepedras1.jpg",
            "type": "praia"
        },
        {
            "id": "canaldojari",
            "name": "Canal do Jari",
            "coords": [-2.4300, -55.0500],
            "desc": "Jardim das Vitórias-Régias.",
            "details": "Um canal estreito rico em biodiversidade. Veja preguiças, macacos, pássaros e o jardim de vitórias-régias.",
            "img": "/static/img/canaldojari.jpg",
            "type": "natureza"
        },
        {
            "id": "flona",
            "name": "Flona do Tapajós",
            "coords": [-2.8500, -55.0300],
            "desc": "A imponência da Amazônia.",
            "details": "Floresta Nacional com árvores centenárias como a Sumaúma. Trilhas guiadas por comunitários locais.",
            "img": "/static/img/flonadotapajos.jpg",
            "type": "natureza"
        }
    ]
    return render_template('rotas.html', destinos=destinos)


@routes.route('/top10para')
def top10para():
    return render_template('top10para.html')


# Passeios - iframes
@routes.route('/rioarapiuns')
def rioarapiuns():
    tours = Tour.query.filter_by(category='rioarapiuns', is_active=True).all()
    return render_template('rioarapiuns.html', tours=tours)


@routes.route('/lagoverde')
def lagoverde():
    tours = Tour.query.filter_by(category='lagoverde', is_active=True).all()
    return render_template('lagoverde.html', tours=tours)


@routes.route('/descendoorio')
def descendoorio():
    tours = Tour.query.filter_by(category='descendoorio', is_active=True).all()
    return render_template('descendoorio.html', tours=tours)


@routes.route('/subindoorio')
def subindoorio():
    tours = Tour.query.filter_by(category='subindoorio', is_active=True).all()
    return render_template('subindoorio.html', tours=tours)


@routes.route('/tourdestaques')
def tourdestaques():
    tours = Tour.query.filter_by(category='destaque', is_active=True).all()
    return render_template('tourdestaques.html', tours=tours)


@routes.route('/depoimentos')
def depoimentos():
    return render_template('depoimentos.html')


# Páginas legais
@routes.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')


@routes.route('/terms-of-use')
def terms_of_use():
    return render_template('terms-of-use.html')


@routes.route('/suporte')
def suporte():
    return render_template('suporte.html')
