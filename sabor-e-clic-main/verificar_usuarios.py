import sqlite3

banco = sqlite3.connect('database/sabor_clic.db')
banco.row_factory = sqlite3.Row

usuarios = banco.execute("""
    SELECT id_usuario, nome, email, nivel_acesso
    FROM usuarios
""").fetchall()

for usuario in usuarios:
    print(dict(usuario))

banco.close()