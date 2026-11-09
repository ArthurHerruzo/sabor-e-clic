from flask import Flask
from app.database import close_db

# Importa os Blueprints de rotas da API e das páginas Web
from app.routes.api_routes import api_bp
from app.routes.web_routes import web_bp

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'sabor_clic_secret_key_2026'

# Encerra a conexão com o SQLite ao finalizar cada requisição
app.teardown_appcontext(close_db)

# Registra as rotas da API com o prefixo /api (ex: /api/cardapio)
app.register_blueprint(api_bp, url_prefix='/api')

# Registra as rotas Web do site (ex: /, /login, /cardapio, /registro)
app.register_blueprint(web_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)