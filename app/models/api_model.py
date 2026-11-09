from app.database import get_db

class CardapioModel:
    @staticmethod
    def listar_ativos():
        db = get_db()
        cursor = db.execute('SELECT id_item, nome, descricao, preco, status_ativo FROM itens_cardapio WHERE status_ativo = 1')
        return cursor.fetchall()

class PedidoModel:
    @staticmethod
    def criar_pedido(id_cliente, valor_total, itens):
        db = get_db()
        # Insere o pedido principal
        cursor = db.execute(
            'INSERT INTO pedidos (id_cliente, status_pedido, valor_total) VALUES (?, ?, ?)',
            (id_cliente, 'AGUARDANDO', valor_total)
        )
        id_pedido_criado = cursor.lastrowid
        
        # Insere os itens vinculados ao pedido
        for item in itens:
            db.execute(
                'INSERT INTO itens_pedido (id_pedido, id_item, quantidade) VALUES (?, ?, ?)',
                (id_pedido_criado, item['id'], item.get('quantidade', 1))
            )
        db.commit()
        return id_pedido_criado

    @staticmethod
    def obter_fila_kds():
        db = get_db()
        cursor = db.execute('SELECT id_pedido, id_cliente, status_pedido, valor_total FROM pedidos')
        return cursor.fetchall()