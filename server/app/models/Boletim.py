"""
Módulo de Modelo da Entidade Boletim.

Este módulo define a classe `Boletim`, que representa a entidade "boletim" no banco de dados.
A classe utiliza o SQLAlchemy para mapear a tabela no banco de dados e fornecer operações CRUD.
"""

from app.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY


class Boletim(db.Model):
    """Classe que representa a entidade Boletim no banco de dados.

    Atributos:
        aluno_matricula (str): Matricula do aluno.
        aula_id (int): O id da aula.
        notas (float): As notas relacionadas ao aluno.
        ausencias (int): As ausências de um aluno.
        situacao (str): A situação do aluno (Caractér único).
    """
    aluno_matricula = db.Column('aluno_matricula', db.String, db.ForeignKey('aluno.matricula', ondelete = 'CASCADE', onupdate = 'CASCADE'), primary_key=True)
    aula_id = db.Column('aula_id', db.Integer, db.ForeignKey('aula.id', ondelete = 'CASCADE', onupdate = 'CASCADE'), primary_key=True)
    notas = db.Column(ARRAY(db.Float), nullable=False)
    ausencias = db.Column(db.Integer, default=0)
    situacao = db.Column(db.CHAR(1), default="M") # M = matriculado, A = aprovado, R = reprovado

    aluno = db.relationship('Aluno', back_populates='boletins')
    aula = db.relationship('Aula', back_populates='boletins', cascade = 'all, delete')