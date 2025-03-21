"""
Este módulo contém testes para as rotas e as operações relacionadas a classe de controle `turma_controller`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o controle `turma_controller`,
incluindo cadastro, listagem, busca, atualização e remoção de turmas no banco de dados.
"""

from app.models import Turma, Sala, Calendario
from app.extensions import db
from app.utils.date_helpers import string_para_data
from tests.user_event import usuario_entra_no_sistema


def criar_dependencias(app):
    """ Garante que instâncias das entidades `Sala` e `Calendario` estejam disponíveis para 
    que testes na classe `Turma` possam ser feitos.
    """
    with app.app_context():
        with db.session.no_autoflush:
            # Garante que a sala existe
            if not Sala.query.filter_by(numero=101).first():
                sala = Sala(numero=101, capacidade=50, localizacao="Bloco A, 1° andar")
                db.session.add(sala)

            # Garante que o calendário existe
            if not Calendario.query.filter_by(ano_letivo=2026).first():
                calendario = Calendario(ano_letivo=2026, data_inicio=string_para_data("2026-02-17"), data_fim=string_para_data("2026-11-27"), dias_letivos=150)
                db.session.add(calendario)

            db.session.commit()

def criar_dependencia_calendario(app):
    """ Garante que a instância da entidade `Calendario` esteja disponível para 
    que testes na classe `Turma` possam ser feitos.
    """
    with app.app_context():
        with db.session.no_autoflush:
            # Garante que o calendário existe
            if not Calendario.query.filter_by(ano_letivo=2026).first():
                calendario = Calendario(ano_letivo = 2026, data_inicio=string_para_data("2026-02-17"), data_fim=string_para_data("2026-11-27"), dias_letivos=150)
                db.session.add(calendario)

            db.session.commit()

def criar_dependencia_sala(app):
    """ Garante que a instância da entidade `Sala` esteja disponível para 
    que testes na classe `Turma` possam ser feitos.
    """
    with app.app_context():
        with db.session.no_autoflush:
            # Garante que a sala existe
            if not Sala.query.filter_by(numero=101).first():
                sala = Sala(numero=101, capacidade=50, localizacao="Bloco A, 1° andar")
                db.session.add(sala)

            db.session.commit()

def test_cadastrar_turma(client, app):
    """Testa o cadastro de uma turma com dados válidos.

    Este teste verifica se:
    1. A requisição POST para a rota '/turma' retorna o status code 201 (Created).
    2. A resposta contém uma mensagem indicando sucesso.
    3. Os dados da turma cadastrada são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        dados_validos = {
            "ano": 9,
            "serie": "A",
            "nivel_de_ensino": "Ensino Fundamental",
            "turno": "M",
            "turno": "M",
            "status": "A",
            "sala_numero": 101,
            "calendario_ano_letivo": 2026
        }

        response = client.post('/turma/', json=dados_validos)

        print("Resposta da API:", response.json)

        assert response.status_code == 201, "O status code deve ser 201 (Created)."
        assert "mensagem" in response.json, "A resposta deve conter uma mensagem."
        assert "data" in response.json, "A resposta deve conter os dados da turma."
        
        turma = response.json["data"]
        
        assert "id" in turma, "A resposta deve conter o campo 'id'."
        assert turma["ano"] == 9, "O ano da turma deve ser 9."
        assert turma["serie"] == "A", "A serie da turma deve ser A."
        assert turma["nivel_de_ensino"] == "Ensino Fundamental", "O nivel de ensino da turma deve ser 'Ensino Fundamental'."
        assert turma["turno"] == "M", "O turno da turma deve ser M."
        assert turma["turno"] == "M", "O turno da turma deve ser M."
        assert turma["status"] == "A", "O status da turma deve ser A."
        assert turma["sala_numero"] == 101, "O numero da sala da turma deve ser 101."
        assert turma["calendario_ano_letivo"] == 2026, "O calendario do ano letivo deve ser 2026."

def test_cadastrar_turma_calendario_inexistente(client, app):
    """Testa o cadastro de uma turma com dado calendário inexistente.

    Este teste verifica se:
    1. A requisição POST para a rota '/turma' retorna o status code 400 (Bad Request).
    2. A resposta contém uma mensagem indicando "Calendário não existe".
    3. Os dados da turma cadastrada são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencia_sala(app)
        usuario_entra_no_sistema(client, app)

        dados_validos = {
            "ano": 9,
            "serie": "A",
            "nivel_de_ensino": "Ensino Fundamental",
            "turno": "M",
            "turno": "M",
            "status": "A",
            "sala_numero": 101,
            "calendario_ano_letivo": 2026
        }

        response = client.post('/turma/', json=dados_validos)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "Calendário não existe"

def test_cadastrar_turma_sala_inexistente(client, app):
    """Testa o cadastro de uma turma com dado sala inexistente.

    Este teste verifica se:
    1. A requisição POST para a rota '/turma' retorna o status code 400 (Bad Request).
    2. A resposta contém uma mensagem indicando "Sala não existe".
    3. Os dados da turma cadastrada são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencia_calendario(app)
        usuario_entra_no_sistema(client, app)

        dados_validos = {
            "ano": 9,
            "serie": "A",
            "nivel_de_ensino": "Ensino Fundamental",
            "turno": "M",
            "turno": "M",
            "status": "A",
            "sala_numero": 101,
            "calendario_ano_letivo": 2026
        }

        response = client.post('/turma/', json=dados_validos)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "Sala não existe"

def test_cadastrar_turma_dados_invalidos(client, app):
    """Testa o cadastro de uma turma com dados inválidos.

    Este teste verifica se a requisição POST para a rota '/turma' retorna o status code 400 (Bad Request)
    e se a resposta contém mensagens de erro para cada campo inválido.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        dados_invalidos = {
            "ano": 13,
            "serie": "Aberta",
            "nivel_de_ensino": "Ensino Fundamental",
            "turno": "D",
            "status": "A",
            "sala_numero": 101,
            "calendario_ano_letivo": 2026
        }

        response = client.post('/turma/', json=dados_invalidos)
        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 3, "Deve haver 3 erros de validação."


def test_cadastrar_turma_com_horario_invalido(client, app):
    """Testa o cadastro de uma turma em uma horário que já existe outra turma.

    Este teste verifica se a requisição POST para a rota '/turma' retorna o status code 400 (Bad Request)
    e se a resposta contém mensagens de erro de que o horário da turma está ocupado.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="M", status="A", sala_numero=101, calendario_ano_letivo=2026)
        turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="M", status="A", sala_numero=101, calendario_ano_letivo=2026)
        db.session.add(turma)
        db.session.commit()

        dados_invalidos = {
            "ano": 1,
            "serie": "A",
            "nivel_de_ensino": "Ensino Fundamental",
            "turno": "M",
            "turno": "M",
            "status": "A",
            "sala_numero": 101,
            "calendario_ano_letivo": 2026
        }

        response = client.post('/turma/', json=dados_invalidos)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert "Já existe uma turma no mesmo horário" in response.json["erro"], "Deve retornar uma mensagem de erro no horário"


def test_listar_turmas(client, app):
    """Testa a listagem de turmas cadastradas.

    Este teste verifica se a requisição GET para a rota '/turma/' retorna o status code 200 (OK)
    e se a resposta contém uma lista com as turmas cadastradas.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="N", status="A", sala_numero=101, calendario_ano_letivo=2026)
        db.session.add(turma)
        db.session.commit()

        response = client.get('/turma/')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, list), "A resposta deve ser uma lista."
        assert len(response.json) == 1, "Deve haver exatamente 1 turma na listagem."
        assert "id" in response.json[0], "A resposta deve conter o campo 'id'."
        

def test_buscar_turma(client, app):
    """Testa a busca de uma turma específica pelo número.

    Este teste verifica se a requisição GET para a rota '/turma/{id}' retorna o status code 200 (OK)
    e se a resposta contém os dados corretos da turma buscada.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="V", status="A", sala_numero=101, calendario_ano_letivo=2026)
        db.session.add(turma)
        db.session.commit()

        response = client.get(f'/turma/{turma.id}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, dict), "A resposta deve ser um dicionário."
        dados = response.json
        assert "id" in dados, "A resposta deve conter o campo 'id'."
        assert dados["ano"] == 9, "O ano da turma deve ser 9."
        assert dados["serie"] == "A", "A serie da turma deve ser A."
        assert dados["nivel_de_ensino"] == "Ensino Fundamental", "O nivel de ensino da turma deve ser 'Ensino Fundamental'."
        assert dados["turno"] == "V", "O turno da turma deve ser V."
        assert dados["status"] == "A", "O status da turma deve ser A."
        assert dados["sala_numero"] == 101, "O numero da sala da turma deve ser 101."
        assert dados["calendario_ano_letivo"] == 2026, "O calendario do ano letivo deve ser 2026."


def test_alterar_turma(client, app):
    """Testa a atualização dos dados de uma turma.

    Este teste verifica se a requisição PUT para a rota '/turma/{id}' retorna o status code 200 (OK),
    se a resposta contém uma mensagem de sucesso e se os dados da turma foram atualizados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="M", status="A", sala_numero=101, calendario_ano_letivo=2026)
        turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="M", status="A", sala_numero=101, calendario_ano_letivo=2026)
        db.session.add(turma)
        db.session.commit()

        # Dados para atualização
        dados_atualizacao = {
            "ano": 9,
            "serie": "M",
            "nivel_de_ensino": "Ensino Fundamental",
            "turno": "N",
            "status": "A",
            "sala_numero": 101,
            "calendario_ano_letivo": 2026
        }

        response = client.put(f'/turma/{turma.id}', json=dados_atualizacao)
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Turma atualizada com sucesso!"
        dados = response.json["data"]
        assert dados["ano"] == 9, "O ano da turma deve ser 9."
        assert dados["serie"] == "M", "A serie da turma deve ser M."
        assert dados["nivel_de_ensino"] == "Ensino Fundamental", "O nivel de ensino da turma deve ser 'Ensino Fundamental'."
        assert dados["turno"] == "N", "O turno da turma deve ser N."
        assert dados["status"] == "A", "O status da turma deve ser A."
        assert dados["sala_numero"] == 101, "O numero da sala da turma deve ser 101."
        assert dados["calendario_ano_letivo"] == 2026, "O calendario do ano letivo deve ser 2026."


def test_deletar_turma(client, app):
    """Testa a exclusão de uma turma.

    Este teste verifica se a requisição DELETE para a rota '/turma/{id}' retorna o status code 200 (OK)
    e se a resposta contém uma mensagem de sucesso.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        turma = Turma(ano=9, serie="A", nivel_de_ensino="Fundamental", turno="M", status="A", sala_numero=101, calendario_ano_letivo=2026)
        turma = Turma(ano=9, serie="A", nivel_de_ensino="Fundamental", turno="M", status="A", sala_numero=101, calendario_ano_letivo=2026)
        db.session.add(turma)
        db.session.commit()

        response = client.delete(f'/turma/{turma.id}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Turma deletada com sucesso!"