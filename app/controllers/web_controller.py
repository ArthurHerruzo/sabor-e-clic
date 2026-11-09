from flask import render_template, request, redirect, url_for, session, flash
from app.models.usuario_model import UsuarioModel

def home():
    return render_template('home.html')

def cardapio():
    if 'id_usuario' not in session:
        flash('Você precisa fazer login para acessar o cardápio.', 'erro')
        return redirect(url_for('web.login'))
    return render_template('cardapio.html')

def login():
    if 'id_usuario' in session:
        flash('Você já está logado no sistema.', 'info')
        return redirect(url_for('web.cardapio'))

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = UsuarioModel.buscar_por_email(email)
        
        if usuario and usuario['senha_hash'] == senha:
            session['id_usuario'] = usuario['id_usuario']
            session['nome'] = usuario['nome']
            session['nivel_acesso'] = usuario['nivel_acesso']
            flash('Login realizado com sucesso!', 'sucesso')
            return redirect(url_for('web.cardapio'))
        else:
            flash('E-mail ou senha incorretos.', 'erro')
            
    return render_template('login.html')

def registro():
    if 'id_usuario' in session:
        flash('Você já possui uma conta e está logado.', 'info')
        return redirect(url_for('web.cardapio'))

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        if UsuarioModel.buscar_por_email(email):
            flash('Este e-mail já está cadastrado.', 'erro')
        else:
            UsuarioModel.criar(nome, email, senha)
            flash('Cadastro realizado com sucesso! Faça o login.', 'sucesso')
            return redirect(url_for('web.login'))
            
    return render_template('registro.html')

def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('web.login'))