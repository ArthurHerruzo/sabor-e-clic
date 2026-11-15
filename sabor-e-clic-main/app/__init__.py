from flask import Flask
from app.database import close_db

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    app.secret_key = 'sabor_clic_secret_key_2026'
    app.teardown_appcontext(close_db)

    from app.controllers.main_controller import main_bp
    from app.routes.web_routes import web_bp
    from app.routes.api_routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app