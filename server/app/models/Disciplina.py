from app.extensions import db

class Disciplina(db.Model):
    codigo = db.Column(db.String(10), primary_key = True)
    nome = db.Column(db.String(50), nullable = False)
    carga_horaria = db.Column(db.Integer, nullable = False)
    ementa = db.Column(db.String(100), nullable = True)
    bibliografia = db.Column(db.String(100), nullable = True)

    aulas = db.relationship('Aula', backref='disciplina', lazy=True)