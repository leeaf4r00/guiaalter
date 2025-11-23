"""
Mobile Admin Routes - Dashboard administrativo mobile-friendly
Acesso via celular com autenticação integrada
ENHANCED: Gestão completa de usuários, IPs, sistema e backup
"""
from flask import render_template, request, redirect, url_for, jsonify, Blueprint, session, send_file
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from app import db
from app.models.users import User, BlockedIP, is_ip_blocked, block_ip, unblock_ip
from app.models.tours import Tour
from app.models.system import SystemSettings, AuditLog, get_setting, set_setting, log_action, is_maintenance_mode, set_maintenance_mode
from datetime import datetime, timedelta
import os
import shutil
import json

routes_mobile_admin = Blueprint('routes_mobile_admin', __name__, url_prefix='/mobile-admin')


def admin_required(f):
    """Decorator para verificar se o usuário é admin"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        # Verifica IP bloqueado
        client_ip = request.remote_addr
        if is_ip_blocked(client_ip):
            return jsonify({"error": "Seu IP foi bloqueado."}), 403
        
        # Verifica se é admin
        if not (current_user.is_admin or getattr(current_user, 'role', None) == 'admin'):
            return jsonify({"error": "Acesso negado. Apenas administradores."}), 403
        return f(*args, **kwargs)
    return decorated_function


# ==================== AUTHENTICATION ====================

@routes_mobile_admin.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login mobile-optimized"""
    # Verifica IP bloqueado
    client_ip = request.remote_addr
    if is_ip_blocked(client_ip):
        if request.method == 'POST':
            return jsonify({"error": "Seu IP foi bloqueado. Entre em contato com o administrador."}), 403
        return render_template('mobile_admin/blocked.html')
    
    # Verifica modo manutenção
    if is_maintenance_mode() and request.method == 'GET':
        return render_template('mobile_admin/maintenance.html')
    
    if request.method == 'GET':
        # Se já está logado e é admin, redireciona para dashboard
        if current_user.is_authenticated and (current_user.is_admin or getattr(current_user, 'role', None) == 'admin'):
            return redirect(url_for('routes_mobile_admin.dashboard'))
        return render_template('mobile_admin/login.html')
    
    # POST - processar login
    data = request.get_json() if request.is_json else request.form
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({"error": "Usuário e senha são obrigatórios"}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        # Verifica status do usuário
        if hasattr(user, 'status') and user.status == 'blocked':
            return jsonify({"error": "Sua conta foi bloqueada."}), 403
        
        # Verifica se é admin
        is_admin = user.is_admin or (hasattr(user, 'role') and user.role == 'admin')
        if not is_admin:
            return jsonify({"error": "Acesso negado. Apenas administradores."}), 403
        
        # Atualiza last_login
        if hasattr(user, 'last_login'):
            user.last_login = datetime.utcnow()
            db.session.commit()
        
        login_user(user, remember=True)
        
        # Log de ação
        log_action(user.id, 'login', ip_address=client_ip)
        
        return jsonify({
            "success": True, 
            "redirect": url_for('routes_mobile_admin.dashboard'),
            "message": "Login realizado com sucesso!"
        }), 200
    else:
        return jsonify({"error": "Usuário ou senha incorretos"}), 401


@routes_mobile_admin.route('/logout')
@login_required
def logout():
    """Logout"""
    log_action(current_user.id, 'logout', ip_address=request.remote_addr)
    logout_user()
    return redirect(url_for('routes_mobile_admin.login'))


# ==================== PUBLIC REGISTRATION ====================

@routes_mobile_admin.route('/register', methods=['GET', 'POST'])
def register():
    """Registro público para parceiros"""
    if request.method == 'GET':
        return render_template('mobile_admin/register.html')
    
    # POST - processar registro
    data = request.get_json() if request.is_json else request.form
    
    # Validações
    required = ['full_name', 'username', 'email', 'phone', 'partner_type', 'password']
    if not all(k in data for k in required):
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400
    
    # Verifica duplicados
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Nome de usuário já existe"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email já cadastrado"}), 400
    
    try:
        # Cria usuário com status 'pending'
        user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            role='partner',  # Sempre cria como parceiro
            is_admin=False,
            status='pending',  # Aguardando aprovação
            full_name=data['full_name'],
            phone=data['phone']
        )
        
        db.session.add(user)
        db.session.flush()  # Para obter o user.id
        
        # Cria registro de parceiro
        from app.models.partner import Partner
        partner = Partner(
            user_id=user.id,
            partner_type=data['partner_type'],
            business_name=data.get('business_name'),
            description=data.get('description')
        )
        
        db.session.add(partner)
        db.session.commit()
        
        # Log (sem user_id pois não está logado)
        log_action(None, 'partner_registration', 
                  target=user.username,
                  details=f"Tipo: {data['partner_type']}",
                  ip_address=request.remote_addr)
        
        return jsonify({
            "success": True, 
            "message": "Cadastro enviado com sucesso! Aguarde aprovação do administrador."
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao criar cadastro: {str(e)}"}), 500


# ==================== DASHBOARD ====================

@routes_mobile_admin.route('/')
@routes_mobile_admin.route('/dashboard')
@admin_required
def dashboard():
    """Dashboard principal mobile"""
    return render_template('mobile_admin/dashboard.html')


@routes_mobile_admin.route('/users')
@admin_required
def users_page():
    """Página de gerenciamento de usuários"""
    return render_template('mobile_admin/users.html')


@routes_mobile_admin.route('/system')
@admin_required
def system_page():
    """Página de controle do sistema"""
    return render_template('mobile_admin/system.html')


# ==================== API ENDPOINTS ====================

@routes_mobile_admin.route('/api/stats')
@admin_required
def api_stats():
    """Estatísticas gerais do sistema"""
    try:
        # Contadores básicos
        total_users = User.query.count()
        
        # Conta admins (is_admin=True OU role='admin')
        total_admins = User.query.filter(
            db.or_(User.is_admin == True, User.role == 'admin')
        ).count() if hasattr(User, 'role') else User.query.filter_by(is_admin=True).count()
        
        # Conta parceiros (role='partner')
        total_partners = User.query.filter_by(role='partner').count() if hasattr(User, 'role') else 0
        
        # Usuários bloqueados
        blocked_users = User.query.filter_by(status='blocked').count() if hasattr(User, 'status') else 0
        
        total_tours = Tour.query.count()
        active_tours = Tour.query.filter_by(is_active=True).count()
        
        # Usuários recentes (últimos 7 dias)
        week_ago = datetime.now() - timedelta(days=7)
        recent_users = User.query.filter(User.created_at >= week_ago).count()
        
        # IPs bloqueados
        blocked_ips_count = BlockedIP.query.count()
        
        # Modo manutenção
        maintenance = is_maintenance_mode()
        
        stats = {
            "users": {
                "total": total_users,
                "admins": total_admins,
                "partners": total_partners,
                "blocked": blocked_users,
                "recent": recent_users
            },
            "tours": {
                "total": total_tours,
                "active": active_tours,
                "inactive": total_tours - active_tours
            },
            "security": {
                "blocked_ips": blocked_ips_count
            },
            "system": {
                "timestamp": datetime.now().isoformat(),
                "admin_name": current_user.username,
                "maintenance_mode": maintenance
            }
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar estatísticas: {str(e)}"}), 500


@routes_mobile_admin.route('/api/users')
@admin_required
def api_users():
    """Lista de usuários"""
    try:
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        role_filter = request.args.get('role')  # 'admin', 'partner', 'user'
        status_filter = request.args.get('status')  # 'active', 'blocked'
        
        query = User.query
        
        # Filtros
        if role_filter and hasattr(User, 'role'):
            query = query.filter_by(role=role_filter)
        if status_filter and hasattr(User, 'status'):
            query = query.filter_by(status=status_filter)
        
        users = query.order_by(User.created_at.desc()).limit(limit).offset(offset).all()
        
        users_data = [user.to_dict() for user in users]
        
        return jsonify({
            "users": users_data,
            "total": query.count(),
            "limit": limit,
            "offset": offset
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar usuários: {str(e)}"}), 500


@routes_mobile_admin.route('/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def api_user_detail(user_id):
    """Detalhes, edição e exclusão de usuário"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'GET':
        return jsonify(user.to_dict()), 200
    
    elif request.method == 'PUT':
        # Editar usuário
        data = request.get_json()
        
        try:
            if 'email' in data:
                user.email = data['email']
            if 'role' in data and hasattr(user, 'role'):
                user.role = data['role']
                # Sincroniza is_admin
                user.is_admin = (data['role'] == 'admin')
            if 'status' in data and hasattr(user, 'status'):
                user.status = data['status']
            if 'full_name' in data and hasattr(user, 'full_name'):
                user.full_name = data['full_name']
            if 'phone' in data and hasattr(user, 'phone'):
                user.phone = data['phone']
            if 'password' in data and data['password']:
                user.password = generate_password_hash(data['password'])
            
            db.session.commit()
            
            # Log
            log_action(current_user.id, 'update_user', 
                      target=user.username, 
                      details=json.dumps(data),
                      ip_address=request.remote_addr)
            
            return jsonify({"success": True, "user": user.to_dict()}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Erro ao atualizar usuário: {str(e)}"}), 500
    
    elif request.method == 'DELETE':
        # Não pode deletar a si mesmo
        if user.id == current_user.id:
            return jsonify({"error": "Você não pode deletar sua própria conta"}), 400
        
        try:
            username = user.username
            db.session.delete(user)
            db.session.commit()
            
            # Log
            log_action(current_user.id, 'delete_user', 
                      target=username,
                      ip_address=request.remote_addr)
            
            return jsonify({"success": True, "message": "Usuário deletado"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Erro ao deletar usuário: {str(e)}"}), 500


@routes_mobile_admin.route('/api/users/create', methods=['POST'])
@admin_required
def api_create_user():
    """Criar novo usuário"""
    data = request.get_json()
    
    # Validações
    required = ['username', 'email', 'password']
    if not all(k in data for k in required):
        return jsonify({"error": "Campos obrigatórios: username, email, password"}), 400
    
    # Verifica duplicados
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username já existe"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email já cadastrado"}), 400
    
    try:
        role = data.get('role', 'user')
        is_admin = (role == 'admin')
        
        user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            role=role if hasattr(User, 'role') else 'user',
            is_admin=is_admin,
            status=data.get('status', 'active') if hasattr(User, 'status') else 'active',
            full_name=data.get('full_name') if hasattr(User, 'full_name') else None,
            phone=data.get('phone') if hasattr(User, 'phone') else None
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Log
        log_action(current_user.id, 'create_user', 
                  target=user.username,
                  details=f"Role: {role}",
                  ip_address=request.remote_addr)
        
        return jsonify({"success": True, "user": user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao criar usuário: {str(e)}"}), 500


# ==================== PARTNER APPROVALS ====================

@routes_mobile_admin.route('/api/partners/pending')
@admin_required
def api_pending_partners():
    """Lista de parceiros aguardando aprovação"""
    try:
        from app.models.partner import Partner
        
        # Busca usuários com status pending e role partner
        pending_users = User.query.filter_by(status='pending', role='partner').order_by(User.created_at.desc()).all()
        
        partners_data = []
        for user in pending_users:
            user_dict = user.to_dict()
            
            # Adiciona informações do parceiro
            partner = Partner.query.filter_by(user_id=user.id).first()
            if partner:
                user_dict['partner_info'] = partner.to_dict()
            
            partners_data.append(user_dict)
        
        return jsonify({
            "pending_partners": partners_data,
            "total": len(partners_data)
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar parceiros pendentes: {str(e)}"}), 500


@routes_mobile_admin.route('/api/partners/<int:user_id>/approve', methods=['POST'])
@admin_required
def api_approve_partner(user_id):
    """Aprovar parceiro"""
    user = User.query.get_or_404(user_id)
    
    if user.role != 'partner':
        return jsonify({"error": "Usuário não é um parceiro"}), 400
    
    if user.status != 'pending':
        return jsonify({"error": "Usuário não está pendente"}), 400
    
    try:
        # Atualiza status para active
        user.status = 'active'
        
        # Marca parceiro como verificado
        from app.models.partner import Partner
        partner = Partner.query.filter_by(user_id=user.id).first()
        if partner:
            partner.verified = True
            partner.verification_date = datetime.utcnow()
            partner.verified_by = current_user.id
        
        db.session.commit()
        
        # Log
        log_action(current_user.id, 'approve_partner', 
                  target=user.username,
                  details=f"Partner type: {partner.partner_type if partner else 'unknown'}",
                  ip_address=request.remote_addr)
        
        return jsonify({
            "success": True, 
            "message": "Parceiro aprovado com sucesso",
            "user": user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao aprovar parceiro: {str(e)}"}), 500


@routes_mobile_admin.route('/api/partners/<int:user_id>/reject', methods=['POST'])
@admin_required
def api_reject_partner(user_id):
    """Rejeitar/Deletar parceiro pendente"""
    user = User.query.get_or_404(user_id)
    
    if user.role != 'partner':
        return jsonify({"error": "Usuário não é um parceiro"}), 400
    
    if user.status != 'pending':
        return jsonify({"error": "Usuário não está pendente"}), 400
    
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'Não especificado')
        
        username = user.username
        
        # Deleta parceiro e usuário
        from app.models.partner import Partner
        partner = Partner.query.filter_by(user_id=user.id).first()
        if partner:
            db.session.delete(partner)
        
        db.session.delete(user)
        db.session.commit()
        
        # Log
        log_action(current_user.id, 'reject_partner', 
                  target=username,
                  details=f"Reason: {reason}",
                  ip_address=request.remote_addr)
        
        return jsonify({
            "success": True, 
            "message": "Parceiro rejeitado"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao rejeitar parceiro: {str(e)}"}), 500


# ==================== IP BLOCKING ====================

@routes_mobile_admin.route('/api/blocked-ips')
@admin_required
def api_blocked_ips():
    """Lista de IPs bloqueados"""
    try:
        blocked_ips = BlockedIP.query.order_by(BlockedIP.blocked_at.desc()).all()
        return jsonify({
            "blocked_ips": [ip.to_dict() for ip in blocked_ips],
            "total": len(blocked_ips)
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar IPs bloqueados: {str(e)}"}), 500


@routes_mobile_admin.route('/api/blocked-ips/add', methods=['POST'])
@admin_required
def api_block_ip():
    """Bloquear um IP"""
    data = request.get_json()
    
    if 'ip_address' not in data:
        return jsonify({"error": "IP address é obrigatório"}), 400
    
    ip_address = data['ip_address']
    reason = data.get('reason', 'Bloqueado pelo administrador')
    expires_at = data.get('expires_at')  # ISO format ou None
    
    if expires_at:
        try:
            expires_at = datetime.fromisoformat(expires_at)
        except:
            expires_at = None
    
    success = block_ip(ip_address, reason, current_user.id, expires_at)
    
    if success:
        log_action(current_user.id, 'block_ip', 
                  target=ip_address,
                  details=reason,
                  ip_address=request.remote_addr)
        return jsonify({"success": True, "message": "IP bloqueado"}), 200
    else:
        return jsonify({"error": "Erro ao bloquear IP"}), 500


@routes_mobile_admin.route('/api/blocked-ips/<ip_address>', methods=['DELETE'])
@admin_required
def api_unblock_ip(ip_address):
    """Desbloquear um IP"""
    success = unblock_ip(ip_address)
    
    if success:
        log_action(current_user.id, 'unblock_ip', 
                  target=ip_address,
                  ip_address=request.remote_addr)
        return jsonify({"success": True, "message": "IP desbloqueado"}), 200
    else:
        return jsonify({"error": "Erro ao desbloquear IP"}), 500


# ==================== SYSTEM CONTROL ====================

@routes_mobile_admin.route('/api/system/maintenance', methods=['GET', 'POST'])
@admin_required
def api_maintenance_mode():
    """Controle do modo manutenção"""
    if request.method == 'GET':
        return jsonify({"maintenance_mode": is_maintenance_mode()}), 200
    
    # POST - ativar/desativar
    data = request.get_json()
    enabled = data.get('enabled', False)
    
    success = set_maintenance_mode(enabled, current_user.id)
    
    if success:
        return jsonify({
            "success": True, 
            "maintenance_mode": enabled,
            "message": f"Modo manutenção {'ativado' if enabled else 'desativado'}"
        }), 200
    else:
        return jsonify({"error": "Erro ao alterar modo manutenção"}), 500


@routes_mobile_admin.route('/api/system/backup', methods=['POST'])
@admin_required
def api_backup_database():
    """Criar backup do banco de dados"""
    try:
        # Caminho do banco de dados
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')
        
        if not os.path.exists(db_path):
            return jsonify({"error": "Banco de dados não encontrado"}), 404
        
        # Cria diretório de backups
        backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Nome do backup com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'database_backup_{timestamp}.db'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copia banco de dados
        shutil.copy2(db_path, backup_path)
        
        # Log
        log_action(current_user.id, 'backup_database', 
                  target=backup_filename,
                  ip_address=request.remote_addr)
        
        return jsonify({
            "success": True, 
            "message": "Backup criado com sucesso",
            "filename": backup_filename,
            "size": os.path.getsize(backup_path)
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao criar backup: {str(e)}"}), 500


@routes_mobile_admin.route('/api/system/backups')
@admin_required
def api_list_backups():
    """Listar backups disponíveis"""
    try:
        backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backups')
        
        if not os.path.exists(backup_dir):
            return jsonify({"backups": []}), 200
        
        backups = []
        for filename in os.listdir(backup_dir):
            if filename.endswith('.db'):
                filepath = os.path.join(backup_dir, filename)
                backups.append({
                    "filename": filename,
                    "size": os.path.getsize(filepath),
                    "created_at": datetime.fromtimestamp(os.path.getctime(filepath)).isoformat()
                })
        
        # Ordena por data (mais recente primeiro)
        backups.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({"backups": backups}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao listar backups: {str(e)}"}), 500


@routes_mobile_admin.route('/api/system/restore/<filename>', methods=['POST'])
@admin_required
def api_restore_database(filename):
    """Restaurar banco de dados a partir de backup"""
    try:
        backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backups')
        backup_path = os.path.join(backup_dir, filename)
        
        if not os.path.exists(backup_path):
            return jsonify({"error": "Backup não encontrado"}), 404
        
        # Caminho do banco atual
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')
        
        # Faz backup do banco atual antes de restaurar
        current_backup = f'database_before_restore_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        shutil.copy2(db_path, os.path.join(backup_dir, current_backup))
        
        # Restaura backup
        shutil.copy2(backup_path, db_path)
        
        # Log
        log_action(current_user.id, 'restore_database', 
                  target=filename,
                  ip_address=request.remote_addr)
        
        return jsonify({
            "success": True, 
            "message": "Banco de dados restaurado com sucesso",
            "warning": "Você precisará fazer login novamente"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao restaurar banco: {str(e)}"}), 500


# ==================== AUDIT LOGS ====================

@routes_mobile_admin.route('/api/logs')
@admin_required
def api_audit_logs():
    """Logs de auditoria"""
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(limit).offset(offset).all()
        
        logs_data = []
        for log in logs:
            log_dict = log.to_dict()
            # Adiciona username
            user = User.query.get(log.user_id)
            log_dict['username'] = user.username if user else 'Desconhecido'
            logs_data.append(log_dict)
        
        return jsonify({
            "logs": logs_data,
            "total": AuditLog.query.count(),
            "limit": limit,
            "offset": offset
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar logs: {str(e)}"}), 500


# ==================== TOURS (mantido para compatibilidade) ====================

@routes_mobile_admin.route('/api/tours')
@admin_required
def api_tours():
    """Lista de tours"""
    try:
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        tours = Tour.query.order_by(Tour.created_at.desc()).limit(limit).offset(offset).all()
        
        tours_data = [{
            "id": tour.id,
            "title": tour.title,
            "category": tour.category,
            "is_active": tour.is_active,
            "created_at": tour.created_at.isoformat() if tour.created_at else None
        } for tour in tours]
        
        return jsonify({
            "tours": tours_data,
            "total": Tour.query.count(),
            "limit": limit,
            "offset": offset
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar tours: {str(e)}"}), 500


@routes_mobile_admin.route('/api/activity')
@admin_required
def api_activity():
    """Atividade recente do sistema"""
    try:
        # Últimos 5 usuários cadastrados
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        
        # Últimos 5 tours criados
        recent_tours = Tour.query.order_by(Tour.created_at.desc()).limit(5).all()
        
        activity = {
            "recent_users": [{
                "type": "user_registered",
                "username": user.username,
                "role": getattr(user, 'role', 'user'),
                "timestamp": user.created_at.isoformat() if user.created_at else None
            } for user in recent_users],
            "recent_tours": [{
                "type": "tour_created",
                "title": tour.title,
                "category": tour.category,
                "timestamp": tour.created_at.isoformat() if tour.created_at else None
            } for tour in recent_tours]
        }
        
        return jsonify(activity), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar atividade: {str(e)}"}), 500
