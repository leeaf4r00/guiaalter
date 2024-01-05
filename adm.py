import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Defina a variável DATABASE_PATH em algum lugar, por exemplo, no início do seu script.
DATABASE_PATH = "data/database.db"


def get_database_connection():
    return sqlite3.connect(DATABASE_PATH)


def create_users_table():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                user_type INTEGER NOT NULL
            )
        """)
        connection.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if connection:
            connection.close()


def clear_database():
    result = messagebox.askquestion(
        "Aviso", "Tem certeza que deseja limpar o banco de dados? Isso excluirá todos os usuários.", icon='warning')
    if result == 'yes':
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM users")
            connection.commit()
            update_user_listbox()
            update_user_count_label()
            messagebox.showinfo("Sucesso", "Banco de dados limpo com sucesso!")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror(
                "Erro", "Não foi possível limpar o banco de dados.")
        finally:
            if connection:
                connection.close()


def count_users():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(id) FROM users")
        return cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return 0
    finally:
        if connection:
            connection.close()


def update_user_password(user_id, new_password):
    hashed_password = generate_password_hash(new_password)
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (hashed_password, user_id)
        )
        connection.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if connection:
            connection.close()


def get_all_users():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, user_type FROM users")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if connection:
            connection.close()


class User(UserMixin):
    def __init__(self, id, username, email, password, user_type):
        self.id = id
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.user_type = user_type

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
def create_user(username, hashed_password):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)', 
            (username, hashed_password))
        connection.commit()

def create_user_button():
    username = username_entry.get()
    password = password_entry.get()
    # Remova a linha user_type = user_type_var.get()
    hashed_password = generate_password_hash(password)
    if create_user(username, hashed_password):
        messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")


def update_user_count_label():
    count = count_users()
    user_count_label.config(text=f"Total de usuários cadastrados: {count}")


def update_user_listbox():
    users = get_all_users()
    user_listbox.delete(0, tk.END)
    for user in users:
        user_listbox.insert(
            tk.END, f"ID: {user[0]}, Nome de Usuário: {user[1]}, Nível de Permissão: {user[2]}")


def create_users_table():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                user_type INTEGER NOT NULL
            )
        """)
        connection.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if connection:
            connection.close()


def edit_user():
    selected_user = user_listbox.curselection()
    if selected_user:
        user_id = selected_user[0] + 1
        new_password = new_password_entry.get()
        if update_user_password(user_id, new_password):
            messagebox.showinfo(
                "Sucesso", "Senha do usuário atualizada com sucesso!")
            update_user_listbox()
        else:
            messagebox.showerror(
                "Erro", "Não foi possível atualizar a senha do usuário.")


def delete_user():
    selected_user = user_listbox.curselection()
    if selected_user:
        user_id = selected_user[0] + 1
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            connection.commit()
            update_user_listbox()
            update_user_count_label()
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Erro", "Não foi possível excluir o usuário.")
        finally:
            if connection:
                connection.close()


root = tk.Tk()
root.title("Sistema de Usuários")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

user_tab = ttk.Frame(notebook)
notebook.add(user_tab, text="Cadastro de Usuários")

username_label = ttk.Label(user_tab, text="Nome de usuário:")
username_label.pack()
username_entry = ttk.Entry(user_tab)
username_entry.pack()

password_label = ttk.Label(user_tab, text="Senha:")
password_label.pack()
password_entry = ttk.Entry(user_tab, show="*")
password_entry.pack()

user_type_label = ttk.Label(user_tab, text="Nível de permissão:")
user_type_label.pack()
user_type_var = tk.IntVar()
user_type_var.set(1)
admin_radio = ttk.Radiobutton(
    user_tab, text="Administrativo", variable=user_type_var, value=3)
admin_radio.pack()
partner_radio = ttk.Radiobutton(
    user_tab, text="Parceiros", variable=user_type_var, value=2)
partner_radio.pack()
user_radio = ttk.Radiobutton(
    user_tab, text="Usuário", variable=user_type_var, value=1)
user_radio.pack()

create_user_button = ttk.Button(
    user_tab, text="Criar Usuário", command=create_user_button)
create_user_button.pack()

list_tab = ttk.Frame(notebook)
notebook.add(list_tab, text="Lista de Usuários")

user_listbox = tk.Listbox(list_tab, selectmode=tk.SINGLE)
user_listbox.pack()

update_user_button = ttk.Button(
    list_tab, text="Atualizar Lista", command=update_user_listbox)
update_user_button.pack()

user_count_label = ttk.Label(list_tab, text="")
user_count_label.pack()

clear_database_button = ttk.Button(
    list_tab, text="Limpar Banco de Dados", command=clear_database)
clear_database_button.pack()

edit_tab = ttk.Frame(notebook)
notebook.add(edit_tab, text="Edição de Usuário")

user_id_label = ttk.Label(edit_tab, text="ID do Usuário:")
user_id_label.pack()
user_id_entry = ttk.Entry(edit_tab)
user_id_entry.pack()

new_password_label = ttk.Label(edit_tab, text="Nova Senha:")
new_password_label.pack()
new_password_entry = ttk.Entry(edit_tab, show="*")
new_password_entry.pack()

edit_user_button = ttk.Button(
    edit_tab, text="Editar Usuário", command=edit_user)
edit_user_button.pack()

delete_user_button = ttk.Button(
    edit_tab, text="Excluir Usuário", command=delete_user)
delete_user_button.pack()

update_user_listbox()
update_user_count_label()

root.mainloop()
