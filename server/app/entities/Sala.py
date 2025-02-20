from ..extensions import db

class Sala(db.Model):
    numero = db.Column(db.Integer, primary_key = True)
    localizacao = db.Column(db.String(10), nullable = False)
    capacidade = db.Column(db.Integer, nullable = False)

    turmas = db.relationship('Turma', backref='sala', lazy=True)
