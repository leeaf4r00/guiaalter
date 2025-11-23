"""
Tours Routes - Rotas de passeios
"""
from flask import render_template, Blueprint

routes_tours = Blueprint('routes_tours', __name__)


# Placeholder - adicione suas rotas de tours aqui
@routes_tours.route('/tours')
def tours_list():
    """Lista de tours"""
    return render_template('passeios.html')
