from flask import Blueprint, render_template

# Criando o Blueprint para administração
routes_admin = Blueprint('routes_admin', __name__)

# Definindo a rota para o painel de administração


@routes_admin.route('/admin/painel')
def painel_adm():
    # Aqui você pode adicionar qualquer lógica específica que precisa ser executada antes de renderizar o template
    return render_template('admin/paineladm.html')
