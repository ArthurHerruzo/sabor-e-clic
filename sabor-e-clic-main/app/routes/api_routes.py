from flask import Blueprint
from app.controllers import api_controller

api_bp = Blueprint('api', __name__)

api_bp.route('/cardapio', methods=['GET'])(api_controller.listar_cardapio)
api_bp.route('/pedidos', methods=['POST'])(api_controller.criar_pedido)
api_bp.route('/pedidos/kds', methods=['GET'])(api_controller.obter_fila_kds)