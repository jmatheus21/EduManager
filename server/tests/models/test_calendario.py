"""
Este módulo contém testes para as operações relacionadas a classe modelo `Calendario`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o modelo `Calendario`,
incluindo cadastro, listagem, busca, atualização e remoção de calendários no banco de dados.
"""

from app.models import Calendario
from app.extensions import db
from app.utils.date_helpers import string_para_data, data_para_string


def test_cadastrar_calendario(app):
    """Testa o cadastro de um calendário no banco de dados.

    Este teste verifica se um calendário pode ser cadastrado corretamente no banco de dados
    e se os dados do calendário cadastrado estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        calendario = Calendario(ano_letivo=2026, data_inicio=string_para_data("2026-02-17"), data_fim=string_para_data("2026-11-27"), dias_letivos=150)
        db.session.add(calendario)
        db.session.commit()

        calendario_adicionado = db.session.get(Calendario, 2026)
        assert calendario_adicionado is not None
        assert calendario_adicionado.ano_letivo == 2026
        assert data_para_string(calendario_adicionado.data_inicio) == "2026-02-17"
        assert data_para_string(calendario_adicionado.data_fim) == "2026-11-27"
        assert calendario_adicionado.dias_letivos == 150


def test_listar_calendarios(app):
    """Testa a listagem de todos os calendários cadastrados no banco de dados.

    Este teste verifica se a listagem de calendários retorna corretamente todas os calendários
    cadastrados e se os dados do primeiro calendário na lista estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        calendario = Calendario(ano_letivo=2026, data_inicio=string_para_data("2026-02-17"), data_fim=string_para_data("2026-11-27"), dias_letivos=150)
        db.session.add(calendario)
        db.session.commit()

        calendarios = Calendario.query.all()
        assert calendarios[0] is not None
        assert calendarios[0].ano_letivo == 2026
        assert data_para_string(calendarios[0].data_inicio) == "2026-02-17"
        assert data_para_string(calendarios[0].data_fim) == "2026-11-27"
        assert calendarios[0].dias_letivos == 150


def test_buscar_calendario(app):
    """Testa a busca de um calendário específico pelo ano letivo no banco de dados.

    Este teste verifica se um calendário pode ser buscado corretamente pelo ano letivo
    e se os dados do calendário buscado estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        calendario = Calendario(ano_letivo=2026, data_inicio=string_para_data("2026-02-17"), data_fim=string_para_data("2026-11-27"), dias_letivos=150)
        db.session.add(calendario)
        db.session.commit()

        calendario_buscado = db.session.get(Calendario, 2026)
        assert calendario_buscado is not None
        assert calendario_buscado.ano_letivo == 2026
        assert data_para_string(calendario_buscado.data_inicio) == "2026-02-17"
        assert data_para_string(calendario_buscado.data_fim) == "2026-11-27"
        assert calendario_buscado.dias_letivos == 150


def test_alterar_calendario(app):
    """Testa a atualização dos dados de um calendario no banco de dados.

    Este teste verifica se os dados de um calendario podem ser atualizados corretamente
    e se os novos dados são persistidos no banco de dados.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        calendario = Calendario(ano_letivo=2026, data_inicio="2026-02-01", data_fim="2026-09-01", dias_letivos=50)
        db.session.add(calendario)
        db.session.commit()

        calendario_original = db.session.get(Calendario, 2026)
        calendario_original.ano_letivo = 2026
        calendario_original.data_inicio = "2026-02-01"
        calendario_original.data_fim = "2026-09-15"
        calendario_original.dias_letivos = 160
        db.session.commit()

        calendario_alterado = db.session.get(Calendario, 2026)
        assert calendario_alterado is not None
        assert calendario_alterado.ano_letivo == 2026
        assert data_para_string(calendario_alterado.data_inicio) == "2026-02-01"
        assert data_para_string(calendario_alterado.data_fim) == "2026-09-15"
        assert calendario_alterado.dias_letivos == 160


def test_remover_calendario(app):
    """Testa a remoção de um calendário do banco de dados.

    Este teste verifica se um calendário pode ser removido corretamente do banco de dados
    e se o calendário não pode mais ser encontrado após a remoção.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        calendario = Calendario(ano_letivo=2026, data_inicio="2026-02-01", data_fim="2026-09-01", dias_letivos=50)
        db.session.add(calendario)
        db.session.commit()

        calendario_adicionado = db.session.get(Calendario, 2026)
        db.session.delete(calendario_adicionado)
        db.session.commit()

        calendario_deletado = db.session.get(Calendario, 2026)
        assert calendario_deletado is None