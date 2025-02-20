from ..extensions import db

class Aula (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    dias_da_semana = db.Column(db.String(100), nullable=False)

    professor_cpf = db.Column(db.String(20), db.ForeignKey('usuario.cpf'), nullable=False)
    disciplina_codigo = db.Column(db.String(10), db.ForeignKey('disciplina.codigo'), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)