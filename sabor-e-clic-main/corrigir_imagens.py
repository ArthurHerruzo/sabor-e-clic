
import sqlite3

banco = sqlite3.connect('database/sabor_clic.db')

imagens = {
    8: 'https://images.unsplash.com/photo-1639020715113-996f7f8f2999?w=700',

    7: 'https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=700',

    19: 'https://images.unsplash.com/photo-1702728109878-c61a98d80491?w=700',

    21: 'https://images.unsplash.com/photo-1507281549113-040fcfef650e?w=700'
}

try:
    for id_item, imagem in imagens.items():
        banco.execute("""
            UPDATE itens_cardapio
            SET imagem = ?
            WHERE id_item = ?
        """, (imagem, id_item))

    banco.commit()
    print("Imagens atualizadas com sucesso!")

except Exception as erro:
    banco.rollback()
    print("Erro:", erro)

finally:
    banco.close()
