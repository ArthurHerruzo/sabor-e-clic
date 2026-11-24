from flask import Blueprint, jsonify, request, session
from app.models.api_model import CardapioModel, PedidoModel
from app.models.reserva_model import ReservaModel

api_bp = Blueprint('api', __name__)


@api_bp.route('/cardapio', methods=['GET'])
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


@api_bp.route('/pedidos', methods=['POST'])
def criar_pedido():
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
    produtos = {item["id_item"]: item for item in cardapio}

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


@api_bp.route('/pedidos/kds', methods=['GET'])
def obter_fila_kds():
    if 'id_usuario' not in session:
        return jsonify({"erro": "Faça login para acessar os pedidos."}), 401

    if session.get('nivel_acesso') not in ['ADMIN', 'COZINHEIRO']:
        return jsonify({"erro": "Você não tem permissão para acessar os pedidos."}), 403

    pedidos = PedidoModel.obter_fila_kds()
    lista = []

    for pedido in pedidos:
        lista.append({
            "id_pedido": pedido["id_pedido"],
            "id_cliente": pedido["id_cliente"],
            "nome_cliente": pedido["nome_cliente"],
            "status": pedido["status_pedido"],
            "total": float(pedido["valor_total"]),
            "nome_item": pedido["nome_item"],
            "quantidade": pedido["quantidade"]
        })

    return jsonify(lista), 200


@api_bp.route('/pedidos/<int:id_pedido>/status', methods=['PUT'])
def atualizar_status_pedido(id_pedido):
    if 'id_usuario' not in session:
        return jsonify({"erro": "Faça login para continuar."}), 401

    if session.get('nivel_acesso') not in ['ADMIN', 'COZINHEIRO']:
        return jsonify({"erro": "Você não tem permissão."}), 403

    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({"erro": "Dados inválidos."}), 400

    novo_status = dados.get('status')
    sucesso = PedidoModel.atualizar_status(id_pedido, novo_status)

    if not sucesso:
        return jsonify({"erro": "Pedido ou status inválido."}), 400

    return jsonify({"mensagem": "Status atualizado com sucesso!"}), 200


@api_bp.route('/reservas/kds', methods=['GET'])
def listar_reservas_kds():
    if 'id_usuario' not in session:
        return jsonify({"erro": "Faça login para continuar."}), 401

    if session.get('nivel_acesso') not in ['ADMIN', 'COZINHEIRO']:
        return jsonify({"erro": "Você não tem permissão."}), 403

    reservas = ReservaModel.listar_reservas()
    lista = []

    for reserva in reservas:
        lista.append({
            "id_reserva": reserva["id_reserva"],
            "nome_cliente": reserva["nome_cliente"],
            "numero_mesa": reserva["numero_mesa"],
            "capacidade": reserva["capacidade"],
            "quantidade_pessoas": reserva["quantidade_pessoas"],
            "inicio": reserva["data_hora_inicio"],
            "fim": reserva["data_hora_fim"],
            "status": reserva["status"]
        })

    return jsonify(lista), 200