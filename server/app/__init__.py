from flask import Flask
from .config import Config
from .extensions import db
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider
from datetime import date, datetime

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.strftime('%Y-%m-%d')
        return super().default(o)

def create_app(config_class=Config):
    app = Flask(__name__)
    
    # Configura o JSON provider customizado
    app.json_provider_class = CustomJSONProvider
    app.json = app.json_provider_class(app)
    
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
    app.config.from_object(config_class)

    # Inicializa o banco de dados
    db.init_app(app)

    # Importar modelos
    from .models import Usuario, Turma, Sala, professor_disciplina, Disciplina, Cargo, Calendario, Boletim, Aula, Aluno, aluno_turma

    # Registra rotas
    from .routes.sala_routes import sala_bp
    from .routes.calendario_routes import calendario_bp
    from .routes.usuario_routes import usuario_bp
    from .routes.disciplina_routes import disciplina_bp
    from .routes.turma_routes import turma_bp
    from .routes.aluno_routes import aluno_bp
    from .routes.aula_routes import aula_bp
    from .routes.login_routes import auth_bp
    app.register_blueprint(sala_bp, url_prefix="/sala")
    app.register_blueprint(calendario_bp, url_prefix="/calendario")
    app.register_blueprint(usuario_bp, url_prefix="/usuario")
    app.register_blueprint(disciplina_bp, url_prefix="/disciplina")
    app.register_blueprint(turma_bp, url_prefix="/turma")
    app.register_blueprint(aluno_bp, url_prefix="/aluno")
    app.register_blueprint(aula_bp, url_prefix="/aula")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    return app
