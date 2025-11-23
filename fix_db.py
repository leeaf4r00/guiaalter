"""
Script de Migração e Correção do Banco de Dados
Verifica se as tabelas e colunas necessárias existem e as cria se necessário.
"""
from app import create_app, db
from sqlalchemy import text
import sqlite3
import os

def check_and_fix_database():
    app = create_app()
    
    db_path = os.path.join(app.instance_path, 'database.db')
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado em {db_path}")
        return

    print(f"🔧 Verificando banco de dados em: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Verificar tabela users
    print("Checking 'users' table...")
    cursor.execute("PRAGMA table_info(users)")
    columns = {row[1] for row in cursor.fetchall()}
    
    migrations = [
        ("role", "TEXT DEFAULT 'user'"),
        ("status", "TEXT DEFAULT 'active'"),
        ("is_admin", "BOOLEAN DEFAULT 0"),
        ("created_at", "DATETIME"),
        ("updated_at", "DATETIME"),
        ("last_login", "DATETIME"),
        ("full_name", "TEXT"),
        ("phone", "TEXT")
    ]
    
    for col_name, col_type in migrations:
        if col_name not in columns:
            print(f"  ➕ Adicionando coluna '{col_name}'...")
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            except Exception as e:
                print(f"  ⚠️ Erro ao adicionar {col_name}: {e}")
    
    # 2. Verificar se tabela partners existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='partners'")
    if not cursor.fetchone():
        print("  ➕ Criando tabela 'partners'...")
        cursor.execute("""
            CREATE TABLE partners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                business_name TEXT NOT NULL,
                partner_type TEXT NOT NULL,
                description TEXT,
                verified BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

    # 3. Verificar se tabela blocked_ips existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='blocked_ips'")
    if not cursor.fetchone():
        print("  ➕ Criando tabela 'blocked_ips'...")
        cursor.execute("""
            CREATE TABLE blocked_ips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT NOT NULL UNIQUE,
                reason TEXT,
                blocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME,
                blocked_by_id INTEGER,
                FOREIGN KEY(blocked_by_id) REFERENCES users(id)
            )
        """)

    # 4. Verificar se tabela audit_logs existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='audit_logs'")
    if not cursor.fetchone():
        print("  ➕ Criando tabela 'audit_logs'...")
        cursor.execute("""
            CREATE TABLE audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                target_type TEXT,
                target_id INTEGER,
                details TEXT,
                ip_address TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

    # 5. Verificar se tabela system_settings existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='system_settings'")
    if not cursor.fetchone():
        print("  ➕ Criando tabela 'system_settings'...")
        cursor.execute("""
            CREATE TABLE system_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                value TEXT,
                description TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

    conn.commit()
    conn.close()
    print("✅ Migração concluída com sucesso!")

if __name__ == "__main__":
    check_and_fix_database()
