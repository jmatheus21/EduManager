from app.extensions import db

# Tabela de associação para o relacionamento Muitos para Muitos entre professor e disciplina
professor_disciplina = db.Table(
    'professor_disciplina',
    db.Column('usuario_cpf', db.String(20), db.ForeignKey('usuario.cpf'), primary_key=True),
    db.Column('disciplina_codigo', db.String(10), db.ForeignKey('disciplina.codigo'), primary_key=True)
)

class Usuario(db.Model):
    cpf = db.Column(db.String(20), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(50), nullable=True)
    endereco = db.Column(db.String(255), nullable=True)
    horario_de_trabalho = db.Column(db.String(20), nullable=False)
    data_de_nascimento = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    formacao = db.Column(db.String(255), nullable=True)
    escolaridade = db.Column(db.String(255), nullable=True)
    habilidades = db.Column(db.String(255), nullable=True)

    aulas = db.relationship('Aula', backref='professor', lazy=True)
    cargos = db.relationship('Cargo', backref='usuario', lazy=True)

    disciplinas = db.relationship(
        'Disciplina',
        secondary=professor_disciplina,
        backref=db.backref('professores', lazy=True),
        lazy=True
    )