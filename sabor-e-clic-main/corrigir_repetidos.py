import sqlite3

banco = sqlite3.connect('database/sabor_clic.db')

try:
    banco.execute("""
        UPDATE itens_cardapio
        SET status_ativo = 0
        WHERE id_item IN (4, 5, 6, 23, 24, 25, 26, 27, 28)
    """)

    banco.commit()

    print("Produtos duplicados desativados com sucesso!")

    produtos = banco.execute("""
        SELECT id_item, nome
        FROM itens_cardapio
        WHERE status_ativo = 1
        ORDER BY id_item
    """).fetchall()

    print("\nProdutos ativos:")

    for produto in produtos:
        print(produto)

except Exception as erro:
    banco.rollback()
    print("Erro:", erro)

finally:
    banco.close()