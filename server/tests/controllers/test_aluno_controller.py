"""
Este módulo contém testes para as rotas e as operações relacionadas a classe de controle `aluno_controller`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o controle `aluno_controller`,
incluindo cadastro, listagem, busca, atualização e remoção de alunos no banco de dados.
"""

from app.models import Aluno, Turma, Sala, Calendario
from app.extensions import db
from app.utils.date_helpers import string_para_data
from tests.user_event import usuario_entra_no_sistema


def criar_dependencias(app):
    """ Garante que instâncias das entidades `Turma` estejam disponíveis para 
    que testes na classe `Aluno` possam ser feitos.
    """
    with app.app_context():
        with db.session.no_autoflush:
            # Garante que a turma existe
            if not Turma.query.filter_by(id=1).first():
                calendario = Calendario(ano_letivo = 2026, data_inicio=string_para_data("2026-02-17"), data_fim=string_para_data("2026-11-27"), dias_letivos=150)
                db.session.add(calendario)
                sala = Sala(numero=101, capacidade=50, localizacao="Bloco A, 1° andar")
                db.session.add(sala)
                turma1 = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="M", status="A", sala_numero=101, calendario_ano_letivo=2026)
                db.session.add(turma1)
                turma2 = Turma(ano=1, serie="A", nivel_de_ensino="Ensino Médio", turno="V", status="C", sala_numero=101, calendario_ano_letivo=2026)
                db.session.add(turma2)

            db.session.commit()
    return turma1, turma2

    return turma1, turma2


def test_cadastrar_aluno(client, app):
    """Testa o cadastro de um aluno com dados válidos.

    Este teste verifica se:
    1. A requisição POST para a rota '/aluno' retorna o status code 201 (Created).
    2. A resposta contém uma mensagem indicando sucesso.
    3. Os dados do aluno cadastrado são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario_entra_no_sistema(client, app)
        criar_dependencias(app)

        dados_validos = {
            "nome": "João Pedro dos Santos",
            "email": "joaopedro@email.com",
            "telefone": "79 9 1234-5678",
            "endereco": "Bairro X, Rua A",
            "data_de_nascimento": "2011-09-10",
            "turma_id": 1,
        }

        response = client.post('/aluno/', json=dados_validos)

        assert response.status_code == 201, "O status code deve ser 201 (Created)."
        assert "mensagem" in response.json, "A resposta deve conter uma mensagem."
        assert "data" in response.json, "A resposta deve conter os dados do aluno."
        
        aluno = response.json["data"]
        
        assert aluno["matricula"] == "202600000001", "A matrícula do aluno deve ser '202600000001'."
        assert aluno["nome"] == "João Pedro dos Santos", "O nome do aluno deve ser 'João Pedro dos Santos'."
        assert aluno["email"] == "joaopedro@email.com", "O e-mail do aluno deve ser 'joaopedro@email.com'."
        assert aluno["telefone"] == "79 9 1234-5678", "O número do aluno deve ser '79 9 1234-5678'."
        assert aluno["endereco"] == "Bairro X, Rua A", "O endereço do aluno deve ser 'Bairro X, Rua A'."
        assert aluno["data_de_nascimento"] == "2011-09-10", "A data de nascimento do aluno deve ser '2011-09-10'."


def test_cadastrar_aluno_existente(client, app):
    """Testa o cadastro de um aluno já existente.

    Este teste verifica se:
    1. A requisição POST para a rota '/aluno' retorna o status code 400 (Bad Request).
    2. A resposta contém uma mensagem indicando fracasso.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario_entra_no_sistema(client, app)
        criar_dependencias(app)

        aluno = Aluno(matricula="202600000001", nome="João Pedro dos Santos", email="joaopedro@email.com", telefone="79 9 1234-5678", endereco="Bairro X, Rua A", data_de_nascimento=string_para_data("2011-09-10"))
        db.session.add(aluno)
        db.session.commit()

        dados = {
            "nome": "João Pedro dos Santos",
            "email": "joaopedro@email.com",
            "telefone": "79 9 1234-5678",
            "endereco": "Bairro X, Rua A",
            "data_de_nascimento": "2011-09-10",
            "turma_id": 1,
        }

        response = client.post('/aluno/', json=dados)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "Matrícula já existe."


def test_cadastrar_aluno_turma_inexistente(client, app):
    """Testa o cadastro de uma aluno com dado turma inexistente.

    Este teste verifica se:
    1. A requisição POST para a rota '/aluno' retorna o status code 400 (Bad Request).
    2. A resposta contém uma mensagem indicando "A turma não existe".

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario_entra_no_sistema(client, app)

        dados = {
            "nome": "João Pedro dos Santos",
            "email": "joaopedro@email.com",
            "telefone": "79 9 1234-5678",
            "endereco": "Bairro X, Rua A",
            "data_de_nascimento": "2011-09-10",
            "turma_id": 1,
        }

        response = client.post('/aluno/', json=dados)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A turma não existe."


def test_cadastrar_aluno_dados_invalidos(client, app):
    """Testa o cadastro de uma aluno com dados inválidos.

    Este teste verifica se a requisição POST para a rota '/aluno' retorna o status code 400 (Bad Request)
    e se a resposta contém mensagens de erro para cada campo inválido.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario_entra_no_sistema(client, app)
        criar_dependencias(app)

        dados_invalidos = {
            "nome": "",
            "email": "",
            "telefone": "79 9 12345-678", # Formato inválido
            "endereco": "",
            "data_de_nascimento": "3200-09-10",
            "turma_id": 1,
        }

        response = client.post('/aluno/', json=dados_invalidos)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 5, "Deve haver 5 erros de validação."


def test_listar_alunos(client, app):
    """Testa a listagem de alunos cadastrados.

    Este teste verifica se a requisição GET para a rota '/aluno/' retorna o status code 200 (OK)
    e se a resposta contém uma lista com os alunos cadastrados.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario_entra_no_sistema(client, app)
        turma1, turma2 = criar_dependencias(app)

        aluno = Aluno(matricula="202600000001", nome="João Pedro dos Santos", email="joaopedro@email.com", telefone="79 9 1234-5678", endereco="Bairro X, Rua A", data_de_nascimento=string_para_data("2011-09-10"), turmas=[turma1, turma2])
        db.session.add(aluno)
        db.session.commit()

        response = client.get('/aluno/')
        
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, list), "A resposta deve ser uma lista."
        assert len(response.json) == 1, "Deve haver exatamente 1 aluno na listagem."
        assert "matricula" in response.json[0], "A resposta deve conter o campo 'matricula'."
        

def test_buscar_aluno(client, app):
    """Testa a busca de um aluno específico pela matrícula.

    Este teste verifica se a requisição GET para a rota '/aluno/{matricula}' retorna o status code 200 (OK)
    e se a resposta contém os dados corretos do aluno buscado.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario_entra_no_sistema(client, app)
        turma1, turma2 = criar_dependencias(app)

        aluno = Aluno(matricula="202600000001", nome="João Pedro dos Santos", email="joaopedro@email.com", telefone="79 9 1234-5678", endereco="Bairro X, Rua A", data_de_nascimento=string_para_data("2011-09-10"), turmas=[turma1])
        db.session.add(aluno)
        db.session.commit()

        response = client.get(f'/aluno/{aluno.matricula}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, dict), "A resposta deve ser um dicionário."

        dados = response.json
        
        assert "matricula" in dados, "A resposta deve conter o campo 'matricula'."
        assert dados["matricula"] == "202600000001", "A matrícula do aluno deve ser 202600000001."
        assert dados["nome"] == "João Pedro dos Santos", "O nome do aluno deve ser João Pedro dos Santos."
        assert dados["email"] == "joaopedro@email.com", "O email do aluno deve ser joaopedro@email.com."
        assert dados["telefone"] == "79 9 1234-5678", "O telefone do aluno deve ser 79 9 1234-5678."
        assert dados["endereco"] == "Bairro X, Rua A", "O endereco do aluno deve ser Bairro X, Rua A."
        assert dados["data_de_nascimento"] == "2011-09-10", "A data de nascimento do aluno deve ser 2011-09-10."


def test_alterar_aluno(client, app):
    """Testa a atualização dos dados de um aluno.

    Este teste verifica se a requisição PUT para a rota '/aluno/{matricula}' retorna o status code 200 (OK),
    se a resposta contém uma mensagem de sucesso e se os dados da aluno foram atualizados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario_entra_no_sistema(client, app)
        turma1, turma2 = criar_dependencias(app)

        aluno = Aluno(matricula="202600000001", nome="João Pedro dos Santos", email="joaopedro@email.com", telefone="79 9 1234-5678", endereco="Bairro X, Rua A", data_de_nascimento=string_para_data("2011-09-10"), turmas=[turma2])
        db.session.add(aluno)
        db.session.commit()

        # Dados para atualização
        dados_atualizacao = {
            "nome": "João Pedro dos Santos",
            "email": "joaopedro123@email.com",
            "telefone": "79 9 1234-5678",
            "endereco": "Bairro X, Rua A",
            "data_de_nascimento": "2011-09-11",
            "turma_id": 1,
        }

        response = client.put(f'/aluno/{aluno.matricula}', json=dados_atualizacao)

        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert "mensagem" in response.json, "A resposta deve conter uma mensagem."
        assert "data" in response.json, "A resposta deve conter os dados do aluno."
        
        aluno = response.json["data"]
        
        assert aluno["matricula"] == "202600000001", "A matrícula do aluno deve ser '202600000001'."
        assert aluno["nome"] == "João Pedro dos Santos", "O nome do aluno deve ser 'João Pedro dos Santos'."
        assert aluno["email"] == "joaopedro123@email.com", "O e-mail do aluno deve ser 'joaopedro123@email.com'."
        assert aluno["telefone"] == "79 9 1234-5678", "O número do aluno deve ser '79 9 1234-5678'."
        assert aluno["endereco"] == "Bairro X, Rua A", "O endereço do aluno deve ser 'Bairro X, Rua A'."
        assert aluno["data_de_nascimento"] == "2011-09-11", "A data de nascimento do aluno deve ser '2011-09-11'."

def test_alterar_aluno_turma_inexistente(client, app):
    """Testa a atualização dos dados de um aluno.

    Este teste verifica se a requisição PUT para a rota '/aluno/{matricula}' retorna o status code 400 (Bad request),
    se a resposta contém uma mensagem de erro e se os dados da aluno não foram atualizados.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario_entra_no_sistema(client, app)
        turma1, turma2 = criar_dependencias(app)

        aluno = Aluno(matricula="202600000001", nome="João Pedro dos Santos", email="joaopedro@email.com", telefone="79 9 1234-5678", endereco="Bairro X, Rua A", data_de_nascimento=string_para_data("2011-09-10"), turmas=[turma1, turma2])
        db.session.add(aluno)
        db.session.commit()

        # Dados para atualização
        dados_atualizacao = {
            "nome": "João Pedro dos Santos",
            "email": "joaopedro123@email.com",
            "telefone": "79 9 1234-5678",
            "endereco": "Bairro X, Rua A",
            "data_de_nascimento": "2011-09-11",
            "turma_id": 3,
        }

        response = client.put(f'/aluno/{aluno.matricula}', json=dados_atualizacao)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        erro = response.json["erro"]
        assert "Turma não existe" in erro, "Deve haver um erro de turma inexistente"
        
def test_alterar_aluno_turma_fechada(client, app):
    """Testa a atualização dos dados de um aluno.

    Este teste verifica se a requisição PUT para a rota '/aluno/{matricula}' retorna o status code 400 (Bad request),
    se a resposta contém uma mensagem de erro e se os dados da aluno não foram atualizados.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario_entra_no_sistema(client, app)
        turma1, turma2 = criar_dependencias(app)

        aluno = Aluno(matricula="202600000001", nome="João Pedro dos Santos", email="joaopedro@email.com", telefone="79 9 1234-5678", endereco="Bairro X, Rua A", data_de_nascimento=string_para_data("2011-09-10"), turmas=[turma1])
        db.session.add(aluno)
        db.session.commit()

        # Dados para atualização
        dados_atualizacao = {
            "nome": "João Pedro dos Santos",
            "email": "joaopedro123@email.com",
            "telefone": "79 9 1234-5678",
            "endereco": "Bairro X, Rua A",
            "data_de_nascimento": "2011-09-11",
            "turma_id": 2,
        }

        response = client.put(f'/aluno/{aluno.matricula}', json=dados_atualizacao)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        erro = response.json["erro"]
        assert "A turma está fechada" in erro, "Deve haver um erro de turma fechada"

def test_deletar_aluno(client, app):
     """Testa a exclusão de um aluno.

     Este teste verifica se a requisição DELETE para a rota '/aluno/{matricula}' retorna o status code 200 (OK)
     e se a resposta contém uma mensagem de sucesso.

     Args:
         client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
         app (Flask): Aplicação Flask para acessar o contexto da aplicação.
     """
     with app.app_context():
        usuario_entra_no_sistema(client, app)
        criar_dependencias(app)

        aluno = Aluno(matricula="202600000001", nome="João Pedro dos Santos", email="joaopedro@email.com", telefone="79 9 1234-5678", endereco="Bairro X, Rua A", data_de_nascimento=string_para_data("2011-09-10"))
        db.session.add(aluno)
        db.session.commit()

        response = client.delete(f'/aluno/{aluno.matricula}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Aluno deletado com sucesso!"

    
