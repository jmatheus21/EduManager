from app.extensions import db

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    ano = db.Column(db.Integer, nullable = False)
    serie = db.Column(db.CHAR(1), nullable = False)
    nivel_ensino = db.Column(db.String(30), nullable = False)
    turno = db.Column(db.CHAR(1), nullable = False)
    status = db.Column(db.CHAR(1), nullable = False, default='A')

    sala_numero = db.Column(db.Integer, db.ForeignKey('sala.numero', ondelete = 'SET NULL', onupdate = 'CASCADE'), nullable = True)
    calendario_ano_letivo = db.Column(db.Integer, db.ForeignKey('calendario.ano_letivo', ondelete = 'CASCADE', onupdate = 'CASCADE'), nullable = False)

    aulas = db.relationship('Aula', backref='turma', lazy=True, cascade='all, delete-orphan')
