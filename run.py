from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db, close_db

# Importa o Blueprint das rotas da API que criamos acima
from routes.api_routes import api_bp

app = Flask(_name_)
app.secret_key = 'sabor_clic_secret_key_2026'

# Garante que a conexão com o banco é fechada após cada requisição
app.teardown_appcontext(close_db)

# Registra o Blueprint das rotas da API com o prefixo api
app.register_blueprint(api_bp, url_prefix='api')

@app.route('')
def index()
    return render_template('index.html')

# (Demais rotas de login e logout continuam aqui...)

if _name_ == '_main_'
    app.run(debug=True, port=5000)