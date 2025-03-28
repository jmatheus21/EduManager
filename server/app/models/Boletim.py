from app.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY

class Boletim(db.Model):
    aluno_matricula = db.Column('aluno_matricula', db.String, db.ForeignKey('aluno.matricula', ondelete = 'CASCADE', onupdate = 'CASCADE'), primary_key=True)
    aula_id = db.Column('aula_id', db.Integer, db.ForeignKey('aula.id', ondelete = 'CASCADE', onupdate = 'CASCADE'), primary_key=True)
    notas = db.Column(ARRAY(db.Float), nullable=False)
    ausencias = db.Column(db.Integer, default=0)
    situacao = db.Column(db.CHAR(1), default="M") # M = matriculado, A = aprovado, R = reprovado

    aluno = db.relationship('Aluno', back_populates='boletins', cascade = 'all, delete')
    aula = db.relationship('Aula', back_populates='boletins', cascade = 'all, delete')
    
