"""
Este módulo contém testes para as rotas e as operações relacionadas a classe de controle `aula_controller`.

Os testes verificam as operações básicas de CRUD (Create, Read, Update, Delete) para o controle `aula_controller`,
incluindo cadastro, listagem, busca, atualização e remoção de aulas no banco de dados.
"""

from app.models import Aula, Usuario, Disciplina, Turma, Calendario, Sala, Cargo
from app.extensions import db
from app.utils.date_helpers import string_para_data
from app.utils.hour_helpers import string_para_hora
from app.utils.usuario_helpers import gerar_hashing
from tests.user_event import usuario_entra_no_sistema


def criar_dependencias(app):
    """ Garante que instâncias das entidades `Usuario`, `Disciplina` e `Turma` estejam disponíveis para 
    que testes na classe `aula` possam ser feitos.
    """
    with app.app_context():
        with db.session.no_autoflush:
            # Garante que a disciplina existe
            if not Disciplina.query.filter_by(codigo="MAT001").first():
                disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro:Zahar, 2014.")
                db.session.add(disciplina)
            
            # Garante que o usuário existe
            cargo = Cargo(nome="Professor", salario=2060.0, data_contrato="2027-12-31")
            if not Usuario.query.filter_by(id=1).first():
                usuario = Usuario(cpf="12345678910", nome="Alan Ferreira dos Santos", email="alanferreira@email.com", senha=gerar_hashing("bocaAberta123"), telefone="79 9 9999-8888", endereco="Bairro X, Rua A", horario_de_trabalho="Seg-Sex,7h-12h", data_de_nascimento=string_para_data("1998-05-17"), tipo="p", formacao="Licenciatura em Matemática", escolaridade= None, habilidades= None, disciplinas= [disciplina], cargos=[cargo])
                db.session.add(usuario)

            # Garante que a turma existe
            if not Turma.query.filter_by(id=1).first():
                calendario = Calendario(ano_letivo = 2026, data_inicio=string_para_data("2026-02-17"), data_fim=string_para_data("2026-11-27"), dias_letivos=150)
                db.session.add(calendario)
                sala = Sala(numero=101, capacidade=50, localizacao="Bloco A, 1° andar")
                db.session.add(sala)
                turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="M", status="A", sala_numero= 101, calendario_ano_letivo= 2026)
                db.session.add(turma)

            db.session.commit()


def criar_dependencias_segunda_disciplina(app):
    """ Garante que instâncias das entidades `Usuario`, `Disciplina` e `Turma` estejam disponíveis para 
    que testes na classe `aula` possam ser feitos. 

    A criação desta dependência garante que o teste de cadastro de aula no mesmo horário, com o mesmo professor, seja feito.
    """
    with app.app_context():
        with db.session.no_autoflush:
            # Garante que a disciplina existe
            if not Disciplina.query.filter_by(codigo="MAT002").first():
                disciplina = Disciplina(codigo="MAT002", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro:Zahar, 2014.")
                db.session.add(disciplina)
            
            # Garante que o usuário existe
            cargo = Cargo(nome="Professor", salario=2060.0, data_contrato="2027-12-31")
            if not Usuario.query.filter_by(id=1).first():
                usuario = Usuario(cpf="12345678910", nome="Alan Ferreira dos Santos", email="alanferreira@email.com", senha=gerar_hashing("bocaAberta123"), telefone="79 9 9999-8888", endereco="Bairro X, Rua A", horario_de_trabalho="Seg-Sex,7h-12h", data_de_nascimento=string_para_data("1998-05-17"), tipo="p", formacao="Licenciatura em Matemática", escolaridade= None, habilidades= None, disciplinas= [disciplina], cargos=[cargo])
                db.session.add(usuario)

            # Garante que a turma existe
            if not Turma.query.filter_by(id=1).first():
                calendario = Calendario(ano_letivo = 2026, data_inicio=string_para_data("2026-02-17"), data_fim=string_para_data("2026-11-27"), dias_letivos=150)
                db.session.add(calendario)
                sala = Sala(numero=101, capacidade=50, localizacao="Bloco A, 1° andar")
                db.session.add(sala)
                turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="M", status="A", sala_numero= 101, calendario_ano_letivo= 2026)
                db.session.add(turma)

            db.session.commit()


def criar_dependencias_usuario(app):
    """ Garante que a instância das entidades `Usuario` esteja disponível para 
    que testes na classe `aula` possam ser feitos.
    """
    with app.app_context():
        with db.session.no_autoflush:
            # Garante que a disciplina existe
            if not Disciplina.query.filter_by(codigo="MAT001").first():
                disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro:Zahar, 2014.")
                db.session.add(disciplina)
            
            # Garante que o usuário existe
            cargo = Cargo(nome="Professor", salario=2060.0, data_contrato="2027-12-31")
            if not Usuario.query.filter_by(id=1).first():
                usuario = Usuario(cpf="12345678910", nome="Alan Ferreira dos Santos", email="alanferreira@email.com", senha=gerar_hashing("bocaAberta123"), telefone="79 9 9999-8888", endereco="Bairro X, Rua A", horario_de_trabalho="Seg-Sex,7h-12h", data_de_nascimento=string_para_data("1998-05-17"), tipo="p", formacao="Licenciatura em Matemática", escolaridade= None, habilidades= None, disciplinas= [disciplina], cargos=[cargo])
                db.session.add(usuario)

            db.session.commit()


def criar_dependencias_disciplina(app):
    """ Garante que a instâncias das entidades `Disciplina` esteja disponível para 
    que testes na classe `aula` possam ser feitos.
    """
    with app.app_context():
        with db.session.no_autoflush:
            # Garante que a disciplina existe
            if not Disciplina.query.filter_by(codigo="MAT001").first():
                disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro:Zahar, 2014.")
                db.session.add(disciplina)
            
            db.session.commit()


def criar_dependencias_turma(app):
    """ Garante que instâncias da entidade `Turma` esteja disponível para 
    que testes na classe `aula` possam ser feitos.
    """
    with app.app_context():
        with db.session.no_autoflush:
            # Garante que a turma existe
            if not Turma.query.filter_by(id=1).first():
                calendario = Calendario(ano_letivo = 2026, data_inicio=string_para_data("2026-02-17"), data_fim=string_para_data("2026-11-27"), dias_letivos=150)
                db.session.add(calendario)
                sala = Sala(numero=101, capacidade=50, localizacao="Bloco A, 1° andar")
                db.session.add(sala)
                turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="M", status="A", sala_numero= 101, calendario_ano_letivo= 2026)
                db.session.add(turma)

            db.session.commit()


def test_cadastrar_aula(client, app):
    """Testa o cadastro de uma aula com dados válidos.

    Este teste verifica se:
    1. A requisição POST para a rota '/aula' retorna o status code 201 (Created).
    2. A resposta contém uma mensagem indicando sucesso.
    3. Os dados da aula cadastrada são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        dados_validos = {
            "hora_inicio": "13:00",
            "hora_fim": "15:00",
            "dias_da_semana": ["Segunda"],
            "usuario_cpf": "12345678910",
            "disciplina_codigo": "MAT001",
            "turma_id": 1
        }

        response = client.post('/aula/', json=dados_validos)

        print("Resposta da API:", response.json)

        assert response.status_code == 201, "O status code deve ser 201 (Created)."
        assert "mensagem" in response.json, "A resposta deve conter uma mensagem."
        assert "data" in response.json, "A resposta deve conter os dados da aula."
        
        aula = response.json["data"]
        
        assert "id" in aula, "A resposta deve conter o campo 'id'."
        assert aula["hora_inicio"] == "13:00:00", "O horário de início da aula deve ser '13:00:00'."
        assert aula["hora_fim"] == "15:00:00", "O horário de fim da aula deve ser '15:00:00'."
        assert aula["dias_da_semana"] == ["Segunda"], "O dia da semana deve ser '['Segunda']'."
        assert aula["usuario_id"] == 1, "O id do usuário deve ser 1."
        assert aula["disciplina_codigo"] == "MAT001", "O código da disciplina deve ser 'MAT001'."
        assert aula["turma_id"] == 1, "O id da turma deve ser 1."


def test_cadastrar_aula_usuario_inexistente(client, app):
    """Testa o cadastro de uma aula com dado usuário inexistente.

    Este teste verifica se:
    1. A requisição POST para a rota '/aula' retorna o status code 400 (Bad Request).
    2. A resposta contém uma mensagem indicando "Usuário não existe".
    3. Os dados da aula cadastrada são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias_disciplina(app)
        criar_dependencias_turma(app)
        usuario_entra_no_sistema(client, app)

        dados_validos = {
            "hora_inicio": "13:00:00",
            "hora_fim": "15:00:00",
            "dias_da_semana": "Segunda",
            "usuario_cpf": "12345678911",
            "disciplina_codigo": "MAT001",
            "turma_id": 1
        }

        response = client.post('/aula/', json=dados_validos)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "Usuário não existe"


def test_cadastrar_aula_disciplina_inexistente(client, app):
    """Testa o cadastro de uma aula com dado disciplina inexistente.

    Este teste verifica se:
    1. A requisição POST para a rota '/aula' retorna o status code 400 (Bad Request).
    2. A resposta contém uma mensagem indicando "Disciplina não existe".
    3. Os dados da aula cadastrada são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias_usuario(app)
        criar_dependencias_turma(app)
        usuario_entra_no_sistema(client, app)
        
        dados_validos = {
            "hora_inicio": "08:00:00",
            "hora_fim": "09:00:00",
            "dias_da_semana": "Segunda",
            "usuario_cpf": "12345678910",
            "disciplina_codigo": "MAT001",
            "turma_id": 1
        }

        response = client.post('/aula/', json=dados_validos)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "Disciplina não existe"


def test_cadastrar_aula_turma_inexistente(client, app):
    """Testa o cadastro de uma aula com dado turma inexistente.

    Este teste verifica se:
    1. A requisição POST para a rota '/aula' retorna o status code 400 (Bad Request).
    2. A resposta contém uma mensagem indicando "Turma não existe".
    3. Os dados da aula cadastrada são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias_usuario(app)
        usuario_entra_no_sistema(client, app)
        
        dados_validos = {
            "hora_inicio": "08:00:00",
            "hora_fim": "09:00:00",
            "dias_da_semana": "Segunda",
            "usuario_cpf": "12345678910",
            "disciplina_codigo": "MAT001",
            "turma_id": 1
        }

        response = client.post('/aula/', json=dados_validos)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "Turma não existe"


def test_cadastrar_aula_dados_invalidos(client, app):
    """Testa o cadastro de uma aula com dados inválidos.

    Este teste verifica se a requisição POST para a rota '/aula' retorna o status code 400 (Bad Request)
    e se a resposta contém mensagens de erro para cada campo inválido.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        dados_invalidos = {
            "hora_inicio": "",
            "hora_fim": "",
            "dias_da_semana": "",
            "usuario_cpf": "12345678",
            "disciplina_codigo": "M01",
            "turma_id": 0
        }

        response = client.post('/aula/', json=dados_invalidos)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 6, "Deve haver 6 erros de validação."


def test_cadastrar_aula_no_mesmo_horario_com_mesmo_usuario(client, app):
    """Testa o cadastro de uma aula em uma horário que já existe outra aula com o mesmo usuário.

    Este teste verifica se a requisição POST para a rota '/aula' retorna o status code 400 (Bad Request)
    e se a resposta contém mensagens de erro de que o horário da aula está ocupado.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        criar_dependencias_segunda_disciplina(app)
        usuario_entra_no_sistema(client, app)

        aula = Aula(hora_inicio=string_para_hora("08:00:00"), hora_fim=string_para_hora("09:00:00"), dias_da_semana=["Segunda"], usuario_id=1, disciplina_codigo="MAT001", turma_id=1)
        db.session.add(aula)
        db.session.commit()

        dados_invalidos = {
            "hora_inicio": "08:00",
            "hora_fim": "09:00",
            "dias_da_semana": ["Segunda"],
            "usuario_cpf": "12345678910",
            "disciplina_codigo": "MAT002",
            "turma_id": 1
        }

        response = client.post('/aula/', json=dados_invalidos)

        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert "Já existe uma aula no mesmo horário, com o mesmo professor" in response.json["erro"], "Deve retornar uma mensagem de erro no horário, com o mesmo professor"


def test_listar_aulas(client, app):
    """Testa a listagem de aulas cadastradas.

    Este teste verifica se a requisição GET para a rota '/aula/' retorna o status code 200 (OK)
    e se a resposta contém uma lista com as aulas cadastradas.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        aula = Aula(hora_inicio=string_para_hora("08:00:00"), hora_fim=string_para_hora("09:00:00"), dias_da_semana=["Segunda"], usuario_id=1, disciplina_codigo="MAT001", turma_id=1)
        db.session.add(aula)
        db.session.commit()

        response = client.get('/aula/')

        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, list), "A resposta deve ser uma lista."
        assert len(response.json) == 1, "Deve haver exatamente 1 turma na listagem."
        assert "id" in response.json[0], "A resposta deve conter o campo 'id'."
        

def test_buscar_aula(client, app):
    """Testa a busca de uma aula específica pelo número.

    Este teste verifica se a requisição GET para a rota '/aula/{id}' retorna o status code 200 (OK)
    e se a resposta contém os dados corretos da aula buscada.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        aula = Aula(hora_inicio="08:00:00", hora_fim="09:00:00", dias_da_semana=["Segunda"], usuario_id=1, disciplina_codigo="MAT001", turma_id=1)
        db.session.add(aula)
        db.session.commit()

        response = client.get(f'/aula/{aula.id}')

        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, dict), "A resposta deve ser um dicionário."
        dados = response.json
        assert "id" in dados, "A resposta deve conter o campo 'id'."
        assert dados["hora_inicio"] == "08:00:00", "O horário de início da aula deve ser 08:00:00."
        assert dados["hora_fim"] == "09:00:00", "O horário de fim da aula deve ser 09:00:00."
        assert dados["dias_da_semana"] == ["Segunda"], "O dia da semana deve ser '['Segunda']'."
        assert dados["professor_id"] == 1, "O id do professor deve ser 1."
        assert dados["disciplina_codigo"] == "MAT001", "O código da disciplina deve ser 'MAT001'."
        assert dados["turma_id"] == 1, "O id da turma deve ser 1."


def test_alterar_aula(client, app):
    """Testa a atualização dos dados de uma aula.

    Este teste verifica se a requisição PUT para a rota '/aula/{id}' retorna o status code 200 (OK),
    se a resposta contém uma mensagem de sucesso e se os dados da aula foram atualizados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        aula = Aula(hora_inicio="08:00:00", hora_fim="09:00:00", dias_da_semana=["Segunda"], usuario_id=1, disciplina_codigo="MAT001", turma_id=1)
        db.session.add(aula)
        db.session.commit()

        # Dados para atualização
        dados_atualizacao = {
            "hora_inicio": "07:00",
            "hora_fim": "09:00",
            "dias_da_semana": ["Segunda", "Quarta"],
            "usuario_cpf": "12345678910",
            "disciplina_codigo": "MAT001",
            "turma_id": 1
        }

        response = client.put(f'/aula/{aula.id}', json=dados_atualizacao)
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Aula atualizada com sucesso!"

        dados = response.json["data"]
        
        assert dados["hora_inicio"] == "07:00:00", "O horário de início deve ser '07:00:00'."
        assert dados["hora_fim"] == "09:00:00", "O horário de fim deve ser '09:00:00'."
        assert dados["dias_da_semana"] == ["Segunda", "Quarta"], "Os dias da semana devem ser '['Segunda', 'Quarta']'."
        assert dados["usuario_id"] == 1, "O id do usuario deve ser 1."
        assert dados["disciplina_codigo"] == "MAT001", "O código da disciplina deve ser 'MAT001'."
        assert dados["turma_id"] == 1, "O id da turma deve 1."


def test_remover_aula(client, app):
    """Testa a exclusão de uma aula.

    Este teste verifica se a requisição DELETE para a rota '/aula/{id}' retorna o status code 200 (OK)
    e se a resposta contém uma mensagem de sucesso.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        aula = Aula(hora_inicio="08:00:00", hora_fim="09:00:00", dias_da_semana=["Segunda"], usuario_id=1, disciplina_codigo="MAT001", turma_id=1)
        db.session.add(aula)
        db.session.commit()

        response = client.delete(f'/aula/{aula.id}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Aula deletada com sucesso!"