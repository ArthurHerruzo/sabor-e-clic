from app.database import get_db

class UsuarioModel:
    @staticmethod
    def buscar_por_email(email):
        db = get_db()
        return db.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()

    @staticmethod
    def criar(nome, email, senha):
        db = get_db()
        db.execute(
            'INSERT INTO usuarios (nome, email, senha_hash, nivel_acesso) VALUES (?, ?, ?, ?)',
            (nome, email, senha, 'CLIENTE')
        )
        db.commit()