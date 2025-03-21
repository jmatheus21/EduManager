from app.extensions import db

class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    salario = db.Column(db.Numeric(10, 2), nullable=False)
    data_contrato = db.Column(db.Date, nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete ='CASCADE', onupdate ='CASCADE'), nullable=False)