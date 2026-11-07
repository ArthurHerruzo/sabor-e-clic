from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db, close_db
from routes.api_routes import api_bp

app = Flask(_name_)
app.secret_key = 'sabor_clic_secret_key_2026'

# Encerra conexão com o SQLite ao finalizar requisição
app.teardown_appcontext(close_db)

# Registra as rotas da API com o prefixo /api
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        db = get_db()
        usuario = db.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        
        if usuario and usuario['senha_hash'] == senha:
            session['id_usuario'] = usuario['id_usuario']
            session['nome'] = usuario['nome']
            session['nivel_acesso'] = usuario['nivel_acesso']
            
            flash('Login realizado com sucesso!', 'sucesso')
            return redirect(url_for('index'))
        else:
            flash('E-mail ou senha incorretos.', 'erro')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))

if _name_ == '_main_':
    app.run(debug=True, port=5000)