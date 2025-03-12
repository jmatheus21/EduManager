"""
Módulo de Modelo da Entidade Turma.

Este módulo define a classe `Turma`, que representa a entidade "Turma" no banco de dados.
A classe utiliza o SQLAlchemy para mapear a tabela no banco de dados e fornecer operações CRUD.
"""

from app.extensions import db


class Turma(db.Model):
    """Classe que representa a entidade Turma no banco de dados.

    Atributos:
        id (int): Id da turma (Chave primária) (Autoincrementa-se).
        ano (int): Ano da turma (Número inteiro positivo).
        serie (str): A série da turma (Carácter único).
        nivel_de_ensino (str): O nível de ensino da turma (máximo 30 caracteres).
        turno (str): O turno da turma (Carácter único).
        status (str): O status da turma (Carácter único).
        sala_numero (int): O número da sala de aula (chave estrangeira de `Sala`(numero)).
        calendario_ano_letivo (int): O ano letivo do calendário da turma (chave estrangeira de `Calendario`(ano_letivo)).
        aulas (relatioship): Relacionamento com a entidade Aula. Cada turma deve ter uma ou várias aulas associadas. 
    """

    id = db.Column(db.Integer, primary_key = True, autoincrement = True, doc="Id da turma (Chave primária) (Autoincrementa-se).")
    ano = db.Column(db.Integer, nullable = False, doc="Ano da turma (Número inteiro positivo).")
    serie = db.Column(db.CHAR(1), nullable = False, doc="A série da turma (Carácter único).")
    nivel_de_ensino = db.Column(db.String(30), nullable = False, doc="O nível de ensino da turma (máximo 30 caracteres).")
    turno = db.Column(db.CHAR(1), nullable = False, doc="O turno da turma (Carácter único).")
    status = db.Column(db.CHAR(1), nullable = False, default='A', doc="O status da turma (Carácter único).")

    sala_numero = db.Column(db.Integer, db.ForeignKey('sala.numero'), nullable = False, doc="O número da sala de aula (chave estrangeira de `Sala`(numero)).")
    calendario_ano_letivo = db.Column(db.Integer, db.ForeignKey('calendario.ano_letivo'), nullable = False, doc="O ano letivo do calendário da turma (chave estrangeira de `Calendario`(ano_letivo)).")

    aulas = db.relationship('Aula', backref='turma', lazy=True, doc="Relacionamento com a entidade Aula. Cada turma deve ter uma ou várias aulas associadas.")