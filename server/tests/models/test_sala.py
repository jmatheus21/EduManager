"""
Este módulo contém testes para as operações relacionadas a classe modelo `Sala`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o modelo `Sala`,
incluindo cadastro, listagem, busca, atualização e remoção de salas no banco de dados.
"""

from app.models import Sala
from app.extensions import db


def test_cadastrar_sala(app):
    """Testa o cadastro de uma sala no banco de dados.

    Este teste verifica se uma sala pode ser cadastrada corretamente no banco de dados
    e se os dados da sala cadastrada estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        sala = Sala(numero=101, capacidade=50, localizacao="Bloco A, 1° andar")
        db.session.add(sala)
        db.session.commit()

        sala_adicionada = Sala.query.filter_by(numero=101).first()
        assert sala_adicionada is not None
        assert sala_adicionada.numero == 101
        assert sala_adicionada.capacidade == 50
        assert sala_adicionada.localizacao == "Bloco A, 1° andar"


def test_listar_salas(app):
    """Testa a listagem de todas as salas cadastradas no banco de dados.

    Este teste verifica se a listagem de salas retorna corretamente todas as salas
    cadastradas e se os dados da primeira sala na lista estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        sala = Sala(numero=101, capacidade=50, localizacao="Bloco A, 1° andar")
        db.session.add(sala)
        db.session.commit()

        salas = Sala.query.all()
        assert salas[0] is not None
        assert salas[0].numero == 101
        assert salas[0].capacidade == 50
        assert salas[0].localizacao == "Bloco A, 1° andar"


def test_buscar_sala(app):
    """Testa a busca de uma sala específica pelo número no banco de dados.

    Este teste verifica se uma sala pode ser buscada corretamente pelo número
    e se os dados da sala buscada estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        sala = Sala(numero=101, capacidade=50, localizacao="Bloco A, 1° andar")
        db.session.add(sala)
        db.session.commit()

        sala_buscada = db.session.get(Sala, 101)
        assert sala_buscada is not None
        assert sala_buscada.numero == 101
        assert sala_buscada.capacidade == 50
        assert sala_buscada.localizacao == "Bloco A, 1° andar"


def test_alterar_sala(app):
    """Testa a atualização dos dados de uma sala no banco de dados.

    Este teste verifica se os dados de uma sala podem ser atualizados corretamente
    e se os novos dados são persistidos no banco de dados.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        sala = Sala(numero=101, capacidade=50, localizacao="Bloco A, 1° andar")
        db.session.add(sala)
        db.session.commit()

        sala_original = db.session.get(Sala, 101)
        sala_original.numero = 101
        sala_original.capacidade = 100
        sala_original.localizacao = "Bloco B, 1° andar"
        db.session.commit()

        sala_alterada = db.session.get(Sala, 101)
        assert sala_alterada is not None
        assert sala_alterada.numero == 101
        assert sala_alterada.capacidade == 100
        assert sala_alterada.localizacao == "Bloco B, 1° andar"


def test_remover_sala(app):
    """Testa a remoção de uma sala do banco de dados.

    Este teste verifica se uma sala pode ser removida corretamente do banco de dados
    e se a sala não pode mais ser encontrada após a remoção.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        sala = Sala(numero=101, capacidade=50, localizacao="Bloco A, 1° andar")
        db.session.add(sala)
        db.session.commit()

        sala_adicionada = db.session.get(Sala, 101)
        db.session.delete(sala_adicionada)
        db.session.commit()

        sala_deletada = db.session.get(Sala, 101)
        assert sala_deletada is None