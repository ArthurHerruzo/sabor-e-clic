
from flask import Blueprint
from app.controllers import web_controller

web_bp = Blueprint('web', __name__)

web_bp.route('/cardapio')(web_controller.cardapio)
web_bp.route('/login', methods=['GET', 'POST'])(web_controller.login)
web_bp.route('/registro', methods=['GET', 'POST'])(web_controller.registro)
web_bp.route('/logout')(web_controller.logout)
