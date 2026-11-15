# Base de dados em memória
cardapio_db = [
    {"id": 1, "nome": "Hamburguer Artesanal", "preco": 32.50, "ativo": True},
    {"id": 2, "nome": "Batata Rústica", "preco": 18.00, "ativo": True}
]

pedidos_db = []

class CardapioModel:
    @staticmethod
    def listar_todos():
        return cardapio_db

    @staticmethod
    def adicionar(nome, preco):
        novo_item = {
            "id": len(cardapio_db) + 1,
            "nome": nome,
            "preco": float(preco),
            "ativo": True
        }
        cardapio_db.append(novo_item)
        return novo_item

class PedidoModel:
    @staticmethod
    def criar(cliente, itens, total):
        novo_pedido = {
            "id_pedido": len(pedidos_db) + 1,
            "cliente": cliente,
            "itens": itens,
            "status": "Aguardando",
            "total": total
        }
        pedidos_db.append(novo_pedido)
        return novo_pedido

    @staticmethod
    def obter_kds():
        return pedidos_db