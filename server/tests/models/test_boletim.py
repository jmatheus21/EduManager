from app.models import Aula, Usuario, Cargo, Disciplina, Turma, Calendario, Sala, Aluno, Boletim
from app.extensions import db
from app.utils.usuario_helpers import gerar_hashing
from app.utils.date_helpers import string_para_data

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

            db.session.commit()

def test_cadastrar_notas_aula(app):
    """Testa o cadastro das notas de todos os alunos de uma aula específica no boletim.

    Este teste verifica se as notas dos alunos de uma aula podem ser cadastradas no boletim
    e se os dados referentes às notas estão corretos.
    
    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        boletim1 = Boletim(aluno_matricula="202600000001", aula_id=1, notas=[], ausencias=0)
        boletim1.notas.append(4.5)
        db.session.add(boletim1)
        db.session.commit()

        boletim_adicionado = db.session.query(Boletim).filter_by(aluno_matricula="202600000001", aula_id=1).first()
        assert boletim_adicionado is not None
        assert boletim_adicionado.aluno_matricula == "202600000001"
        assert boletim_adicionado.aula_id == 1
        assert boletim_adicionado.notas == [4.5]

def test_alterar_notas_aula(app):
    """Testa a atualização dos dados de um boletim no banco de dados.

    Este teste verifica se os dados de um boletim podem ser atualizados corretamente
    e se os novos dados são persistidos no banco de dados.

    Args:
        app (Flask): Aplicação Flask para acessar o contexto da aplicação.
    """
    with app.app_context():
        criar_dependencias(app)
        boletim = Boletim(aluno_matricula="202600000001", aula_id=1, notas=[7.8,5.6], ausencias=0)
        db.session.add(boletim)
        db.session.commit()

        boletim_alterado = db.session.query(Boletim).filter_by(aluno_matricula="202600000001", aula_id=1).first()
        boletim_alterado.notas = [7.8,6.0]
        db.session.commit()
        
        assert boletim_alterado is not None
        assert boletim_alterado.aluno_matricula == "202600000001"
        assert boletim_alterado.aula_id == 1
        assert boletim_alterado.notas == [7.8,6.0]

        


