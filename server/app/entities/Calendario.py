from ..extensions import db

class Calendario(db.Model):
    ano_letivo = db.Column(db.Integer, primary_key = True)
    data_inicio = db.Column(db.Date, nullable = False)
    data_fim = db.Column(db.Date, nullable = False)
    dias_letivos = db.Column(db.Integer, nullable = False)

    turmas = db.relationship('Turma', backref='ano_letivo', lazy=True)