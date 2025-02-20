from flask import Flask
from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa
    db.init_app(app)

    # Importar modelos
    from .entities import Usuario, Turma, Sala, professor_ensina, Disciplina, Cargo, Calendario, Boletim, Aula, Aluno, aluno_participa

    # Registra rotas
    # from .routes import init_routes
    # init_routes(app)

    return app