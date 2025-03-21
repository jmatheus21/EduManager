"""
Este módulo contém testes para as rotas e as operações relacionadas a classe de controle `aula_controller`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o controle `aula_controller`,
incluindo cadastro, listagem, busca, atualização e remoção de aulas no banco de dados.
"""

from app.models import Aula, Usuario, Disciplina, Turma, Calendario, Sala
from app.extensions import db
from app.utils.date_helpers import string_para_data
from app.utils.hour_helpers import string_para_hora


def criar_dependencias(app):
    """ Garante que instâncias das entidades `Usuario`, `Disciplina` e `Turma` estejam disponíveis para 
    que testes na classe `aula` possam ser feitos.
    """
    with app.app_context():
        with db.session.no_autoflush:
            # Garante que o usuário existe
            if not Usuario.query.filter_by(cpf=12345678912).first():
                usuario = Usuario(cpf=12345678912, nome="Alan Ferreira dos Santos", senha="bocaAberta123", telefone="79 9 9999-8888", endereco="Bairro X, Rua A",horario_de_trabalho="Seg-Sex,7h-12h", data_de_nascimento="1998-05-17", tipo="p", formacao="Licenciatura em Matemática", escolaridade= None, habilidades= None, disciplinas= ["MAT123", "FIS789"], cargos=[2])
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

        dados_validos = {
            "ano": 9,
            "serie": "A",
            "nivel_de_ensino": "Ensino Fundamental",
            "turno": "D",
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
        assert turma["turno"] == "D", "O turno da turma deve ser D."
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

        dados_validos = {
            "ano": 9,
            "serie": "A",
            "nivel_de_ensino": "Ensino Fundamental",
            "turno": "D",
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

        dados_validos = {
            "ano": 9,
            "serie": "A",
            "nivel_de_ensino": "Ensino Fundamental",
            "turno": "D",
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

        dados_invalidos = {
            "ano": 13,
            "serie": "Aberta",
            "nivel_de_ensino": "Ensino Fundamental",
            "turno": "",
            "status": "A",
            "sala_numero": 101,
            "calendario_ano_letivo": 2026
        }

        response = client.post('/turma/', json=dados_invalidos)
        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 4, "Deve haver 3 erros de validação."

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

        turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="D", status="A", sala_numero=101, calendario_ano_letivo=2026)
        db.session.add(turma)
        db.session.commit()

        dados_invalidos = {
            "ano": 1,
            "serie": "A",
            "nivel_de_ensino": "Ensino Fundamental",
            "turno": "D",
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

        turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="D", status="A", sala_numero=101, calendario_ano_letivo=2026)
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

        turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="D", status="A", sala_numero=101, calendario_ano_letivo=2026)
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
        assert dados["turno"] == "D", "O turno da turma deve ser D."
        assert dados["status"] == "A", "O status da turma deve ser A."
        assert dados["sala_numero"] == 101, "O numero da sala da turma deve ser 101."
        assert dados["calendario_ano_letivo"] == 2026, "O calendario do ano letivo deve ser 2026."


# def test_alterar_aula(client, app):
#     """Testa a atualização dos dados de uma aula.

#     Este teste verifica se a requisição PUT para a rota '/aula/{id}' retorna o status code 200 (OK),
#     se a resposta contém uma mensagem de sucesso e se os dados da aula foram atualizados corretamente.

#     Args:
#         client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
#         app (Flask): Aplicação Flask para acessar o contexto da aplicação.
#     """
#     with app.app_context():
#         criar_dependencias(app)


# def test_deletar_aula(client, app):
#     """Testa a exclusão de uma aula.

#     Este teste verifica se a requisição DELETE para a rota '/aula/{id}' retorna o status code 200 (OK)
#     e se a resposta contém uma mensagem de sucesso.

#     Args:
#         client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
#         app (Flask): Aplicação Flask para acessar o contexto da aplicação.
#     """
#     with app.app_context():
#         criar_dependencias(app)