"""
Public Portal Routes - Portal público para turistas
Acesso via QR code e web
"""
from flask import render_template, request, jsonify, Blueprint, send_file
from app.models.tours import Tour
from app.models.users import User
from app.models.partner import Partner
import qrcode
from io import BytesIO
import os

routes_public = Blueprint('routes_public', __name__, url_prefix='/portal')


# ==================== PÁGINAS PÚBLICAS ====================

@routes_public.route('/')
def home():
    """Página inicial do portal público"""
    return render_template('public/home.html')


@routes_public.route('/tours')
def tours_catalog():
    """Catálogo de tours"""
    return render_template('public/tours.html')


@routes_public.route('/tours/<int:tour_id>')
def tour_detail(tour_id):
    """Detalhes de um tour específico"""
    tour = Tour.query.get_or_404(tour_id)
    return render_template('public/tour_detail.html', tour=tour)


@routes_public.route('/parceiros')
def partners_list():
    """Lista de parceiros (hotéis, restaurantes, guias)"""
    return render_template('public/partners.html')


@routes_public.route('/parceiros/<int:partner_id>')
def partner_detail(partner_id):
    """Perfil de um parceiro"""
    partner = Partner.query.get_or_404(partner_id)
    user = User.query.get(partner.user_id)
    return render_template('public/partner_detail.html', partner=partner, user=user)


@routes_public.route('/sobre')
def about():
    """Sobre Alter do Chão"""
    return render_template('public/about.html')


@routes_public.route('/contato')
def contact():
    """Página de contato"""
    return render_template('public/contact.html')


# ==================== API PÚBLICA ====================

@routes_public.route('/api/tours')
def api_public_tours():
    """Lista pública de tours ativos"""
    try:
        # Filtros
        category = request.args.get('category')
        search = request.args.get('search')
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Query base - apenas tours ativos
        query = Tour.query.filter_by(is_active=True)
        
        # Aplica filtros
        if category:
            query = query.filter_by(category=category)
        if search:
            query = query.filter(
                Tour.title.ilike(f'%{search}%') | 
                Tour.description.ilike(f'%{search}%')
            )
        
        # Paginação
        tours = query.order_by(Tour.created_at.desc()).limit(limit).offset(offset).all()
        
        tours_data = [{
            'id': tour.id,
            'title': tour.title,
            'category': tour.category,
            'description': tour.description,
            'price': getattr(tour, 'price', None),
            'duration': getattr(tour, 'duration', None),
            'image_url': getattr(tour, 'image_url', None),
            'created_at': tour.created_at.isoformat() if tour.created_at else None
        } for tour in tours]
        
        return jsonify({
            'tours': tours_data,
            'total': query.count(),
            'limit': limit,
            'offset': offset
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes_public.route('/api/partners')
def api_public_partners():
    """Lista pública de parceiros verificados"""
    try:
        partner_type = request.args.get('type')
        limit = request.args.get('limit', 20, type=int)
        
        # Query - apenas parceiros verificados e ativos
        query = Partner.query.filter_by(verified=True).join(User).filter_by(status='active')
        
        if partner_type:
            query = query.filter(Partner.partner_type == partner_type)
        
        partners = query.limit(limit).all()
        
        partners_data = []
        for partner in partners:
            user = User.query.get(partner.user_id)
            partners_data.append({
                'id': partner.id,
                'business_name': partner.business_name or user.full_name,
                'partner_type': partner.partner_type,
                'description': partner.description,
                'phone': user.phone,
                'verified': partner.verified
            })
        
        return jsonify({
            'partners': partners_data,
            'total': len(partners_data)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes_public.route('/api/categories')
def api_tour_categories():
    """Lista de categorias de tours disponíveis"""
    try:
        from sqlalchemy import func
        
        # Busca categorias únicas de tours ativos
        categories = Tour.query.filter_by(is_active=True).with_entities(
            Tour.category,
            func.count(Tour.id).label('count')
        ).group_by(Tour.category).all()
        
        categories_data = [
            {'name': cat, 'count': count} 
            for cat, count in categories if cat
        ]
        
        return jsonify({'categories': categories_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== QR CODE ====================

@routes_public.route('/qr/<path:url>')
def generate_qr(url):
    """Gera QR Code para uma URL"""
    try:
        # Cria QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Adiciona dados
        full_url = request.host_url.rstrip('/') + '/' + url.lstrip('/')
        qr.add_data(full_url)
        qr.make(fit=True)
        
        # Cria imagem
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Salva em buffer
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return str(e), 500


@routes_public.route('/qr-tour/<int:tour_id>')
def qr_tour(tour_id):
    """Página com QR Code de um tour"""
    tour = Tour.query.get_or_404(tour_id)
    return render_template('public/qr_tour.html', tour=tour)


@routes_public.route('/qr-partner/<int:partner_id>')
def qr_partner(partner_id):
    """Página com QR Code de um parceiro"""
    partner = Partner.query.get_or_404(partner_id)
    user = User.query.get(partner.user_id)
    return render_template('public/qr_partner.html', partner=partner, user=user)


# ==================== BUSCA ====================

@routes_public.route('/buscar')
def search():
    """Página de busca"""
    query = request.args.get('q', '')
    return render_template('public/search.html', query=query)


@routes_public.route('/api/search')
def api_search():
    """API de busca unificada"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'results': []}), 200
        
        results = []
        
        # Busca em tours
        tours = Tour.query.filter(
            Tour.is_active == True,
            (Tour.title.ilike(f'%{query}%') | Tour.description.ilike(f'%{query}%'))
        ).limit(5).all()
        
        for tour in tours:
            results.append({
                'type': 'tour',
                'id': tour.id,
                'title': tour.title,
                'description': tour.description[:100] + '...' if len(tour.description) > 100 else tour.description,
                'url': f'/portal/tours/{tour.id}'
            })
        
        # Busca em parceiros
        partners = Partner.query.filter(
            Partner.verified == True,
            (Partner.business_name.ilike(f'%{query}%') | Partner.description.ilike(f'%{query}%'))
        ).limit(5).all()
        
        for partner in partners:
            user = User.query.get(partner.user_id)
            if user and user.status == 'active':
                results.append({
                    'type': 'partner',
                    'id': partner.id,
                    'title': partner.business_name or user.full_name,
                    'description': partner.description[:100] + '...' if partner.description and len(partner.description) > 100 else partner.description,
                    'url': f'/portal/parceiros/{partner.id}'
                })
        
        return jsonify({
            'query': query,
            'results': results,
            'total': len(results)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
