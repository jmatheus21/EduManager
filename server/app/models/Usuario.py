"""
Módulo de Modelo da Entidade Usuário.

Este módulo define a classe `Usuário`, que representa a entidade "Usuário" no banco de dados.
A classe utiliza o SQLAlchemy para mapear a tabela no banco de dados e fornecer operações CRUD.
"""

from app.extensions import db

# Tabela de associação para o relacionamento Muitos para Muitos entre professor e disciplina
professor_disciplina = db.Table(
    'professor_disciplina',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate = 'CASCADE'), primary_key=True),
    db.Column('disciplina_codigo', db.String(10), db.ForeignKey('disciplina.codigo',ondelete=('CASCADE'), onupdate = ('CASCADE')), primary_key=True)
)

class Usuario(db.Model):
    """Classe que representa a entidade Usuário no banco de dados.

    Atributos:
        id (integer): id do usuário (chave primária).
        cpf (str): CPF do usuário (11 caracteres, é único).
        nome (str): Nome do usuário (máximo 100 caracteres).
        email (str): Email do usuário (máximo 100 caracteres).
        senha (str): Senha do usuário (máximo 100 caracteres).
        telefone (str): Telefone do usuário (máximo 50 caracteres, pode ser NULL).
        endereco (str): Endereço do usuário (máximo 255 caracteres, pode ser NULL).
        horario_de_trabalho (str): Horário de trabalho do usuário (máximo 20 caracteres).
        data_de_nascimento (date): Data de nascimento do usuário (YYYY-MM-DD / YYYY representa o ano, MM o mês e DD o dia).
        tipo (char): O tipo do usuário - funcionário ou professor (char).
        formacao (str): A formação do usuário (máximo 255 caracteres, pode ser NULL).
        escolaridade (str): O nível de escolaridade do usuário (máximo 255 caracteres, pode ser NULL).
        habilidades (str): As habilidades do usuário (máximo 255 caracteres, pode ser NULL).
        disciplinas (relationship): Relacionamento com a entidade Disciplina. Cada usuário do tipo professor pode ensinar várias disciplinas.
        cargos (relationship): Relacionamento com a entidade Cargo. Cada usuário pode ter vários cargos associados.
        aulas (relationship): Relacionamento com a entidade Aula. Cada usuário do tipo professor pode ministrar várias aulas.
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc="Id do usuário (chave primária)")
    cpf = db.Column(db.CHAR(11), unique=True, nullable = False, doc = "CPF do usuário")
    nome = db.Column(db.String(100), nullable=False, doc = "Nome do usuário (máximo 100 caracteres).")
    email = db.Column(db.String(100), unique=True, nullable=False, doc = "Email do usuário (máximo 100 caracteres).")
    senha = db.Column(db.String(100), nullable=False, doc = "Senha do usuário (máximo 100 caracteres).")
    telefone = db.Column(db.CHAR(14), nullable=False, doc = "Telefone do usuário (máximo 50 caracteres).")
    endereco = db.Column(db.String(255), nullable=False, doc = "Endereço do usuário (máximo 255 caracteres).")
    horario_de_trabalho = db.Column(db.String(20), nullable=False, doc = "Horário de trabalho do usuário (máximo 20 caracteres).")
    data_de_nascimento = db.Column(db.Date, nullable=False, doc = "Data de nascimento do usuário (YYYY-MM-DD / YYYY representa o ano, MM o mês e DD o dia).")
    tipo = db.Column(db.CHAR(1), nullable=False, doc = "O tipo do usuário - funcionário ou professor.")
    formacao = db.Column(db.String(255), nullable=True, doc = "A formação do usuário (máximo 255 caracteres, pode ser NULL).")
    escolaridade = db.Column(db.String(255), nullable=True, doc = "O nível de escolaridade do usuário (máximo 255 caracteres, pode ser NULL).")
    habilidades = db.Column(db.String(255), nullable=True, doc = "As habilidades do usuário (máximo 255 caracteres, pode ser NULL).")

    aulas = db.relationship('Aula', backref='professor', lazy=True, cascade='all, delete-orphan', doc = "Relacionamento com a entidade Aula. Cada usuário do tipo professor pode ministrar várias aulas.")
    cargos = db.relationship('Cargo', backref='usuario', lazy=True, cascade='all, delete-orphan', doc = "Relacionamento com a entidade Cargo. Cada usuário pode ter vários cargos associados.")

    disciplinas = db.relationship(
        'Disciplina',
        secondary=professor_disciplina,
        backref=db.backref('professores', lazy=True),
        lazy=True, doc = "Relacionamento com a entidade Disciplina. Cada usuário do tipo professor pode ensinar várias disciplinas."
    )
