from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.usuario_model import UsuarioModel
from app.models.reserva_model import ReservaModel

web_bp = Blueprint('web', __name__)


@web_bp.route('/cardapio')
def cardapio():
    if 'id_usuario' not in session:
        flash('Você precisa fazer login para acessar o cardápio.', 'erro')
        return redirect(url_for('web.login'))

    return render_template('cardapio.html')


@web_bp.route('/login', methods=['GET', 'POST'])
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

        flash('E-mail ou senha incorretos.', 'erro')

    return render_template('login.html')


@web_bp.route('/registro', methods=['GET', 'POST'])
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


@web_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('web.login'))


@web_bp.route('/reservas', methods=['GET', 'POST'])
def reservas():
    if 'id_usuario' not in session:
        flash('Faça login para reservar uma mesa.', 'erro')
        return redirect(url_for('web.login'))

    mesas = []

    if request.method == 'POST':
        inicio = request.form.get('inicio')
        fim = request.form.get('fim')
        quantidade = request.form.get('quantidade_pessoas')

        try:
            inicio_data = datetime.strptime(inicio, '%Y-%m-%dT%H:%M')
            fim_data = datetime.strptime(fim, '%Y-%m-%dT%H:%M')
            quantidade = int(quantidade)

            if inicio_data <= datetime.now():
                flash('Escolha uma data e horário futuros.', 'erro')

            elif fim_data <= inicio_data:
                flash('O horário de término deve ser posterior ao início.', 'erro')

            elif quantidade < 1 or quantidade > 6:
                flash('A quantidade de pessoas deve ser entre 1 e 6.', 'erro')

            else:
                mesas = ReservaModel.listar_mesas_disponiveis(
                    inicio, fim, quantidade
                )

                if not mesas:
                    flash('Não há mesas disponíveis nesse horário.', 'erro')

        except (ValueError, TypeError):
            flash('Preencha os dados da reserva corretamente.', 'erro')

    return render_template('reservas.html', mesas=mesas)


@web_bp.route('/reservas/criar', methods=['POST'])
def criar_reserva():
    if 'id_usuario' not in session:
        flash('Faça login para reservar uma mesa.', 'erro')
        return redirect(url_for('web.login'))

    inicio = request.form.get('inicio')
    fim = request.form.get('fim')

    try:
        quantidade = int(request.form.get('quantidade_pessoas'))
        id_mesa = int(request.form.get('id_mesa'))

        inicio_data = datetime.strptime(inicio, '%Y-%m-%dT%H:%M')
        fim_data = datetime.strptime(fim, '%Y-%m-%dT%H:%M')

        if inicio_data <= datetime.now():
            flash('Escolha uma data e horário futuros.', 'erro')

        elif fim_data <= inicio_data:
            flash('O horário de término deve ser posterior ao início.', 'erro')

        elif quantidade < 1 or quantidade > 6:
            flash('Quantidade de pessoas inválida.', 'erro')

        else:
            sucesso = ReservaModel.criar_reserva(
                session['id_usuario'],
                id_mesa,
                quantidade,
                inicio,
                fim
            )

            if sucesso:
                flash('Reserva realizada com sucesso!', 'sucesso')
                return redirect(url_for('web.reservas'))

            flash('Essa mesa não está mais disponível.', 'erro')

    except (ValueError, TypeError):
        flash('Dados da reserva inválidos.', 'erro')

    return redirect(url_for('web.reservas'))