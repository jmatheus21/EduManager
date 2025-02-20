from app import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Cria o banco de dados e as tabelas (executar apenas uma vez)
        from app.extensions import db
        db.create_all()
    
    app.run(debug=True)