"""
Módulo de Modelo da Entidade Aula.

Este módulo define a classe `Aula`, que representa a entidade "Aula" no banco de dados.
A classe utiliza o SQLAlchemy para mapear a tabela no banco de dados e fornecer operações CRUD.
"""

from app.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY


class Aula (db.Model):
    """Classe que representa a entidade Aula no banco de dados.

    Atributos:
        id (int): O id da aula (Chave primária) (Autoincrementa-se).
        hora_inicio (time): O horário de início da aula (Deve ser no formato 'HH:MM', em que HH representa as horas e MM representa os minutos).
        hora_fim (time): O horário de fim da aula (Deve ser no formato 'HH:MM', em que HH representa as horas e MM representa os minutos).
        dias_da_semana (str): Os dias da semana que a aula ocorre (máximo de 7 caracteres).
        usuario_id (str): O cpf do professor que ministra a aula (máximo de 20 caracteres).
        disciplina_codigo (str): O código da discplina referente a aula (máximo de 10 caracteres).
        turma_id (int): O id da turma referente a aula (Número inteiro positivo).
        boletins (ralationship): Relacionamento com a entidade Boletim. Cada aula deve ter um boletim (pertencente a um aluno) associado a ela.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc="O id da aula (Chave primária) (Autoincrementa-se).")
    hora_inicio = db.Column(db.Time, nullable=False, doc="O horário de início da aula (Deve ser no formato 'HH:MM', em que HH representa as horas e MM representa os minutos).")
    hora_fim = db.Column(db.Time, nullable=False, doc="O horário de fim da aula (Deve ser no formato 'HH:MM', em que HH representa as horas e MM representa os minutos).")
    dias_da_semana = db.Column(ARRAY(db.String(7)), nullable=False, doc="Os dias da semana que a aula ocorre (máximo de 7 caracteres).")
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete = 'CASCADE', onupdate = 'CASCADE'), nullable=False, doc="O cpf do professor que ministra a aula (máximo de 20 caracteres).")
    disciplina_codigo = db.Column(db.String(10), db.ForeignKey('disciplina.codigo', ondelete = 'CASCADE', onupdate = 'CASCADE'), nullable=False, doc="O código da discplina referente a aula (máximo de 10 caracteres).")
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id', ondelete = 'CASCADE', onupdate = 'CASCADE'), nullable=False, doc="O id da turma referente a aula (Número inteiro positivo).")

    boletins = db.relationship('Boletim', back_populates='aula', cascade = 'all, delete', doc="Relacionamento com a entidade Boletim. Cada aula deve ter um boletim (pertencente a um aluno) associado a ela.")