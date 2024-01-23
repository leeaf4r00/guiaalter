from flask import Blueprint, render_template, jsonify
from app.database import db

# Criando o Blueprint para administração
routes_admin = Blueprint('routes_admin', __name__)

# Definindo a rota para o painel de administração


@routes_admin.route('/admin/painel')
def painel_adm():
    # Aqui você pode adicionar qualquer lógica específica que precisa ser executada antes de renderizar o template
    return render_template('admin/paineladm.html')

# Rota para listar todos os usuários cadastrados


@routes_admin.route('/admin/user_list')
def user_list():
    # Obter a lista de usuários do banco de dados
    users = db.get_all_users()

    # Verificar se a lista de usuários não é None
    if users is not None:
        # Converter a lista de usuários em um formato JSON
        users_json = [{'id': user['id'], 'username': user['username'],
                       'email': user['email']} for user in users]
    else:
        # Se users é None, retornar uma lista vazia
        users_json = []

    # Retornar os dados dos usuários em formato JSON
    return jsonify({'users': users_json})
