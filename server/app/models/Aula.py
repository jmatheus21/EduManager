from app.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY

class Aula (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    dias_da_semana = db.Column(ARRAY(db.String(3)), nullable=False)
    professor_cpf = db.Column(db.String(20), db.ForeignKey('usuario.cpf', ondelete = 'CASCADE', onupdate = 'CASCADE'), nullable=False)
    disciplina_codigo = db.Column(db.String(10), db.ForeignKey('disciplina.codigo', ondelete = 'CASCADE', onupdate = 'CASCADE'), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id', ondelete = 'CASCADE', onupdate = 'CASCADE'), nullable=False)

    boletins = db.relationship('Boletim', back_populates='aula', cascade = 'all, delete')