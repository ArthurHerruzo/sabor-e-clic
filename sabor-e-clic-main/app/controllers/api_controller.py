from flask import jsonify, request, session

from app.models.api_model import CardapioModel, PedidoModel


def listar_cardapio():

    itens = CardapioModel.listar_ativos()

    lista = []

    for item in itens:

        lista.append({
            "id": item["id_item"],
            "nome": item["nome"],
            "descricao": item["descricao"],
            "preco": float(item["preco"]),
            "categoria": item["categoria"],
            "imagem": item["imagem"],
            "ativo": bool(item["status_ativo"])
        })

    return jsonify(lista), 200


def criar_pedido():

    # Verifica se o cliente está logado
    if 'id_usuario' not in session:
        return jsonify({
            "erro": "Faça login para realizar o pedido."
        }), 401

    dados = request.get_json(silent=True)

    if not dados or not isinstance(dados.get('itens'), list) or not dados['itens']:
        return jsonify({
            "erro": "Adicione produtos ao carrinho."
        }), 400

    cardapio = CardapioModel.listar_ativos()

    produtos = {
        item["id_item"]: item
        for item in cardapio
    }

    itens_pedido = []
    valor_total = 0

    for item in dados['itens']:

        try:
            id_item = int(item['id'])
            quantidade = int(item['quantidade'])

        except (KeyError, TypeError, ValueError):
            return jsonify({
                "erro": "Produto ou quantidade inválida."
            }), 400

        if quantidade < 1 or id_item not in produtos:
            return jsonify({
                "erro": "Produto indisponível."
            }), 400

        produto = produtos[id_item]

        valor_total += float(produto["preco"]) * quantidade

        itens_pedido.append({
            "id": id_item,
            "quantidade": quantidade
        })

    id_pedido = PedidoModel.criar_pedido(
        session['id_usuario'],
        round(valor_total, 2),
        itens_pedido
    )

    return jsonify({
        "mensagem": "Pedido realizado com sucesso!",
        "id_pedido": id_pedido,
        "total": round(valor_total, 2),
        "status": "AGUARDANDO"
    }), 201


def obter_fila_kds():

    pedidos = PedidoModel.obter_fila_kds()

    lista = []

    for pedido in pedidos:

        lista.append({
            "id_pedido": pedido["id_pedido"],
            "id_cliente": pedido["id_cliente"],
            "status": pedido["status_pedido"],
            "total": float(pedido["valor_total"])
        })

    return jsonify(lista), 200
