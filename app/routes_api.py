from flask import Blueprint, jsonify, request, session
from app.models.product import Product

api = Blueprint('api', __name__)

# ----------------------------------------------------------------------
# Endpoint: Lista de produtos (JSON)
# ----------------------------------------------------------------------
@api.route('/api/products')
def get_products():
    """Retorna todos os produtos cadastrados como JSON."""
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

# ----------------------------------------------------------------------
# Endpoint: Adiciona produto ao carrinho (session based)
# ----------------------------------------------------------------------
@api.route('/api/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Adiciona o produto ao carrinho armazenado na sessão."""
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', [])
    cart.append(product.id)
    session['cart'] = cart
    return jsonify({
        'message': f'Produto "{product.name}" adicionado ao carrinho!',
        'cart_total': len(cart)
    })
