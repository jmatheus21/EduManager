"""
Módulo de Modelo da Entidade Sala.

Este módulo define a classe `Sala`, que representa a entidade "Sala" no banco de dados.
A classe utiliza o SQLAlchemy para mapear a tabela no banco de dados e fornecer operações CRUD.
"""

from app.extensions import db


class Sala(db.Model):
    """Classe que representa a entidade Sala no banco de dados.

    Atributos:
        numero (int): Número da sala (chave primária).
        localizacao (str): Localização da sala (máximo 100 caracteres).
        capacidade (int): Capacidade da sala (número inteiro positivo).
        turmas (relationship): Relacionamento com a entidade Turma. Cada sala pode ter várias turmas associadas.
    """

    numero = db.Column(db.Integer, primary_key=True, doc="Número da sala (chave primária).")
    localizacao = db.Column(db.String(100), nullable=False, doc="Localização da sala (máximo 100 caracteres).")
    capacidade = db.Column(db.Integer, nullable=False, doc="Capacidade da sala (número inteiro positivo).")

    turmas = db.relationship('Turma', backref='sala', lazy=True, cascade='save-update, merge, refresh-expire', doc="Relacionamento com a entidade Turma. Cada sala pode ter várias turmas associadas.")