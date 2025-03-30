"""
Módulo de Modelo da Entidade Cargo.

Este módulo define a classe `Cargo`, que representa a entidade "Cargo" no banco de dados.
A classe utiliza o SQLAlchemy para mapear a tabela no banco de dados e fornecer operações CRUD.
"""

from app.extensions import db


class Cargo(db.Model):
    """Classe que representa a entidade Aula no banco de dados.

    Atributos:
        id (int): O id do cargo (Chave primária) (Autoincrementa-se).
        nome (str): O nome do cargo (máximo de 100 caracteres).
        salario (str): O salario do cargo (Numérico).
        data_contrato (date): A data de fim do contrato do cargo.
        usuario_id (int): O id do usuario referente ao cargo (Número inteiro positivo).
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    salario = db.Column(db.Numeric(10, 2), nullable=False)
    data_contrato = db.Column(db.Date, nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete ='CASCADE', onupdate ='CASCADE'), nullable=False)