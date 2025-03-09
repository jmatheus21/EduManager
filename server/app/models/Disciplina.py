"""
Módulo de Modelo da Entidade Disciplina.

Este módulo define a classe `Disciplina`, que representa a entidade "Disciplina" no banco de dados.
A classe utiliza o SQLAlchemy para mapear a tabela no banco de dados e fornecer operações CRUD.
"""

from app.extensions import db


class Disciplina(db.Model):
    """Classe que representa a entidade Disciplina no banco de dados.

    Atributos:
        codigo (str): Código da disciplina (chave primária) (máximo 10 caracteres).
        nome (str): Nome da disciplina (máximo 50 caracteres).
        carga_horaria: Carga horária da disciplina (número inteiro positivo).
        ementa: Ementa da disciplina (máximo de 100 caracteres) (Pode ser nulo).
        bibliografia: Bibliografia da disciplina (máximo 100 caracteres) (Pode ser nulo).
        aulas (relationship): Relacionamento com a entidade Aula. Cada disciplina deve ter uma ou mais aulas associadas.
    """

    codigo = db.Column(db.String(10), primary_key = True)
    nome = db.Column(db.String(50), nullable = False)
    carga_horaria = db.Column(db.Integer, nullable = False)
    ementa = db.Column(db.String(100), nullable = True)
    bibliografia = db.Column(db.String(100), nullable = True)

    aulas = db.relationship('Aula', backref='disciplina', lazy=True, doc="Relacionamento com a entidade Aula. Cada disciplina deve ter uma ou várias aulas associadas.")