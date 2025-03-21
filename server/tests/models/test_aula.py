"""
Este módulo contém testes para as operações relacionadas a classe modelo `Aula`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o modelo `Aula`,
incluindo cadastro, listagem, busca, atualização e remoção de aulas no banco de dados.
"""

from app.models import Aula, Usuario, Disciplina, Turma, Calendario, Sala
from app.extensions import db
from datetime import datetime
from app.utils.date_helpers import string_para_data


def criar_dependencias(app):
    """ Garante que instâncias das entidades `Usuario`, `Disciplina` e `Turma` estejam disponíveis para 
    que testes na classe `aula` possam ser feitos.
    """
    with app.app_context():
        with db.session.no_autoflush:
            # Garante que o usuário existe
            if not Usuario.query.filter_by(cpf="12345678912").first():
                usuario = Usuario(cpf="12345678912", nome="Alan Ferreira dos Santos", senha="bocaAberta123", telefone="79 9 9999-8888", endereco="Bairro X, Rua A",horario_de_trabalho="Seg-Sex,7h-12h", data_de_nascimento="1998-05-17", tipo="p", formacao="Licenciatura em Matemática", escolaridade= None, habilidades= None, disciplinas= ["MAT123", "FIS789"], cargos=[2])
                db.session.add(usuario)

            # Garante que a disciplina existe
            if not Disciplina.query.filter_by(codigo="MAT001").first():
                disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro:Zahar, 2014.")
                db.session.add(disciplina)

            # Garante que a turma existe
            if not Turma.query.filter_by(id=1).first():
                calendario = Calendario(ano_letivo = 2026, data_inicio=string_para_data("2026-02-17"), data_fim=string_para_data("2026-11-27"), dias_letivos=150)
                db.session.add(calendario)
                sala = Sala(numero=101, capacidade=50, localizacao="Bloco A, 1° andar")
                db.session.add(sala)
                turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="M", status="A", sala_numero= 101, calendario_ano_letivo= 2026)
                db.session.add(turma)

            db.session.commit()


#def criar_dependencias_usuario(app):
    


def test_cadastrar_aula(app):
    """Testa o cadastro de uma aula no banco de dados.

    Este teste verifica se uma aula pode ser cadastrada corretamente no banco de dados
    e se os dados da aula cadastrada estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)

        aula = aula(ano=9, serie="A", nivel_de_ensino="Fundamental", turno="D", status="A", sala_numero=101, calendario_ano_letivo=2026)
        db.session.add(aula)
        db.session.commit()

        aula_adicionada = aula.query.filter_by(id=aula.id).first()
        assert aula_adicionada is not None
        assert aula_adicionada.id == aula.id
        assert aula_adicionada.ano == 9
        assert aula_adicionada.serie == "A"
        assert aula_adicionada.nivel_de_ensino == "Fundamental"
        assert aula_adicionada.turno == "D"
        assert aula_adicionada.status == "A"
        assert aula_adicionada.sala_numero == 101
        assert aula_adicionada.calendario_ano_letivo == 2026


def test_listar_aulas(app):
    """Testa a listagem de todas as aulas cadastradas no banco de dados.

    Este teste verifica se a listagem de aulas retorna corretamente todas as aulas
    cadastradas e se os dados da primeira aula na lista estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)

        aula = aula(ano=9, serie="A", nivel_de_ensino="Fundamental", turno="D", status="A", sala_numero=101, calendario_ano_letivo=2026)
        db.session.add(aula)
        db.session.commit()

        aulas = aula.query.all()
        assert aulas[0] is not None
        assert aulas[0].id == aula.id
        assert aulas[0].ano == 9
        assert aulas[0].serie == "A"
        assert aulas[0].nivel_de_ensino == "Fundamental"
        assert aulas[0].turno == "D"
        assert aulas[0].status == "A"
        assert aulas[0].sala_numero == 101
        assert aulas[0].calendario_ano_letivo == 2026


def test_buscar_aula(app):
    """Testa a busca de uma aula específica pelo número no banco de dados.

    Este teste verifica se uma aula pode ser buscada corretamente pelo número
    e se os dados da aula buscada estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)

        aula = aula(ano=9, serie="A", nivel_de_ensino="Fundamental", turno="D", status="A", sala_numero=101, calendario_ano_letivo=2026)
        db.session.add(aula)
        db.session.commit()

        aula_buscada = db.session.get(aula, aula.id)
        assert aula_buscada is not None
        assert aula_buscada.id == aula.id
        assert aula_buscada.ano == 9
        assert aula_buscada.serie == "A"
        assert aula_buscada.nivel_de_ensino == "Fundamental"
        assert aula_buscada.turno == "D"
        assert aula_buscada.status == "A"
        assert aula_buscada.sala_numero == 101
        assert aula_buscada.calendario_ano_letivo == 2026


# def test_alterar_aula(app):
#     """Testa a atualização dos dados de uma aula no banco de dados.

#     Este teste verifica se os dados de uma aula podem ser atualizados corretamente
#     e se os novos dados são persistidos no banco de dados.

#     Args:
#         app (Flask): Aplicação Flask para acessar o contexto da aplicação.
#     """
#     with app.app_context():
#         criar_dependencias(app)


# def test_remover_aula(app):
#     """Testa a remoção de uma aula do banco de dados.

#     Este teste verifica se uma aula pode ser removida corretamente do banco de dados
#     e se a aula não pode mais ser encontrada após a remoção.

#     Args:
#         app (Flask): Aplicação Flask para acessar o contexto da aplicação.
#     """
#     with app.app_context():
#         criar_dependencias(app)