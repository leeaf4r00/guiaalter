from app import create_app, db
from app.models.users import User
import os

def reset_users():
    app = create_app()
    with app.app_context():
        print("🗑️ Limpando tabela de usuários...")
        try:
            num_users = db.session.query(User).delete()
            db.session.commit()
            print(f"✅ {num_users} usuários removidos.")
            print("🚀 O sistema agora está pronto para o setup inicial (primeiro uso).")
        except Exception as e:
            print(f"❌ Erro ao limpar usuários: {e}")

if __name__ == "__main__":
    reset_users()
