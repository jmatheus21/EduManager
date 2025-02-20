from ..extensions import db
from sqlalchemy.dialects.postgresql import ARRAY

class Boletim:
    notas = db.Column(ARRAY(db.Float), nullable=False)
    ausencias = db.Column(db.Integer, default=0)
    situacao = db.Column(db.CHAR(1), default="M") # M = matriculado, A = aprovado, R = reprovado
    
    aluno_matricula = db.Column('aluno_matricula', db.Integer, db.ForeignKey('aluno.matricula'), primary_key=True)
    aula_id = db.Column('aula_id', db.Integer, db.ForeignKey('aula.id'), primary_key=True)

    aluno = db.relationship('Aluno', backref="boletins")
    aula = db.relationship('Aula', backref="boletins")
    