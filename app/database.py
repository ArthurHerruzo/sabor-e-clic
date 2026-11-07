import sqlite3
from flask import g

DATABASE = 'database/sabor_clic.db' # Ou o caminho relativo para o banco SQLite

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row # Permite acessar as colunas pelo nome
    return db

def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()