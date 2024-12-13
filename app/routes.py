from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from app.models import Animal, Reserva, Cliente, User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from apimercadopago import gerar_link_pagamento
import os
import uuid
from werkzeug.utils import secure_filename

bp = Blueprint('clientes', __name__)

# Rota inicial
@bp.route('/')
def index():
    link_pagamento = gerar_link_pagamento()
    return render_template('index.html', link_pagamento=link_pagamento)

@bp.route('/update-profile-pic', methods=['POST'])
def update_profile_pic():
    if 'profile_pic' not in request.files:
        flash('Nenhum arquivo selecionado.', 'error')
        return redirect(url_for('clientes.index'))  # Alterado para 'clientes.index'
    
    file = request.files['profile_pic']
    if file.filename == '':
        flash('Nenhum arquivo foi escolhido.', 'error')
        return redirect(url_for('clientes.index'))  # Alterado para 'clientes.index'
    
    if file:
        # Gera um nome único para o arquivo
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Define o caminho para salvar a imagem na pasta 'uploads'
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(filepath)  # Salva o arquivo com um nome único
        flash('Foto de perfil atualizada com sucesso!', 'success')
        return redirect(url_for('clientes.index'))  # Alterado para 'clientes.index'


# Registro de usuários
@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form['user']
        senha = request.form['senha']
        cpf = request.form['cpf']

        # Verifica se o usuário ou o CPF já existe no banco de dados
        if User.query.filter_by(Usuario=user).first():
            flash('Este nome de usuário já está em uso. Por favor, escolha outro.', 'danger')
            return redirect(url_for('clientes.register'))

        if User.query.filter_by(CPF=cpf).first():
            flash('Este CPF já está cadastrado. Por favor, verifique suas informações.', 'danger')
            return redirect(url_for('clientes.register'))

        # Criar um novo usuário e armazenar a senha com hash
        novo_usuario = User(Usuario=user, senha=generate_password_hash(senha), CPF=cpf)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Usuário registrado com sucesso.', 'success')
        return redirect(url_for('clientes.login'))

    return render_template('register.html')

# Login de usuários
@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        senha = request.form['senha']

        # Verifica se o usuário existe no banco de dados
        usuario = User.query.filter_by(Usuario=user).first()

        # Validar senha usando hashing
        if usuario and check_password_hash(usuario.senha, senha):
            session['user_id'] = usuario.id
            session['username'] = usuario.Usuario

            flash('Login realizado com sucesso.', 'success')
            return redirect(url_for('clientes.index'))  # Alterado para 'clientes.index'
        else:
            flash('Nome de usuário ou senha incorretos.', 'danger')

    return render_template('login.html')

# Logout de usuários
@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Você foi desconectado com sucesso.', 'success')
    return redirect(url_for('clientes.login'))

# Logout de usuários
@bp.route('/contato')
def contato():
    flash('Pagina contato carregado com sucesso.')
    return render_template("contato.html", contato=contato)

# Rota para agendar consulta (somente para usuários logados)
@bp.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if not session.get('username'):
        flash('Você precisa fazer login para acessar essa página.', 'danger')
        return redirect(url_for('clientes.login'))

    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        animal_id = request.form['animal_id']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        servico = request.form['servico']

        try:
            nova_reserva = Reserva(
                cliente_id=cliente_id,
                animal_id=animal_id,
                data_inicio=datetime.strptime(data_inicio, '%Y-%m-%dT%H:%M'),
                data_fim=datetime.strptime(data_fim, '%Y-%m-%dT%H:%M'),
                servico=servico
            )

            db.session.add(nova_reserva)
            db.session.commit()

            flash('Reserva agendada com sucesso!', 'success')
            return redirect(url_for('clientes.agendar'))  # Alterado para 'clientes.agendar'
        except Exception as e:
            flash(f'Ocorreu um erro ao agendar a reserva: {str(e)}', 'danger')

    clientes = Cliente.query.all()
    animais = Animal.query.all()
    return render_template('agendamento.html', clientes=clientes, animais=animais)

@bp.route('/cadastrar_animal', methods=['GET', 'POST'])
def cadastrar_animal():
    if not session.get('username'):
        flash('Você precisa fazer login para acessar essa página.', 'danger')
        return redirect(url_for('clientes.login'))

    if request.method == 'POST':
        resposta = request.form.get('resposta')
        if resposta != 'belinha':  # Resposta para confirmar a ação
            flash('Resposta incorreta. Você não tem permissão para cadastrar animais.', 'danger')
            return redirect(url_for('clientes.cadastrar_animal'))  # Alterado para 'clientes.cadastrar_animal'

        # Dados do animal
        nome = request.form['nome']
        especie = request.form['especie']
        raca = request.form['raca']
        idade = request.form['idade']
        cliente_id = request.form['cliente_id']

        novo_animal = Animal(nome=nome, especie=especie, raca=raca, idade=idade, cliente_id=cliente_id)
        
        try:
            db.session.add(novo_animal)
            db.session.commit()
            flash('Animal cadastrado com sucesso.', 'success')
            return redirect(url_for('animais.listar_animais'))  # Certifique-se de que esta rota está correta
        except Exception as e:
            flash(f'Ocorreu um erro ao cadastrar o animal: {str(e)}', 'danger')

    clientes = Cliente.query.all()
    return render_template('cadastrar_animal.html', clientes=clientes)
