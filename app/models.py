from app import db
from datetime import datetime

# Modelo para Clientes
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)

    # Relacionamento com Animais e Reservas
    animais = db.relationship('Animal', backref='cliente', lazy=True)
    reservas = db.relationship('Reserva', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nome}>'

# Modelo para Animais
class Animal(db.Model):
    __tablename__ = 'animais'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)  # Ex: cachorro, gato
    raca = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)

    # Relacionamento com Reservas
    reservas = db.relationship('Reserva', backref='animal', lazy=True)

    def __repr__(self):
        return f'<Animal {self.nome}>'

# Modelo para Reservas de serviços
class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime, nullable=False)
    servico = db.Column(db.String(255), nullable=False)  # Ex: banho, tosquia
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animais.id'), nullable=False)

    def __repr__(self):
        return f'<Reserva {self.servico} para {self.animal.nome} em {self.data_inicio}>'

# Modelo para Usuários (autenticação)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    Usuario = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)  # Armazenar o hash da senha
    CPF = db.Column(db.String(11), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.Usuario}>'
