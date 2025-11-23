from app import create_app, db
from app.models.users import User
from werkzeug.security import generate_password_hash
import sys

def ensure_admin():
    app = create_app()
    with app.app_context():
        print("🔄 Verificando banco de dados...")
        
        # Garante que as tabelas existam
        db.create_all()
        
        # Verifica se existe algum usuário
        if User.query.first():
            print("✅ Já existem usuários cadastrados.")
            
            # Verifica se existe o admin específico
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print("✅ Usuário 'admin' já existe.")
                # Garante que é admin
                if not admin.is_admin:
                    admin.is_admin = True
                    admin.role = 'admin'
                    db.session.commit()
                    print("🔄 Permissões de 'admin' atualizadas.")
            return

        print("⚠️ Nenhum usuário encontrado. Criando admin padrão...")
        
        try:
            admin = User(
                username='admin',
                email='admin@guiaalter.com',
                password=generate_password_hash('admin123'),
                role='admin',
                is_admin=True,
                status='active',
                full_name='Administrador Sistema'
            )
            
            db.session.add(admin)
            db.session.commit()
            print("🎉 Usuário 'admin' criado com sucesso!")
            print("🔑 Login: admin")
            print("🔑 Senha: admin123")
            
        except Exception as e:
            print(f"❌ Erro ao criar admin: {e}")
            sys.exit(1)

if __name__ == "__main__":
    ensure_admin()
