"""
Este módulo contém testes para as operações relacionadas a classe modelo `aluno`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o modelo `aluno`,
incluindo cadastro, listagem, busca, atualização e remoção de alunos no banco de dados.
"""

from app.models import Aluno
from app.extensions import db
from app.utils.date_helpers import string_para_data, data_para_string


def test_cadastrar_aluno(app):
    """Testa o cadastro de um aluno no banco de dados.

    Este teste verifica se um aluno pode ser cadastrado corretamente no banco de dados
    e se os dados da aluno cadastrado estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        aluno = Aluno(matricula="202600000001", nome="João Pedro dos Santos", email="joaopedro@email.com", telefone="79 9 1234-5678", endereco="Bairro X, Rua A", data_de_nascimento=string_para_data("2011-09-10"))
        db.session.add(aluno)
        db.session.commit()

        aluno_adicionado = db.session.get(Aluno, "202600000001")
        assert aluno_adicionado is not None
        assert aluno_adicionado.matricula == "202600000001"
        assert aluno_adicionado.nome == "João Pedro dos Santos"
        assert aluno_adicionado.email == "joaopedro@email.com"
        assert aluno_adicionado.telefone == "79 9 1234-5678"
        assert aluno_adicionado.endereco == "Bairro X, Rua A"
        assert data_para_string(aluno_adicionado.data_de_nascimento) == "2011-09-10"
        

def test_listar_alunos(app):
    """Testa a listagem de todos os alunos cadastrados no banco de dados.

    Este teste verifica se a listagem de alunos retorna corretamente todos os alunos
    cadastrados e se os dados do primeiro aluno na lista estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        aluno = Aluno(matricula="202600000001", nome="João Pedro dos Santos", email="joaopedro@email.com", telefone="79 9 1234-5678", endereco="Bairro X, Rua A", data_de_nascimento=string_para_data("2011-09-10"))
        db.session.add(aluno)
        db.session.commit()

        alunos = Aluno.query.all()
        assert alunos[0] is not None
        assert alunos[0].matricula == "202600000001"
        assert alunos[0].nome == "João Pedro dos Santos"
        assert alunos[0].email == "joaopedro@email.com"
        assert alunos[0].telefone == "79 9 1234-5678"
        assert alunos[0].endereco == "Bairro X, Rua A"
        assert data_para_string(alunos[0].data_de_nascimento) == "2011-09-10"


def test_buscar_aluno(app):
    """Testa a busca de um aluno específico pela matrícula no banco de dados.

    Este teste verifica se um aluno pode ser buscado corretamente pela matrícula
    e se os dados do aluno buscado estão corretos.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        aluno = Aluno(matricula="202600000001", nome="João Pedro dos Santos", email="joaopedro@email.com", telefone="79 9 1234-5678", endereco="Bairro X, Rua A", data_de_nascimento="2011-09-10")
        db.session.add(aluno)
        db.session.commit()

        aluno_buscado = db.session.get(Aluno, "202600000001")
        assert aluno_buscado is not None
        assert aluno_buscado.matricula == "202600000001"
        assert aluno_buscado.nome == "João Pedro dos Santos"
        assert aluno_buscado.email == "joaopedro@email.com"
        assert aluno_buscado.telefone == "79 9 1234-5678"
        assert aluno_buscado.endereco == "Bairro X, Rua A"
        assert data_para_string(aluno_buscado.data_de_nascimento) == "2011-09-10"


    # def test_alterar_aluno(app):
    # """Testa a atualização dos dados de um aluno no banco de dados.

    # Este teste verifica se os dados de um aluno podem ser atualizados corretamente
    # e se os novos dados são persistidos no banco de dados.

    # Args:
    #     app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    # """
    # with app.app_context():
        

# def test_remover_aluno(app):
#     """Testa a remoção de um aluno do banco de dados.

#     Este teste verifica se um aluno pode ser removido corretamente do banco de dados
#     e se o aluno não pode mais ser encontrado após a remoção.

#     Args:
#         app (Flask): Aplicação Flask para acessar o contexto da aplicação.
#     """
#     with app.app_context():