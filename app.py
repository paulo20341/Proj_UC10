from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        print("Criando tabelas no banco de dados...")
        db.create_all()  # Cria as tabelas no banco de dados
        print("Tabelas criadas!")
    app.run(host='0.0.0.0', port=5000, debug=True)
