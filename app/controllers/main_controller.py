from flask import Blueprint, render_template, session, redirect, url_for, flash

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('home.html')


@main_bp.route('/kds')
def kds():
    if 'id_usuario' not in session:
        flash('Faça login para acessar o painel da cozinha.', 'erro')
        return redirect(url_for('web.login'))

    if session.get('nivel_acesso') not in ['ADMIN', 'COZINHEIRO']:
        flash('Você não tem permissão para acessar o painel da cozinha.', 'erro')
        return redirect(url_for('web.cardapio'))

    return render_template('kds.html')