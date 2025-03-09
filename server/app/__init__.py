from flask import Flask
from .config import Config
from .extensions import db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:5173"])
    app.config.from_object(Config)

    # Inicializa
    db.init_app(app)

    # Importar modelos
    from .models import Usuario, Turma, Sala, professor_disciplina, Disciplina, Cargo, Calendario, Boletim, Aula, Aluno, aluno_turma

    # Registra rotas
    from .routes.sala_routes import sala_bp
    app.register_blueprint(sala_bp, url_prefix="/sala")

    from .routes.disciplina_routes import disciplina_bp
    app.register_blueprint(disciplina_bp, url_prefix="/disciplina")
    
    return app