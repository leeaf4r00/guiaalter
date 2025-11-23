"""
Script para criar usuário administrador
Execute: python create_admin.py
"""
from app import create_app, db
from app.models.users import User
from werkzeug.security import generate_password_hash

def create_admin_user():
    """Cria usuário administrador padrão"""
    app = create_app()
    
    with app.app_context():
        # Verificar se admin já existe
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print("❌ Usuário 'admin' já existe!")
            print(f"   ID: {admin.id}")
            print(f"   Email: {admin.email}")
            print(f"   Admin: {admin.is_admin}")
            return False
        
        # Criar novo admin
        print("Criando usuário administrador...")
        admin = User(
            username='admin',
            email='admin@guiadealter.com',
            password=generate_password_hash('admin123'),  # MUDE ESTA SENHA!
            is_admin=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Usuário admin criado com sucesso!")
        print("")
        print("=" * 50)
        print("   CREDENCIAIS DE ACESSO")
        print("=" * 50)
        print("   Username: admin")
        print("   Senha:    admin123")
        print("   Email:    admin@guiadealter.com")
        print("=" * 50)
        print("")
        print("⚠️  IMPORTANTE: Mude a senha após o primeiro login!")
        print("")
        print("Acesse o dashboard em:")
        print("   Local:    http://localhost:5000/mobile-admin/login")
        print("   Wi-Fi:    http://[SEU-IP]:5000/mobile-admin/login")
        print("")
        return True

if __name__ == '__main__':
    create_admin_user()
