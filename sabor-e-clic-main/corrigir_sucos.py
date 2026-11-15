import sqlite3

banco = sqlite3.connect('database/sabor_clic.db')

banco.execute("""
    UPDATE itens_cardapio
    SET status_ativo = 0
    WHERE id_item = 20
""")

banco.commit()

print("Suco Natural de Laranja desativado!")

banco.close()