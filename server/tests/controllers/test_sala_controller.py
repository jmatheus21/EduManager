"""
Este módulo contém testes para as rotas e as operações relacionadas a classe de controle `sala_controller`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o controle `sala_controller`,
incluindo cadastro, listagem, busca, atualização e remoção de salas no banco de dados.
"""

from app.models import Sala, Calendario, Turma
from app.extensions import db


def test_cadastrar_sala(client, app):
    """Testa o cadastro de uma sala com dados válidos.

    Este teste verifica se:
    1. A requisição POST para a rota '/sala' retorna o status code 201 (Created).
    2. A resposta contém uma mensagem indicando sucesso.
    3. Os dados da sala cadastrada são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        dados_validos = {
            "numero": 101,
            "capacidade": 30,
            "localizacao": "Bloco A, 1º Andar"
        }

        response = client.post('/sala/', json=dados_validos)

        assert response.status_code == 201, "O status code deve ser 201 (Created)."
        assert "mensagem" in response.json, "A resposta deve conter uma mensagem."
        assert "data" in response.json, "A resposta deve conter os dados da sala."
        sala = response.json["data"]
        assert sala["numero"] == 101, "O número da sala deve ser 101."
        assert sala["capacidade"] == 30, "A capacidade da sala deve ser 30."
        assert sala["localizacao"] == "Bloco A, 1º Andar", "A localização da sala deve ser 'Bloco A, 1º Andar'."

def test_cadastrar_sala_calendario_ine(client, app):
    """Testa o cadastro de uma sala com dados válidos.

    Este teste verifica se:
    1. A requisição POST para a rota '/sala' retorna o status code 201 (Created).
    2. A resposta contém uma mensagem indicando sucesso.
    3. Os dados da sala cadastrada são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        dados_validos = {
            "numero": 101,
            "capacidade": 30,
            "localizacao": "Bloco A, 1º Andar"
        }

        response = client.post('/sala/', json=dados_validos)

        assert response.status_code == 201, "O status code deve ser 201 (Created)."
        assert "mensagem" in response.json, "A resposta deve conter uma mensagem."
        assert "data" in response.json, "A resposta deve conter os dados da sala."
        sala = response.json["data"]
        assert sala["numero"] == 101, "O número da sala deve ser 101."
        assert sala["capacidade"] == 30, "A capacidade da sala deve ser 30."
        assert sala["localizacao"] == "Bloco A, 1º Andar", "A localização da sala deve ser 'Bloco A, 1º Andar'."



def test_cadastrar_sala_dados_invalidos(client, app):
    """Testa o cadastro de uma sala com dados inválidos.

    Este teste verifica se a requisição POST para a rota '/sala' retorna o status code 400 (Bad Request)
    e se a resposta contém mensagens de erro para cada campo inválido.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        dados_invalidos = {
            "numero": 0, 
            "capacidade": -10, 
            "localizacao": ""
        }

        response = client.post('/sala/', json=dados_invalidos)
        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 3, "Deve haver 3 erros de validação."


def test_listar_salas(client, app):
    """Testa a listagem de salas cadastradas.

    Este teste verifica se a requisição GET para a rota '/sala/' retorna o status code 200 (OK)
    e se a resposta contém uma lista com as salas cadastradas.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        sala = Sala(numero=101, capacidade=30, localizacao="Bloco A, 1º Andar")
        db.session.add(sala)
        db.session.commit()

        response = client.get('/sala/')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, list), "A resposta deve ser uma lista."
        assert len(response.json) == 1, "Deve haver exatamente 1 sala na listagem."
        assert response.json[0]["numero"] == 101, "O número da sala deve ser 101."


def test_buscar_sala(client, app):
    """Testa a busca de uma sala específica pelo número.

    Este teste verifica se a requisição GET para a rota '/sala/{numero}' retorna o status code 200 (OK)
    e se a resposta contém os dados corretos da sala buscada.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        sala = Sala(numero=101, capacidade=30, localizacao="Bloco A, 1º Andar")
        db.session.add(sala)
        db.session.commit()

        response = client.get(f'/sala/{sala.numero}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, dict), "A resposta deve ser um dicionário."
        dados = response.json
        assert dados['numero'] == 101
        assert dados['capacidade'] == 30
        assert dados['localizacao'] == "Bloco A, 1º Andar"


def test_alterar_sala(client, app):
    """Testa a atualização dos dados de uma sala.

    Este teste verifica se a requisição PUT para a rota '/sala/{numero}' retorna o status code 200 (OK),
    se a resposta contém uma mensagem de sucesso e se os dados da sala foram atualizados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        sala = Sala(numero=101, capacidade=30, localizacao="Bloco A, 1º Andar")
        db.session.add(sala)
        db.session.commit()

        # Dados para atualização
        dados_atualizacao = {
            "numero": 101,
            "capacidade": 40,
            "localizacao": "Bloco A, 2º Andar"
        }

        response = client.put(f'/sala/{sala.numero}', json=dados_atualizacao)
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Sala atualizada com sucesso!"
        dados = response.json["data"]
        assert dados['numero'] == 101, "O número da sala deve ser 101."
        assert dados['capacidade'] == 40, "A capacidade da sala deve ser 40."
        assert dados['localizacao'] == "Bloco A, 2º Andar", "A localização da sala deve ser 'Bloco A, 2º Andar'."


# def test_deletar_sala(client, app):
#     """Testa a exclusão de uma sala.

#     Este teste verifica se a requisição DELETE para a rota '/sala/{numero}' retorna o status code 200 (OK)
#     e se a resposta contém uma mensagem de sucesso.

#     Args:
#         client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
#         app (Flask): Aplicação Flask para acessar o contexto da aplicação.
#     """
#     with app.app_context():
#         sala = Sala(numero=101, capacidade=30, localizacao="Bloco A, 1º Andar")
#         db.session.add(sala)
#         db.session.commit()

#         response = client.delete(f'/sala/{sala.numero}')
#         assert response.status_code == 200, "O status code deve ser 200 (OK)."
#         assert response.json["mensagem"] == "Sala deletada com sucesso!"


def test_deletar_sala_valido(client, app):
    """Testa a exclusão de uma sala.

    Este teste verifica se a requisição DELETE para a rota '/sala/{numero}' retorna o status code 200 (OK)
    e se a resposta contém uma mensagem de sucesso.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        sala = Sala(numero=101, capacidade=30, localizacao="Bloco A, 1º Andar")
        db.session.add(sala)
        db.session.commit()

        calendario = Calendario(ano_letivo = 2026, data_inicio = "2026-01-15", data_fim = "2026-09-15", dias_letivos = 150)
        db.session.add(calendario)
        db.session.commit()

        turmaDaManha = Turma(ano = 1, serie = 'A', nivel_ensino = 'Fundamental',turno = 'M', status ='C', sala_numero = 101, calendario_ano_letivo = 2026)
        turmaDaTarde = Turma(ano = 1, serie = 'A', nivel_ensino = 'Fundamental',turno = 'V', status ='C', sala_numero = 101, calendario_ano_letivo = 2026)
        db.session.add(turmaDaManha, turmaDaTarde)
        db.session.commit()

        response = client.delete(f'/sala/{sala.numero}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Sala deletada com sucesso!"

def test_deletar_sala_turmas_ativas(client, app):
    """Testa a exclusão de uma sala com turmas ativas.

    Este teste verifica se a requisição DELETE para a rota '/sala/{numero}' retorna o status code 400
    e se a resposta contém uma mensagem de erro.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        sala = Sala(numero=101, capacidade=30, localizacao="Bloco A, 1º Andar")
        db.session.add(sala)
        db.session.commit()

        calendario = Calendario(ano_letivo = 2026, data_inicio = "2026-01-15", data_fim = "2026-09-15", dias_letivos = 150)
        db.session.add(calendario)
        db.session.commit()

        turmaDaManha = Turma(ano = 1, serie = 'A', nivel_ensino = 'Fundamental',turno = 'M', status ='C', sala_numero = 101, calendario_ano_letivo = 2026)
        turmaDaTarde = Turma(ano = 1, serie = 'A', nivel_ensino = 'Fundamental',turno = 'V', status ='A', sala_numero = 101, calendario_ano_letivo = 2026)
        db.session.add_all([turmaDaManha, turmaDaTarde])
        db.session.commit()

        response = client.delete(f'/sala/{sala.numero}')
        assert response.status_code == 400, "O status code deve ser 400"
        assert response.json["erro"] == "Não é possível remover a sala, pois há turmas ativas associadas a essa sala"