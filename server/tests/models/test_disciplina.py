"""
Este módulo contém testes para as operações relacionadas a classe modelo `Disciplina`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o modelo `Disciplina`,
incluindo cadastro, listagem, busca, atualização e remoção de disciplinas no banco de dados. 
"""

from app.models import Disciplina
from app.extensions import db


def test_cadastrar_disciplina(app):
    """Testa o cadastro de uma disciplina no banco de dados.

    Este teste verifica se uma disciplina pode ser cadastrada corretamente no banco de dados
    e se os dados da disciplina cadastrada estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014.")
        db.session.add(disciplina)
        db.session.commit()

        disciplina_adicionada = Disciplina.query.filter_by(codigo="MAT001").first()
        assert disciplina_adicionada is not None
        assert disciplina_adicionada.codigo == "MAT001"
        assert disciplina_adicionada.nome == "Matemática"
        assert disciplina_adicionada.carga_horaria == 30
        assert disciplina_adicionada.ementa == "Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos."
        assert disciplina_adicionada.bibliografia == "STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014."


def test_listar_disciplinas(app):
    """Testa a listagem de todas as disciplinas cadastradas no banco de dados.

    Este teste verifica se a listagem de disciplinas retorna corretamente todas as disciplinas
    cadastradas e se os dados da primeira disciplina na lista estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014.")
        db.session.add(disciplina)
        db.session.commit()

        disciplinas = Disciplina.query.all()
        assert disciplinas[0] is not None
        assert disciplinas[0].codigo == "MAT001"
        assert disciplinas[0].nome == "Matemática"
        assert disciplinas[0].carga_horaria == 30
        assert disciplinas[0].ementa == "Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos."
        assert disciplinas[0].bibliografia == "STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014."


def test_buscar_disciplina(app):
    """Testa a busca de uma disciplina específica pelo número no banco de dados.

    Este teste verifica se uma disciplina pode ser buscada corretamente pelo número
    e se os dados da disciplina buscada estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014.")
        db.session.add(disciplina)
        db.session.commit()

        disciplina_buscada = db.session.get(Disciplina, "MAT001")
        assert disciplina_buscada is not None
        assert disciplina_buscada.codigo == "MAT001"
        assert disciplina_buscada.nome == "Matemática"
        assert disciplina_buscada.carga_horaria == 30
        assert disciplina_buscada.ementa == "Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos."
        assert disciplina_buscada.bibliografia == "STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014."


def test_alterar_disciplina(app):
    """Testa a atualização dos dados de uma disciplina no banco de dados.

    Este teste verifica se os dados de uma disciplina podem ser atualizados corretamente
    e se os novos dados são persistidos no banco de dados.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014.")
        db.session.add(disciplina)
        db.session.commit()

        disciplina_original = db.session.get(Disciplina, "MAT001")
        disciplina_original.codigo = "MAT001"
        disciplina_original.nome = "Matemática"
        disciplina_original.carga_horaria = 120
        disciplina_original.ementa = "Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos."
        disciplina_original.bibliografia = "STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014."
        db.session.commit()

        disciplina_alterada = db.session.get(Disciplina, "MAT001")
        assert disciplina_alterada is not None
        assert disciplina_alterada.codigo == "MAT001"
        assert disciplina_alterada.nome == "Matemática"
        assert disciplina_alterada.carga_horaria == 120
        assert disciplina_alterada.ementa == "Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos."
        assert disciplina_alterada.bibliografia == "STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014."


def test_remover_disciplina(app):
    """Testa a remoção de uma disciplina do banco de dados.

    Este teste verifica se uma disciplina pode ser removida corretamente do banco de dados
    e se a disciplina não pode mais ser encontrada após a remoção.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014.")
        db.session.add(disciplina)
        db.session.commit()

        disciplina_adicionada = db.session.get(Disciplina, "MAT001")
        db.session.delete(disciplina_adicionada)
        db.session.commit()

        disciplina_deletada = db.session.get(Disciplina, "MAT001")
        assert disciplina_deletada is None