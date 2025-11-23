"""
Database Migration Script - SIMPLIFIED
Adiciona novas colunas sem usar modelos ORM

Execute: python migrate_db_simple.py
"""
import sqlite3
import os

def migrate():
    """Migra banco de dados"""
    # Caminho do banco
    db_path = os.path.join('instance', 'database.db')
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return False
    
    print("=" * 60)
    print("  MIGRAÇÃO DO BANCO DE DADOS")
    print("=" * 60)
    print()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Adiciona colunas na tabela users
        print("1️⃣  Atualizando tabela 'users'...")
        
        columns = {
            'role': ("role", "VARCHAR(20) DEFAULT 'user' NOT NULL"),
            'status': ("status", "VARCHAR(20) DEFAULT 'active' NOT NULL"),
            'updated_at': ("updated_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
            'last_login': ("last_login", "DATETIME"),
            'full_name': ("full_name", "VARCHAR(200)"),
            'phone': ("phone", "VARCHAR(20)")
        }
        
        # Verifica quais colunas já existem
        cursor.execute("PRAGMA table_info(users)")
        existing = [row[1] for row in cursor.fetchall()]
        
        for col_name, (name, definition) in columns.items():
            if name not in existing:
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {name} {definition}")
                    print(f"   ✅ Coluna '{name}' adicionada")
                except Exception as e:
                    print(f"   ⚠️  '{name}': {str(e)}")
            else:
                print(f"   ⏭️  Coluna '{name}' já existe")
        
        conn.commit()
        
        # 2. Sincroniza roles
        print("\n2️⃣  Sincronizando roles...")
        cursor.execute("UPDATE users SET role = 'admin' WHERE is_admin = 1")
        print(f"   ✅ Roles sincronizados")
        conn.commit()
        
        # 3. Cria tabela blocked_ips
        print("\n3️⃣  Criando tabela 'blocked_ips'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blocked_ips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address VARCHAR(45) UNIQUE NOT NULL,
                reason VARCHAR(500),
                blocked_by INTEGER,
                blocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME,
                FOREIGN KEY (blocked_by) REFERENCES users(id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_blocked_ips_ip ON blocked_ips(ip_address)")
        print("   ✅ Tabela 'blocked_ips' criada")
        
        # 4. Cria tabela system_settings
        print("\n4️⃣  Criando tabela 'system_settings'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key VARCHAR(100) UNIQUE NOT NULL,
                value TEXT,
                description VARCHAR(500),
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_by INTEGER,
                FOREIGN KEY (updated_by) REFERENCES users(id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_system_settings_key ON system_settings(key)")
        
        # Insere configuração padrão
        cursor.execute("""
            INSERT OR IGNORE INTO system_settings (key, value, description) 
            VALUES ('maintenance_mode', 'false', 'Site em modo manutenção')
        """)
        print("   ✅ Tabela 'system_settings' criada")
        
        # 5. Cria tabela audit_logs
        print("\n5️⃣  Criando tabela 'audit_logs'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action VARCHAR(100) NOT NULL,
                target VARCHAR(200),
                details TEXT,
                ip_address VARCHAR(45),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs(user_id)")
        print("   ✅ Tabela 'audit_logs' criada")
        
        # 6. Cria tabela partners
        print("\n6️⃣  Criando tabela 'partners'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS partners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                partner_type VARCHAR(50) NOT NULL,
                business_name VARCHAR(200),
                description TEXT,
                address VARCHAR(500),
                document_number VARCHAR(50),
                license_number VARCHAR(100),
                verified BOOLEAN DEFAULT 0,
                verification_date DATETIME,
                verified_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (verified_by) REFERENCES users(id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_partners_user ON partners(user_id)")
        print("   ✅ Tabela 'partners' criada")
        
        conn.commit()
        
        # 7. Estatísticas
        print("\n" + "=" * 60)
        print("  ✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print()
        print("📊 Estatísticas:")
        
        cursor.execute("SELECT COUNT(*) FROM users")
        print(f"   • Total de usuários: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        print(f"   • Administradores: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'partner'")
        print(f"   • Parceiros: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'pending'")
        print(f"   • Pendentes: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM blocked_ips")
        print(f"   • IPs bloqueados: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM audit_logs")
        print(f"   • Logs de auditoria: {cursor.fetchone()[0]}")
        
        print()
        print("🎉 Banco de dados atualizado e pronto para uso!")
        print()
        
        return True
        
    except Exception as e:
        conn.rollback()
        print("\n" + "=" * 60)
        print("  ❌ ERRO NA MIGRAÇÃO!")
        print("=" * 60)
        print(f"\nErro: {str(e)}")
        import traceback
        traceback.print_exc()
        print()
        return False
    finally:
        conn.close()


if __name__ == '__main__':
    print()
    print("⚠️  ATENÇÃO: Esta operação irá modificar o banco de dados.")
    print()
    
    resposta = input("Deseja continuar? (s/N): ").strip().lower()
    
    if resposta == 's':
        success = migrate()
        exit(0 if success else 1)
    else:
        print("\n❌ Migração cancelada.")
        exit(0)
