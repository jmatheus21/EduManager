"""
Módulo de Modelo da Entidade Aluno.

Este módulo define a classe `Aluno`, que representa a entidade "Aluno" no banco de dados.
A classe utiliza o SQLAlchemy para mapear a tabela no banco de dados e fornecer operações CRUD.
"""

from app.extensions import db


# Tabela de associação para o relacionamento Muitos para Muitos entre aluno e turma
aluno_turma = db.Table(
    'aluno_turma',
    db.Column('aluno_matricula', db.String(15), db.ForeignKey('aluno.matricula', ondelete='CASCADE', onupdate = 'CASCADE'), primary_key=True),
    db.Column('turma_id', db.Integer, db.ForeignKey('turma.id', ondelete='CASCADE', onupdate = 'CASCADE'), primary_key=True)
)


class Aluno (db.Model):
    """Classe que representa a entidade Aluno no banco de dados.

    Atributos:
        matricula (str): Matricula do aluno (chave primária).
        nome (str): Nome do aluno (máximo 100 caracteres).
        email (str): Email do aluno (máximo 100 caracteres).
        telefone (str): Telefone do aluno (máximo 50 caracteres).
        endereco (str): Endereço do aluno (máximo 255 caracteres).
        data_de_nascimento (date): Data de nascimento do aluno (YYYY-MM-DD / YYYY representa o ano, MM o mês e DD o dia).
        boletins: Relacionamento com a entidade Boletim. Cada aluno deve ter um boletim associado a ele.
    """
    matricula = db.Column(db.String(15), primary_key=True, doc="Matricula do aluno (chave primária).")
    nome = db.Column(db.String(100), nullable=False, doc="Nome do aluno (máximo 100 caracteres).")
    email = db.Column(db.String(100), unique=True, nullable=False, doc="Email do aluno (máximo 100 caracteres).")
    telefone = db.Column(db.String(50), nullable=False, doc="Telefone do aluno (máximo 50 caracteres).")
    endereco = db.Column(db.String(255), nullable=False, doc="Endereço do aluno (máximo 255 caracteres).")
    data_de_nascimento = db.Column(db.Date, nullable=False, doc="Data de nascimento do aluno (YYYY-MM-DD / YYYY representa o ano, MM o mês e DD o dia).")

    boletins = db.relationship('Boletim', back_populates='aluno', cascade = 'all, delete')

    turmas = db.relationship(
        'Turma',
        secondary=aluno_turma,
        backref=db.backref('alunos', lazy=True),
        lazy=True, 
        doc = "Relacionamento com a entidade Turma. Cada aluno pode participar de várias turmas ao longo do tempo na escola."
    )