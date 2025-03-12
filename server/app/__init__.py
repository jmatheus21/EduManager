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

def create_app():
    app = Flask(__name__)
    
    # Configura o JSON provider customizado
    app.json_provider_class = CustomJSONProvider
    app.json = app.json_provider_class(app)
    
    CORS(app, origins=["http://localhost:5173"])
    app.config.from_object(Config)

    # Inicializa o banco de dados
    db.init_app(app)

    # Importar modelos
    from .models import Usuario, Turma, Sala, professor_disciplina, Disciplina, Cargo, Calendario, Boletim, Aula, Aluno, aluno_turma

    # Registra rotas
    from .routes.sala_routes import sala_bp
    from .routes.usuario_routes import usuario_bp
    app.register_blueprint(sala_bp, url_prefix="/sala")
    app.register_blueprint(usuario_bp, url_prefix="/usuario")

    return app
