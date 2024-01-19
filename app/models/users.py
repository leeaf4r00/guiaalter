from werkzeug.security import generate_password_hash, check_password_hash

# Simulando um banco de dados temporário como exemplo


class UserDatabase:
    def __init__(self):
        self.users = {}
        self.user_id_counter = 1

    def create_user(self, username, password, is_admin=False):
        user_id = self.user_id_counter
        self.users[user_id] = {
            'id': user_id,
            'username': username,
            'password': password,
            'is_admin': is_admin
        }
        self.user_id_counter += 1
        return user_id

    def get_user_by_id(self, user_id):
        return self.users.get(user_id)

    def get_user_by_username(self, username):
        for user in self.users.values():
            if user['username'] == username:
                return user
        return None

    def count_admin_users(self):
        count = 0
        for user in self.users.values():
            if user['is_admin']:
                count += 1
        return count

    def count_users(self):
        return len(self.users)


# Exemplo de uso
db = UserDatabase()

# Função para criar um novo usuário


def create_user(username, password, is_admin=False):
    hashed_password = generate_password_hash(password)
    return db.create_user(username, hashed_password, is_admin)

# Função para verificar se as credenciais do usuário são válidas


def validate_login(username, password):
    user = db.get_user_by_username(username)
    if user and check_password_hash(user['password'], password):
        return user
    return None

# Função para obter todos os usuários


def get_all_users():
    return list(db.users.values())
