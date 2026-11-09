from flask import jsonify, request
from app.models.api_model import CardapioModel, PedidoModel

def listar_cardapio():
    itens = CardapioModel.listar_ativos()
    lista_pratos = []
    
    for item in itens:
        lista_pratos.append({
            "id": item["id_item"],
            "nome": item["nome"],
            "descricao": item["descricao"],
            "preco": item["preco"],
            "ativo": bool(item["status_ativo"])
        })
        
    return jsonify(lista_pratos), 200

def criar_pedido():
    dados = request.get_json()
    
    if not dados or 'itens' not in dados:
        return jsonify({"erro": "Lista de itens obrigatória"}), 400
        
    id_cliente = dados.get("id_cliente", 1)
    valor_total = dados.get("total", 0.0)
    
    id_pedido = PedidoModel.criar_pedido(id_cliente, valor_total, dados['itens'])
    
    return jsonify({
        "mensagem": "Pedido criado com sucesso!",
        "id_pedido": id_pedido,
        "status": "AGUARDANDO",
        "total": valor_total
    }), 201

def obter_fila_kds():
    pedidos = PedidoModel.obter_fila_kds()
    lista_pedidos = []
    
    for p in pedidos:
        lista_pedidos.append({
            "id_pedido": p["id_pedido"],
            "id_cliente": p["id_cliente"],
            "status": p["status_pedido"],
            "total": p["valor_total"]
        })
        
    return jsonify(lista_pedidos), 200