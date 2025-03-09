"""
Este módulo contém testes para as rotas e as operações relacionadas a classe de controle `disciplina_controller`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o controle `disciplina_controller`,
incluindo cadastro, listagem, busca, atualização e remoção de disciplinas no banco de dados.
"""

from app.models import Disciplina
from app.extensions import db


def test_cadastrar_disciplina(client, app):
    """Testa o cadastro de uma disciplina com dados válidos.

    Este teste verifica se:
    1. A requisição POST para a rota '/disciplina' retorna o status code 201 (Created).
    2. A resposta contém uma mensagem indicando sucesso.
    3. Os dados da disciplina cadastrada são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        dados_validos = {
            "codigo": "MAT001", 
            "nome": "Matemática",
            "carga_horaria": 30,
            "ementa": "Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.",
            "bibliografia": "STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014."
        } 

        response = client.post('/disciplina/', json=dados_validos)

        assert response.status_code == 201, "O status code deve ser 201 (Created)."
        assert "mensagem" in response.json, "A resposta deve conter uma mensagem."
        assert "data" in response.json, "A resposta deve conter os dados da disciplina."
        disciplina = response.json["data"]
        assert disciplina["codigo"] == "MAT001", "O código da disciplina deve ser MAT001."
        assert disciplina["nome"] == "Matemática", "O nome da disciplina deve ser Matemática."
        assert disciplina["carga_horaria"] == 30, "A carga-horária da disciplina deve ser 30."
        assert disciplina["ementa"] == "Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", "A ementa da disciplina deve ser Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos."
        assert disciplina["bibliografia"] == "STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014.", "A bibliografia da disciplina deve ser STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014."


def test_cadastrar_disciplina_dados_invalidos(client, app):
    """Testa o cadastro de uma disciplina com dados inválidos.

    Este teste verifica se a requisição POST para a rota '/disciplina' retorna o status code 400 (Bad Request)
    e se a resposta contém mensagens de erro para cada campo inválido.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        dados_invalidos = {
            "codigo": "MMAATT000011", 
            "nome": "Ma", 
            "carga_horaria": 10,
            "ementa": "",
            "bibliografia": "" 
        }

        response = client.post('/disciplina/', json=dados_invalidos)
        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 3, "Deve haver 3 erros de validação."


def test_listar_disciplina(client, app):
    """Testa a listagem de disciplinas cadastradas.

    Este teste verifica se a requisição GET para a rota '/disciplina/' retorna o status code 200 (OK)
    e se a resposta contém uma lista com as disciplinas cadastradas.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014.")
        db.session.add(disciplina)
        db.session.commit()

        response = client.get('/disciplina/')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, list), "A resposta deve ser uma lista."
        assert len(response.json) == 1, "Deve haver exatamente 1 disciplina na listagem."
        assert response.json[0]["codigo"] == "MAT001", "O código da disciplina deve ser MAT001."


def test_buscar_disciplina(client, app):
    """Testa a busca de uma disciplina específica pelo código.

    Este teste verifica se a requisição GET para a rota '/disciplina/{codigo}' retorna o status code 200 (OK)
    e se a resposta contém os dados corretos da disciplina buscada.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014.")
        db.session.add(disciplina)
        db.session.commit()

        response = client.get(f'/disciplina/{disciplina.codigo}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, dict), "A resposta deve ser um dicionário."
        dados = response.json
        assert dados['codigo'] == "MAT001"
        assert dados['nome'] == "Matemática"
        assert dados['carga_horaria'] == 30
        assert dados['ementa'] == "Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos."
        assert dados['bibliografia'] == "bibliografia", "STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014."


def test_alterar_disciplina(client, app):
    """Testa a atualização dos dados de uma disciplina.

    Este teste verifica se a requisição PUT para a rota '/disciplina/{codigo}' retorna o status code 200 (OK),
    se a resposta contém uma mensagem de sucesso e se os dados da disciplina foram atualizados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014.")
        db.session.add(disciplina)
        db.session.commit()

        # Dados para atualização
        dados_atualizacao = {
            "codigo": "MAT001",
            "nome": "Matemática",
            "carga_horaria": 120,
            "ementa": "Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.",
            "bibliografia": "STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014."
        }

        response = client.put(f'/disciplina/{disciplina.codigo}', json=dados_atualizacao)
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Disciplina atualizada com sucesso!"
        dados = response.json["data"]
        assert dados['codigo'] == "MAT001", "O código da disciplina deve ser MAT001."
        assert dados['nome'] == "Matemática", "O nome da disciplina deve ser Matemática."
        assert dados['carga_horaria'] == 120, "A carga-horária da disciplina deve ser 120."
        assert dados['ementa'] == "Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", "A ementa da disciplina deve ser Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos."
        assert dados['bibliografia'] == "STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014.", "A bibliografia da disciplina deve ser STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014."


def test_deletar_disciplina(client, app):
    """Testa a exclusão de uma disciplina.

    Este teste verifica se a requisição DELETE para a rota '/disciplina/{codigo}' retorna o status code 200 (OK)
    e se a resposta contém uma mensagem de sucesso.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=120, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro: Zahar, 2014.")
        db.session.add(disciplina)
        db.session.commit()

        response = client.delete(f'/disciplina/{disciplina.codigo}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Disciplina deletada com sucesso!"