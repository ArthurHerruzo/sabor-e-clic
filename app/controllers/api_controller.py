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
            SELECT
                p.id_pedido,
                p.id_cliente,
                u.nome AS nome_cliente,
                p.status_pedido,
                p.valor_total,
                ip.quantidade,
                i.nome AS nome_item
            FROM pedidos p
            INNER JOIN usuarios u
                ON p.id_cliente = u.id_usuario
            INNER JOIN itens_pedido ip
                ON p.id_pedido = ip.id_pedido
            INNER JOIN itens_cardapio i
                ON ip.id_item = i.id_item
            ORDER BY p.id_pedido DESC
        """).fetchall()

    @staticmethod
    def atualizar_status(id_pedido, novo_status):
        db = get_db()

        status_validos = [
            'AGUARDANDO',
            'PREPARO',
            'PRONTO',
            'FINALIZADO'
        ]

        if novo_status not in status_validos:
            return False

        pedido = db.execute("""
            SELECT id_pedido
            FROM pedidos
            WHERE id_pedido = ?
        """, (id_pedido,)).fetchone()

        if not pedido:
            return False

        db.execute("""
            UPDATE pedidos
            SET status_pedido = ?
            WHERE id_pedido = ?
        """, (novo_status, id_pedido))

        db.commit()
        return True