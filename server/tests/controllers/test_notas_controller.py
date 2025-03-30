"""
Este módulo contém testes para as rotas e as operações relacionadas a classe de controle `notas_controller`.

Os testes verificam as operações básicas como cadastro, alteração e busca para o controle `notas_controller`,
incluindo cadastro, alteração e busca de notas do boletim de um aluno no banco de dados.
"""

from app.models import Aula, Usuario, Disciplina, Turma, Calendario, Sala, Cargo, Aluno, Boletim
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
            boletim2 = Boletim(aluno_matricula="202600000002", aula_id=1, notas=[], ausencias=0)
            db.session.add_all([boletim1, boletim2])

            db.session.commit()

def test_cadastrar_notas(client, app):
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        dados_validos = {
            "aula_id": 1,
            "alunos": [
                { "matricula": "202600000001", "nota": 8.7 },
                { "matricula": "202600000002", "nota": 5.4 }
            ]
        }

        response = client.post("/notas/", json=dados_validos)
        
        assert response.status_code == 201, "O status code deve ser 201 (Created)."
        assert "mensagem" in response.json, "A resposta deve conter uma mensagem."

def test_cadastrar_notas_dados_invalidos(client, app):
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        dados_invalidos = {
            "aula_id": 1,
            "alunos": [
                { "matricula": "2026000000018", "nota": -1 },
                { "matricula": "202600000002", "nota": 12 }
            ]
        }

        response = client.post("/notas/", json=dados_invalidos)
        assert response.status_code == 400, "O status code deve ser 400 (Bad Request)."
        assert "erro" in response.json, "A resposta deve conter mensagens de erro."
        assert len(response.json["erro"]) == 2, "Deve haver 2 erros de validação."


def test_buscar_notas_aula(client, app):
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        response = client.get("/notas/1")

        assert response.status_code == 200
        assert isinstance(response.json, dict), "A resposta deve ser um dicionário."
        dados = response.json
        assert dados["aula_id"] == 1
        assert dados["alunos"] == [{ "matricula": "202600000001", "nome": "João Pedro dos Santos" },{ "matricula": "202600000002", "nome": "Paulo Silva da Cruz" }]


def test_buscar_notas_aluno(client, app):
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        response = client.get("/notas/202600000001/1")

        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert isinstance(response.json, dict), "A resposta deve ser um dicionário."
        dados = response.json
        assert dados["aula_id"] == 1
        assert dados["matricula"] == "202600000001"
        assert dados["nome"] == "João Pedro dos Santos"
        assert dados["notas"] == []


def test_alterar_notas(client, app):
    with app.app_context():
        criar_dependencias(app)
        usuario_entra_no_sistema(client, app)

        # Dados para atualização
        dados_atualizacao = {
            "notas": [7.8, 5.6]
        }

        response = client.put("/notas/202600000001/1", json=dados_atualizacao)

        assert response.status_code == 200, "O status code deve ser 200 (OK)."
        assert response.json["mensagem"] == "Notas alteradas com sucesso!"
        assert response.json["notas"] == [7.8, 5.6]