import os
from flask import Flask
from app.controllers.main_controller import main_bp
from app.controllers.web_controller import web_bp
from app.controllers.api_controller import api_bp


def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    # Necessário para usar 'session' e 'flash' no Flask
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY',
        'chave-secreta-sabor-e-clic-dev'
    )

    # Se o seu app/database.py tiver uma função init_app(app), descomente abaixo:
    # from app.database import init_app
    # init_app(app)

    # Registro dos Blueprints vindos dos Controllers (padrão MVC)
    app.register_blueprint(main_bp)
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app