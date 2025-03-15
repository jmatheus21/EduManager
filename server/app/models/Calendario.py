"""
Módulo de Modelo da Entidade Calendário.

Este módulo define a classe `Calendário`, que representa a entidade "Calendário" no banco de dados.
A classe utiliza o SQLAlchemy para mapear a tabela no banco de dados e fornecer operações CRUD.
"""

from app.extensions import db

class Calendario(db.Model):
    """Classe que representa a entidade Calendario no banco de dados.

    Atributos:
        ano_letivo (int): Ano letivo do calendário (chave primária).
        data_inicio (date): Data de início do calendário (Deve ser no formato 'YYYY-MM-DD', em que YYYY representa o ano, MM o mês e DD o dia).
        data_fim (date): Data de fim do calendário (Deve ser no formato 'YYYY-MM-DD', em que YYYY representa o ano, MM o mês e DD o dia).
        dias_letivos (int): Número de dias letivos no calendário (número inteiro positivo entre 50 e 200).
        turmas (relationship): Relacionamento com a entidade Turma. Cada calendário pode ter várias turmas associadas.
    """
    
    ano_letivo = db.Column(db.Integer, primary_key = True, doc="Ano letivo do calendário (chave primária).")
    data_inicio = db.Column(db.Date, nullable = False, doc = "Data de início do calendário (Deve ser no formato 'YYYY-MM-DD', em que YYYY representa o ano, MM o mês e DD o dia)")
    data_fim = db.Column(db.Date, nullable = False, doc = "Data de fim do calendário (Deve ser no formato 'YYYY-MM-DD', em que YYYY representa o ano, MM o mês e DD o dia)")
    dias_letivos = db.Column(db.Integer, nullable = False, doc = "Número de dias letivos no calendário (número inteiro positivo entre 50 e 200).")

    turmas = db.relationship('Turma', backref='calendario', lazy=True, cascade = 'all, delete-orphan', doc="Relacionamento com a entidade Turma. Cada calendário pode ter várias turmas associadas.")