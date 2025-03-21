"""
Este módulo contém testes para as rotas e as operações relacionadas à classe de controle `calendario_controller`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o controle `calendario_controller`,
incluindo cadastro, listagem, busca, atualização e remoção de calendários no banco de dados.
"""

from app.models import Calendario
from app.extensions import db
from tests.user_event import usuario_entra_no_sistema

def test_cadastrar_calendario(client, app):
    """Testa o cadastro de um calendário com dados válidos.

    Este teste verifica se:
    1. A requisição POST para a rota '/calendario/' retorna o status code 201 (Created).
    2. A resposta contém uma mensagem indicando sucesso.
    3. Os dados do calendário cadastrado são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():

        usuario_entra_no_sistema(client, app)

        dados_validos = {
            "ano_letivo": 2026,
            "data_inicio": "2026-02-17",
            "data_fim": "2026-11-27",
            "dias_letivos": 150
        }

        response = client.post('/calendario/', json=dados_validos)

        assert response.status_code == 201, "O status code deve ser 201 (Created)."
        assert "mensagem" in response.json, "A resposta deve conter uma mensagem."
        assert "data" in response.json, "A resposta deve conter os dados do calendário."
        calendario = response.json["data"]
        assert calendario["ano_letivo"] == 2026, "O ano letivo deve ser 2026."
        assert calendario["data_inicio"] == "2026-02-17", "A data de inicio deve ser 2026-02-17."
        assert calendario["data_fim"] == "2026-11-27", "A data de fim deve ser 2026-11-27."
        assert calendario["dias_letivos"] == 150, "A quantidade de dias letivos deve ser 150."


def test_cadastrar_calendario_dados_invalidos(client, app):
    """Testa o cadastro de um calendário com dados inválidos.

    Este teste verifica se a requisição POST para a rota '/calendario/' retorna o status code 400 (Bad Request)
    e se a resposta contém mensagens de erro para cada campo inválido.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():

        usuario_entra_no_sistema(client, app)

        dados_invalidos = {
            "ano_letivo": 2024,
            "data_inicio": "2024-02-17",
            "data_fim": "2023-11-27",
            "dias_letivos": 250
        }

        response = client.post('/calendario/', json=dados_invalidos)
        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 5, "Deve haver 5 erros de validação."

def test_cadastrar_calendario_existente(client, app):
    """Testa o cadastro de um calendário para um ano letivo já existente.

    Este teste verifica se a requisição POST para a rota '/calendario/' retorna o status code 400 (Bad Request)
    e se a resposta contém uma mensagem de erro indicando que o calendário já existe.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        
        usuario_entra_no_sistema(client, app)
        
        dados_invalidos = {
            "ano_letivo": 2026,
            "data_inicio": "2026-02-17",
            "data_fim": "2026-11-27",
            "dias_letivos": 150
        }
    
        calendario_existente = Calendario(ano_letivo=dados_invalidos['ano_letivo'], data_inicio=dados_invalidos['data_inicio'], data_fim=dados_invalidos['data_fim'], dias_letivos=dados_invalidos['dias_letivos'])
        db.session.add(calendario_existente)
        db.session.commit()
        
        response = client.post("/calendario/", json=dados_invalidos)
        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 1, "Deve haver 1 erro de validação."
        erro = response.json["erro"]

        assert "Calendário já existe" in erro, "Deve haver um erro de calendário existente"

def test_listar_calendarios(client, app):
    """Testa a listagem de calendários cadastrados.

    Este teste verifica se a requisição GET para a rota '/calendario/' retorna o status code 200 (OK)
    e se a resposta contém uma lista com os calendários cadastrados.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        
        usuario_entra_no_sistema(client, app)
        
        calendario = Calendario(ano_letivo=2026, data_inicio="2026-02-17", data_fim="2026-11-27", dias_letivos=150)
        db.session.add(calendario)
        db.session.commit()

        response = client.get('/calendario/')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, list), "A resposta deve ser uma lista."
        assert len(response.json) == 1, "Deve haver exatamente 1 calendario na listagem."
        assert response.json[0]["ano_letivo"] == 2026, "O ano letivo do calendário deve ser exatamente 2026."


def test_buscar_calendario(client, app):
    """Testa a busca de um calendário específico pelo ano letivo correspondente.

    Este teste verifica se a requisição GET para a rota '/calendario/{ano_letivo}' retorna o status code 200 (OK)
    e se a resposta contém os dados corretos do calendário a ser buscado.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        
        usuario_entra_no_sistema(client, app)
        
        calendario = Calendario(ano_letivo=2026, data_inicio="2026-02-17", data_fim="2026-11-27", dias_letivos=150)
        db.session.add(calendario)
        db.session.commit()

        response = client.get(f'/calendario/{calendario.ano_letivo}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, dict), "A resposta deve ser um dicionário."
        dados = response.json
        assert dados["ano_letivo"] == 2026, "O ano letivo deve ser 2026."
        assert dados["data_inicio"] == "2026-02-17", "A data de início deve ser 2026-02-17."
        assert dados["data_fim"] == "2026-11-27", "A data de fim deve ser 2026-11-27."
        assert dados["dias_letivos"] == 150, "A quantidade de dias letivos deve ser 150."


def test_alterar_calendario(client, app):
    """Testa a atualização dos dados de um calendário.

    Este teste verifica se a requisição PUT para a rota '/calendario/{ano_letivo}' retorna o status code 200 (OK),
    se a resposta contém uma mensagem de sucesso e se os dados do calendário foram atualizados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        
        usuario_entra_no_sistema(client, app)
        
        calendario = Calendario(ano_letivo=2026, data_inicio="2026-02-01", data_fim="2026-09-01", dias_letivos=50)
        db.session.add(calendario)
        db.session.commit()

        # Dados para atualização
        dados_atualizacao = {
            "ano_letivo": 2026,
            "data_inicio": "2026-02-01",
            "data_fim": "2026-09-15",
            "dias_letivos": 160
        }

        response = client.put(f'/calendario/{calendario.ano_letivo}', json=dados_atualizacao)
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Calendário atualizado com sucesso!"
        dados = response.json["data"]
        assert dados['ano_letivo'] == 2026, "O ano letivo do calendário deve ser 2026."
        assert dados['data_inicio'] == "2026-02-01", "A data de início do calendário deve ser '2026-02-01'."
        assert dados['data_fim'] == "2026-09-15", "A data de fim do calendário deve ser '2026-09-15'."
        assert dados['dias_letivos'] == 160, "A quantidade de dias letivos do calendário deve ser 160."


def test_deletar_calendario(client, app):
    """Testa a exclusão de um calendário.

    Este teste verifica se a requisição DELETE para a rota '/calendario/{ano_letivo}' retorna o status code 200 (OK)
    e se a resposta contém uma mensagem de sucesso.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        
        usuario_entra_no_sistema(client, app)
        
        calendario = Calendario(ano_letivo=2026, data_inicio="2026-02-01", data_fim="2026-09-01", dias_letivos=50)
        db.session.add(calendario)
        db.session.commit()

        response = client.delete(f'/calendario/{calendario.ano_letivo}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Calendário deletado com sucesso!"