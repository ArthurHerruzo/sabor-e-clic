
from app.database import get_db


class CardapioModel:

    @staticmethod
    def listar_ativos():
        db = get_db()

        cursor = db.execute("""
            SELECT id_item, nome, descricao, preco,
                   status_ativo, categoria, imagem
            FROM itens_cardapio
            WHERE status_ativo = 1
            ORDER BY categoria, nome
        """)

        return cursor.fetchall()


class PedidoModel:

    @staticmethod
    def criar_pedido(id_cliente, valor_total, itens):
        db = get_db()

        try:
            cursor = db.execute("""
                INSERT INTO pedidos
                (id_cliente, status_pedido, valor_total)
                VALUES (?, ?, ?)
            """, (id_cliente, 'AGUARDANDO', valor_total))

            id_pedido = cursor.lastrowid

            for item in itens:
                db.execute("""
                    INSERT INTO itens_pedido
                    (id_pedido, id_item, quantidade)
                    VALUES (?, ?, ?)
                """, (
                    id_pedido,
                    item['id'],
                    item['quantidade']
                ))

            db.commit()

            return id_pedido

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def obter_fila_kds():
        db = get_db()

        return db.execute("""
            SELECT id_pedido, id_cliente,
                   status_pedido, valor_total
            FROM pedidos
            ORDER BY id_pedido DESC
        """).fetchall()
