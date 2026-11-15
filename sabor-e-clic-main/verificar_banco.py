import sqlite3

db = sqlite3.connect('database/sabor_clic.db')
db.row_factory = sqlite3.Row

produtos = db.execute("""
    SELECT * FROM itens_cardapio
""").fetchall()

for produto in produtos:
    print(dict(produto))

db.close()
