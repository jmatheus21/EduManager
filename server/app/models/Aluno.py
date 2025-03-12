from app.extensions import db

# Tabela de associação para o relacionamento Muitos para Muitos entre aluno e turma
aluno_turma = db.Table(
    'aluno_turma',
    db.Column('aluno_matricula', db.String(50), db.ForeignKey('aluno.matricula'), primary_key=True),
    db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'), primary_key=True)
)

class Aluno (db.Model):
    matricula = db.Column(db.String(50), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(50), nullable=True)
    endereco = db.Column(db.String(255), nullable=True)
    data_de_nascimento = db.Column(db.Date, nullable=False)

    boletins = db.relationship('Boletim', back_populates='aluno')