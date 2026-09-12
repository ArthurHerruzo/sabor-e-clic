from flask import Blueprint, jsonify, request
from app.models.cardapio_model import CardapioModel, PedidoModel

# A variável precisa se chamar exatamente api_bp
api_bp = Blueprint("api", __name__)


@api_bp.route("/cardapio", methods=["GET"])
def listar_cardapio():
    itens = CardapioModel.listar_todos()
    return jsonify(itens), 200


@api_bp.route("/cardapio", methods=["POST"])
def adicionar_item():
    dados = request.get_json()

    if not dados or "nome" not in dados or "preco" not in dados:
        return jsonify({
            "erro": "Dados incompletos para cadastro"
        }), 400

    novo_item = CardapioModel.adicionar(
        dados["nome"],
        dados["preco"]
    )

    return jsonify(novo_item), 201


@api_bp.route("/pedidos", methods=["POST"])
def criar_pedido():
    dados = request.get_json()

    if not dados or "itens" not in dados:
        return jsonify({
            "erro": "Lista de itens obrigatoria"
        }), 400

    cliente = dados.get("cliente", "Cliente Anônimo")

    novo_pedido = PedidoModel.criar(
        cliente,
        dados["itens"],
        dados.get("total", 0.0)
    )

    return jsonify(novo_pedido), 201


@api_bp.route("/pedidos/kds", methods=["GET"])
def obter_fila_kds():
    fila = PedidoModel.obter_kds()
    return jsonify(fila), 200
