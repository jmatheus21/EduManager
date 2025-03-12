"""
Este módulo contém testes para as operações relacionadas a classe modelo `turma`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o modelo `turma`,
incluindo cadastro, listagem, busca, atualização e remoção de turmas no banco de dados.
"""

from app.models import Turma
from app.extensions import db


def test_cadastrar_turma(app):
    """Testa o cadastro de uma turma no banco de dados.

    Este teste verifica se uma turma pode ser cadastrada corretamente no banco de dados
    e se os dados da turma cadastrada estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        turma = Turma(ano=9, serie="A", nivel_de_ensino="Fundamental", turno="D", status="A", sala_numero="10", calendario_ano_letivo="2026")
        db.session.add(turma)
        db.session.commit()

        turma_adicionada = db.session.get(Turma, turma.id)
        assert turma_adicionada is not None
        assert turma_adicionada.ano == 9
        assert turma_adicionada.serie == "A"
        assert turma_adicionada.nivel_de_ensino == "Fundamental"
        assert turma_adicionada.turno == "D"
        assert turma_adicionada.status == "A"
        assert turma_adicionada.sala_numero == "10"
        assert turma_adicionada.calendario_ano_letivo == "2026"


def test_listar_turmas(app):
    """Testa a listagem de todas as turmas cadastradas no banco de dados.

    Este teste verifica se a listagem de turmas retorna corretamente todas as turmas
    cadastradas e se os dados da primeira turma na lista estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        turma = Turma(ano=9, serie="A", nivel_de_ensino="Fundamental", turno="D", status="A", sala_numero="10", calendario_ano_letivo="2026")
        db.session.add(turma)
        db.session.commit()

        turmas = Turma.query.all()
        assert turmas[0] is not None
        assert turmas[0].ano == 9
        assert turmas[0].serie == "A"
        assert turmas[0].nivel_de_ensino == "Fundamental"
        assert turmas[0].turno == "D"
        assert turmas[0].status == "A"
        assert turmas[0].sala_numero == "10"
        assert turmas[0].calendario_ano_letivo == "2026"


def test_buscar_turma(app):
    """Testa a busca de uma turma específica pelo número no banco de dados.

    Este teste verifica se uma turma pode ser buscada corretamente pelo número
    e se os dados da turma buscada estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        turma = Turma(ano=9, serie="A", nivel_de_ensino="Fundamental", turno="D", status="A", sala_numero="10", calendario_ano_letivo="2026")
        db.session.add(turma)
        db.session.commit()

        turma_buscada = db.session.get(Turma, turma.id)
        assert turma_buscada is not None
        assert turma_buscada.ano == 9
        assert turma_buscada.serie == "A"
        # assert turma_buscada.nivel_de_ensino == "Fundamental"
        # assert turma_buscada.turno == "D"
        # assert turma_buscada.status == "A"
        # assert turma_buscada.sala_numero == "10"
        # assert turma_buscada.calendario_ano_letivo == "2026"


def test_alterar_turma(app):
    """Testa a atualização dos dados de uma turma no banco de dados.

    Este teste verifica se os dados de uma turma podem ser atualizados corretamente
    e se os novos dados são persistidos no banco de dados.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        turma = Turma(ano=9, serie="A", nivel_de_ensino="Fundamental", turno="D", status="A", sala_numero="10", calendario_ano_letivo="2026")
        db.session.add(turma)
        db.session.commit()

        turma_original = db.session.get(Turma, turma.id)
        turma_original.ano == 9
        turma_original.serie == "A"
        turma_original.nivel_de_ensino == "Fundamental"
        turma_original.turno == "D"
        turma_original.status == "A"
        turma_original.sala_numero == "10"
        turma_original.calendario_ano_letivo == "2026"
        db.session.commit()

        turma_alterada = db.session.get(Turma, turma.id)
        assert turma_alterada is not None
        assert turma_alterada.ano == 9
        assert turma_alterada.serie == "D"
        assert turma_alterada.nivel_de_ensino == "Fundamental"
        assert turma_alterada.turno == "N"
        assert turma_alterada.status == "A"
        assert turma_alterada.sala_numero == "10"
        assert turma_alterada.calendario_ano_letivo == "2026"


def test_remover_turma(app):
    """Testa a remoção de uma turma do banco de dados.

    Este teste verifica se uma turma pode ser removida corretamente do banco de dados
    e se a turma não pode mais ser encontrada após a remoção.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        turma = Turma(ano=9, serie="A", nivel_de_ensino="Fundamental", turno="D", status="A", sala_numero="10", calendario_ano_letivo="2026")
        db.session.add(turma)
        db.session.commit()

        turma_adicionada = db.session.get(Turma, turma.id)
        db.session.delete(turma_adicionada)
        db.session.commit()

        turma_deletada = db.session.get(Turma, turma.id)
        assert turma_deletada is None