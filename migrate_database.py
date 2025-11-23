"""
Database Migration Script
Adiciona novas colunas e tabelas para o sistema administrativo completo

Execute: python migrate_database.py
"""
from app import create_app, db
from app.models.users import User, BlockedIP
from app.models.system import SystemSettings, AuditLog
from app.models.partner import Partner
from sqlalchemy import text
import sys

def migrate_database():
    """Executa migração do banco de dados"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("  MIGRAÇÃO DO BANCO DE DADOS")
        print("=" * 60)
        print()
        
        try:
            # 1. Adiciona novas colunas na tabela users (se não existirem)
            print("1️⃣  Atualizando tabela 'users'...")
            
            # Verifica se colunas já existem
            inspector = db.inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('users')]
            
            columns_to_add = {
                'role': "ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user' NOT NULL",
                'status': "ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active' NOT NULL",
                'updated_at': "ALTER TABLE users ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP",
                'last_login': "ALTER TABLE users ADD COLUMN last_login DATETIME",
                'full_name': "ALTER TABLE users ADD COLUMN full_name VARCHAR(200)",
                'phone': "ALTER TABLE users ADD COLUMN phone VARCHAR(20)"
            }
            
            for col_name, sql in columns_to_add.items():
                if col_name not in existing_columns:
                    try:
                        db.session.execute(text(sql))
                        print(f"   ✅ Coluna '{col_name}' adicionada")
                    except Exception as e:
                        print(f"   ⚠️  Coluna '{col_name}': {str(e)}")
                else:
                    print(f"   ⏭️  Coluna '{col_name}' já existe")
            
            db.session.commit()
            
            # 2. Sincroniza role com is_admin
            print("\n2️⃣  Sincronizando roles com is_admin...")
            
            # Usa SQL direto para evitar problemas com o modelo
            try:
                db.session.execute(text("UPDATE users SET role = 'admin' WHERE is_admin = 1 AND role != 'admin'"))
                result = db.session.execute(text("SELECT COUNT(*) FROM users WHERE role = 'admin'"))
                admin_count = result.scalar()
                print(f"   ✅ {admin_count} administradores sincronizados")
                db.session.commit()
            except Exception as e:
                print(f"   ⚠️  Erro na sincronização: {str(e)}")
            
            # 3. Cria novas tabelas
            print("\n3️⃣  Criando novas tabelas...")
            
            # Cria todas as tabelas (ignora se já existirem)
            db.create_all()
            
            # Verifica quais tabelas foram criadas
            tables = inspector.get_table_names()
            
            new_tables = ['blocked_ips', 'system_settings', 'audit_logs', 'partners']
            for table_name in new_tables:
                if table_name in tables:
                    print(f"   ✅ Tabela '{table_name}' pronta")
                else:
                    print(f"   ❌ Tabela '{table_name}' não foi criada")
            
            # 4. Configura valores padrão do sistema
            print("\n4️⃣  Configurando sistema...")
            
            from app.models.system import set_setting
            
            # Modo manutenção desligado por padrão
            if not SystemSettings.query.filter_by(key='maintenance_mode').first():
                set_setting('maintenance_mode', 'false', 'Site em modo manutenção')
                print("   ✅ Modo manutenção configurado (desligado)")
            
            db.session.commit()
            
            # 5. Sumário
            print("\n" + "=" * 60)
            print("  ✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            print()
            print("📊 Estatísticas:")
            print(f"   • Total de usuários: {User.query.count()}")
            print(f"   • Administradores: {User.query.filter_by(role='admin').count()}")
            print(f"   • Parceiros: {User.query.filter_by(role='partner').count()}")
            print(f"   • Pendentes: {User.query.filter_by(status='pending').count()}")
            print(f"   • IPs bloqueados: {BlockedIP.query.count()}")
            print(f"   • Logs de auditoria: {AuditLog.query.count()}")
            print()
            print("🎉 Banco de dados atualizado e pronto para uso!")
            print()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print("\n" + "=" * 60)
            print("  ❌ ERRO NA MIGRAÇÃO!")
            print("=" * 60)
            print(f"\nErro: {str(e)}")
            print("\nDetalhes técnicos:")
            import traceback
            traceback.print_exc()
            print()
            return False


if __name__ == '__main__':
    print()
    print("⚠️  ATENÇÃO: Esta operação irá modificar o banco de dados.")
    print("   Certifique-se de ter um backup antes de continuar.")
    print()
    
    resposta = input("Deseja continuar? (s/N): ").strip().lower()
    
    if resposta == 's':
        success = migrate_database()
        sys.exit(0 if success else 1)
    else:
        print("\n❌ Migração cancelada pelo usuário.")
        sys.exit(0)
