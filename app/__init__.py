from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.controllers.main_controller import main_bp
    app.register_blueprint(main_bp)

    from app.controllers.api_controller import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app