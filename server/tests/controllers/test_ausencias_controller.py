"""
Este módulo contém testes para as rotas e as operações relacionadas a classe de controle `ausencias_controller`.

Os testes verificam as operações de registro e alteração de ausências no banco de dados para o controle `aluno_controller`.
"""

from app.models import Disciplina, Cargo, Usuario, Calendario, Sala, Turma, Aluno, Aula, Boletim
from app.extensions import db
from app.utils.date_helpers import string_para_data
from app.utils.usuario_helpers import gerar_hashing
from tests.user_event import usuario_entra_no_sistema


def criar_dependencias(app):
    with app.app_context():
        with db.session.no_autoflush:
            #Garante que a disciplina existe
            if not Disciplina.query.filter_by(codigo="MAT001").first():
                disciplina = Disciplina(codigo="MAT001", nome="Matemática", carga_horaria=30, ementa="Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", bibliografia="STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro:Zahar, 2014.")
                db.session.add(disciplina)
                
            # Garante que o usuário existe
            cargo = Cargo(nome="Professor", salario=2060.0, data_contrato="2027-12-31")
            if not Usuario.query.filter_by(id=1).first():
                usuario = Usuario(cpf="12345678912", nome="Alan Ferreira dos Santos", email="alanferreira@email.com", senha=gerar_hashing("bocaAberta123"), telefone="79 9 9999-8888", endereco="Bairro X, Rua A", horario_de_trabalho="Seg-Sex,7h-12h", data_de_nascimento=string_para_data("1998-05-17"), tipo="p", formacao="Licenciatura em Matemática", escolaridade= None, habilidades= None, disciplinas=[disciplina], cargos=[cargo])
                db.session.add(usuario)
            
            # Garante que a turma existe
            calendario = Calendario(ano_letivo = 2026, data_inicio=string_para_data("2026-02-17"), data_fim=string_para_data("2026-11-27"), dias_letivos=150)
            db.session.add(calendario)
            sala = Sala(numero=101, capacidade=50, localizacao="Bloco A, 1° andar")
            db.session.add(sala)
            turma = Turma(ano=9, serie="A", nivel_de_ensino="Ensino Fundamental", turno="M", status="A", sala_numero= 101, calendario_ano_letivo= 2026)
            db.session.add(turma)
            
            aluno1 = Aluno(matricula="202600000001", nome="João Pedro dos Santos", email="joaopedro@email.com", telefone="79 9 1234-5678", endereco="Bairro X, Rua A", data_de_nascimento=string_para_data("2011-09-10"))
            aluno2 = Aluno(matricula="202600000002", nome="Paulo Silva da Cruz", email="psilva@email.com", telefone="79 9 1989-7841", endereco="Bairro Y, Rua B", data_de_nascimento=string_para_data("2011-05-01"))
            db.session.add_all([aluno1, aluno2])
            aluno1.turmas.append(turma)
            aluno2.turmas.append(turma)

            aula = Aula(hora_inicio="13:00:00", hora_fim="15:00:00", dias_da_semana=["Terça", "Quinta"], usuario_id=1, disciplina_codigo="MAT001", turma_id=1)
            db.session.add(aula)

            boletim1 = Boletim(aluno_matricula="202600000001", aula_id=1, notas=[], ausencias=0)
            boletim2 = Boletim(aluno_matricula="202600000002", aula_id=1, notas=[], ausencias=10)
            db.session.add_all([boletim1, boletim2])

            db.session.commit()


def test_registrar_ausencias(client, app):
    """Testa o registro das ausências com dados válidos.

    Este teste verifica se:
    1. A requisição POST para a rota '/ausencia' retorna o status code 200 (Ok).
    2. A resposta contém uma mensagem indicando sucesso.
    3. Os dados daz ausências registrada são retornados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario_entra_no_sistema(client, app)
        criar_dependencias(app)

        dados = {
            "alunos": [{"matricula": "202600000001", "ausencia": True},
                       {"matricula": "202600000002", "ausencia": True}]
        }

        aula_id = 1

        response = client.put(f'/ausencias/{aula_id}', json=dados)

        assert response.status_code == 200, "O status code deve ser 200 (Ok)."
        assert "mensagem" in response.json, "A resposta deve conter uma mensagem."
        
        resposta = response.json["mensagem"]

        # Verifica se as ausências foram incrementadas
        boletim1 = db.session.query(Boletim).filter_by(aluno_matricula="202600000001", aula_id=1).first()
        boletim2 = db.session.query(Boletim).filter_by(aluno_matricula="202600000002", aula_id=1).first()

        assert boletim1.ausencias == 1, "O número de ausências no boletim 1 deve ser 1."
        assert boletim2.ausencias == 11, "O número de ausências no boletim 2 deve ser 11."
        assert "Ausências cadastradas com sucesso!" in resposta, "Deve apresentar uma mensagem se sucesso."


def test_buscar_ausencias_aula(client, app):
    """Testa a busca dos alunos por aula com dados válidos.

    Este teste verifica se a requisição GET para a rota '/ausencias/' retorna o status code 200 (OK)
    e se a resposta contém uma lista com os alunos cadastrados na aula.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario_entra_no_sistema(client, app)
        criar_dependencias(app)

        aula_id = 1

        response = client.get(f'/ausencias/{aula_id}')

        assert response.status_code == 200, "O status code deve ser 200 (Ok)."
    
        resposta = response.json

        assert resposta['aula_id'] == aula_id, "O id da aula deve ser 1."
        assert isinstance(resposta['alunos'], list), "A resposta deve ser uma lista."
        assert len(resposta['alunos']) == 2, "Deve haver exatamente 2 alunos na listagem."


def test_buscar_ausencias_aluno(client, app):
    """Testa a busca de ausências de um aluno específico pela matrícula e ID de aula.

    Este teste verifica se a requisição GET para a rota '/ausencias/{aula_id}/{aluno_matricula}' retorna o status code 200 (OK)
    e se a resposta contém os dados corretos do aluno buscado.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario_entra_no_sistema(client, app)
        criar_dependencias(app)

        aula_id = 1
        aluno_matricula = "202600000002"
        response = client.get(f'/ausencias/{aula_id}/{aluno_matricula}')
        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, dict), "A resposta deve ser um dicionário."

        resposta = response.json
        
        assert "matricula" in resposta, "A resposta deve conter o campo 'matricula'."
        assert resposta["matricula"] == "202600000002", "A matrícula do aluno deve ser 202600000002."
        assert "nome" in resposta, "A resposta deve conter o campo 'nome'."
        assert resposta["nome"] == "Paulo Silva da Cruz", "O nome do aluno deve ser Paulo Silva da Cruz."
        assert "aula_id" in resposta, "A resposta deve conter o campo 'aula_id'."
        assert resposta['aula_id'] == 1, "O id da aula deve ser 1"
        assert "ausencias" in resposta, "A resposta deve conter o campo 'ausencias'."
        assert resposta['ausencias'] == 10, "O número de ausências no boletim 2 deve ser 10"


def test_alterar_ausencia(client, app):
    """Testa a atualização dos dados de ausência de um aluno.

    Este teste verifica se a requisição PUT para a rota '/aluno/{aula_id}/{aluno_matricula}' retorna o status code 200 (OK),
    se a resposta contém uma mensagem de sucesso e se os dados das ausências do aluno foram atualizados corretamente.

    Args:
        client (FlaskClient): Cliente de teste do Flask para simular requisições HTTP.
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        usuario_entra_no_sistema(client, app)
        criar_dependencias(app)

        dados = {
            "ausencias": 10
        }

        aula_id = 1
        aluno_matricula = "202600000001"
        response = client.put(f'/ausencias/{aula_id}/{aluno_matricula}', json=dados)

        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert "mensagem" in response.json, "A resposta deve conter uma mensagem."
        assert  "ausencias" in response.json, "A repossta deve conter ausências"
        
        # return jsonify({"mensagem": "Ausências alteradas com sucesso!", "ausencias": boletim.ausencias }), 200

        resposta = response.json
        
        assert resposta["mensagem"] == "Ausências alteradas com sucesso!"
        assert resposta["ausencias"] == 10, "O número de ausências deve ser 10."