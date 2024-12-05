from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///petshop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'minha_chave_secreta'

    # Inicializar o banco de dados com o app
    db.init_app(app)

    # Importar e registrar o blueprint das rotas
    from .routes import bp as veiculos_bp
    app.register_blueprint(veiculos_bp)

    return app
