"""
Módulo de Controlador para Aluno

Este módulo contém as funções que implementam a lógica de negócio para as operações relacionadas aos Alunos.
Ele interage com o modelo `Aluno` para realizar operações CRUD e valida os dados usando o módulo `validators`.
"""

from flask import request, jsonify
from app.extensions import db
from ..models import Aluno, Turma, Boletim
from app.utils.validators import validar_aluno
from app.utils.date_helpers import string_para_data


def cadastrar_aluno(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Cadastra um novo aluno no banco de dados.

    Esta função recebe os dados de um aluno via JSON, valida os dados e, se válidos, cadastra o aluno no banco de dados.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados do aluno cadastrado, ou uma mensagem de erro em caso de dados inválidos.
    """

    data = request.get_json()

    erros = validar_aluno(nome=data['nome'], email=data['email'], telefone=data['telefone'], endereco=data['endereco'], data_de_nascimento=data['data_de_nascimento'])
    if erros:
        return jsonify({"erro": erros }), 400

    # Verifica se a turma existe
    turma_existente = db.session.get(Turma, data["turma_id"])
    if turma_existente is None:
        return jsonify({"erro": ["Turma não existe"]}), 400
    
    # criar lógica para matrícula
    id = db.session.query(Aluno).count() + 1
    matricula = f"{turma_existente.calendario_ano_letivo}000{id:05d}"

    # verificando se e-mail é único
    email_existente = db.session.query(Aluno).filter_by(email= data['email']).first()
    if email_existente:
        return jsonify({"erro": ["E-mail já existe"]}), 400
    
    # Verifica se a turma está aberta
    if turma_existente.status != "A":
        return jsonify({"erro": ["A turma está fechada, portanto, não é possível cadastrar mais alunos"]}), 400
    
    # criando aluno
    novo_aluno = Aluno(matricula=matricula, nome=data['nome'], email=data['email'], telefone=data['telefone'], endereco=data['endereco'], data_de_nascimento=data['data_de_nascimento'], turmas=[turma_existente])
    db.session.add(novo_aluno)

    # criando boletim para todas as aulas da turma que o aluno foi cadastrado
    for aula in turma_existente.aulas:
        boletim = Boletim(aluno_matricula=matricula, aula_id=aula.id, notas=[], ausencias=0)
        db.session.add(boletim)
    
    db.session.commit()

    return jsonify({"mensagem": "Aluno criado com sucesso!", "data": {"matricula": novo_aluno.matricula, "nome": novo_aluno.nome, "email": novo_aluno.email, "telefone": novo_aluno.telefone, "endereco": novo_aluno.endereco, "data_de_nascimento": novo_aluno.data_de_nascimento, "turma_id": turma_existente.id}}), 201


def matricular_aluno(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Realiza a matrícula de um novo aluno no banco de dados.

    Esta função recebe os dados de um aluno via JSON, valida os dados e, se válidos, realiza a matrícula o aluno no banco de dados.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados do aluno cadastrado, ou uma mensagem de erro em caso de dados inválidos.
    """

    data = request.get_json()

    matricula = data["aluno_matricula"]
    id = data["turma_id"]

    if not matricula or not isinstance(matricula, str) or len(matricula) != 12:
        return jsonify({"erro": ["A matrícula do aluno é inválida"]}), 400
    
    if not id or not isinstance(id, int) or id <= 0:
        return jsonify({"erro": ["O id da turma é inválido"]}), 400
    
    aluno = db.session.get(Aluno, matricula)
    if aluno is None:
        return jsonify({"erro": ["Não existe aluno com essa matrícula"]}), 400
    
    turma = db.session.get(Turma, id)
    if turma is None:
        return jsonify({"erro": ["Não existe turma com esse id"]}), 400
    
    if turma.status != "A":
        return jsonify({"erro": ["A turma informada não está ativa"]}), 400
    
    if aluno.turmas:
        if turma in aluno.turmas:
            return jsonify({"erro": ["Aluno já está matriculado nessa turma"]}), 400
    
        turma_mais_recente = max(aluno.turmas, key=lambda turma: turma.calendario_ano_letivo)

        if turma_mais_recente.calendario_ano_letivo == turma.calendario_ano_letivo:
            return jsonify({"erro": ["O aluno já está matriculado em uma turma nesse ano letivo"]}), 400
    
    aluno.turmas.append(turma)

    for aula in turma.aulas:
        boletim = Boletim(aluno_matricula=aluno.matricula, aula_id=aula.id, notas=[], ausencias=0)
        db.session.add(boletim)
    
    db.session.commit()

    return jsonify({"messagem": "Aluno matriculado com sucesso!"}), 201


def listar_alunos(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Lista todas os alunos cadastrados no banco de dados.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma lista de alunos com seus respectivos dados.
    """
    alunos = Aluno.query.all()

    return jsonify([{"matricula": aluno.matricula, "nome": aluno.nome, "email": aluno.email, "telefone": aluno.telefone, "endereco": aluno.endereco, "data_de_nascimento": aluno.data_de_nascimento, "turma_id": max(aluno.turmas, key=lambda turma: turma.calendario_ano_letivo).id if aluno.turmas else None} for aluno in alunos]), 200


def buscar_aluno(matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Busca um aluno específico pela matrícula.

    Args:
        matricula (str): A matricula do aluno a ser buscado.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo os dados do aluno encontrado.
    """
    aluno = db.session.get(Aluno, matricula)
    if not aluno.turmas:
        return jsonify({"erro": ["Nenhuma turma associada a aluno!"]}), 400
    
    turma_atual = max(aluno.turmas, key=lambda turma: turma.calendario_ano_letivo) if aluno.turmas else None

    if turma_atual is None or turma_atual.status != "A":
        return jsonify({"matricula": aluno.matricula, "nome": aluno.nome, "email": aluno.email, "telefone": aluno.telefone, "endereco": aluno.endereco, "data_de_nascimento": aluno.data_de_nascimento, "turma_id": "Não matriculado"}), 200
    else:
        return jsonify({"matricula": aluno.matricula, "nome": aluno.nome, "email": aluno.email, "telefone": aluno.telefone, "endereco": aluno.endereco, "data_de_nascimento": aluno.data_de_nascimento, "turma_id": turma_atual.id, "turma_ano": turma_atual.ano, "turma_serie": turma_atual.serie, "turma_nivel_de_ensino": turma_atual.nivel_de_ensino}), 200


def alterar_aluno(matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Altera os dados de um aluno existente.

    Esta função recebe a matrícula de um aluno e os novos dados via JSON, valida os dados e, se válidos, atualiza o aluno no banco de dados.

    Args:
        matricula (str): A matrícula do aluno a ser alterado.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados atualizados do aluno, ou uma mensagem de erro em caso de dados inválidos.
    """
    aluno = db.session.query(Aluno).filter_by(matricula=matricula).first()
    data = request.get_json()
    
    erros = validar_aluno(nome=data['nome'], email=data['email'], telefone=data['telefone'], endereco=data['endereco'], data_de_nascimento=data['data_de_nascimento'])
    if erros:
        return jsonify({"erro": erros}), 400

    # verifica se fez alteração no turma_id
    nova_turma = all(turma.id != data['turma_id'] for turma in aluno.turmas)

    if nova_turma:
        # Verifica se a turma existe
        turma_existente = db.session.get(Turma, data["turma_id"])
        if turma_existente is None:
            return jsonify({"erro": ["Turma não existe"]}), 400
        
        # Verifica se a turma está aberta
        if turma_existente.status == "C":
            return jsonify({"erro": ["A turma está fechada"]}), 400
        
        turma_mais_recente = max(aluno.turmas, key=lambda turma: turma.calendario_ano_letivo)

        # apaga os boletins da turma anterior
        for aula in turma_mais_recente.aulas:
            boletins = db.session.query(Boletim).filter_by(aluno_matricula=aluno.matricula, aula_id=aula.id)
            for boletim in boletins:
                db.session.delete(boletim)

        # Caso a turma seja nova, adiciona nova turma ao aluno
        aluno.turmas.remove(turma_mais_recente)
        
        # criar boletim para novas turmas
        for aula in turma_existente.aulas:
            boletim = Boletim(aluno_matricula=aluno.matricula, aula_id=aula.id, notas=[], ausencias=0)
            db.session.add(boletim)

        aluno.turmas.append(turma_existente)

    if aluno.email != data['email']:
        email_existente = db.session.query(Aluno).filter_by(email= data['email']).first()
        if email_existente:
            return jsonify({"erro": ["E-mail já existe"]}), 400
        
    aluno.nome = data['nome']
    aluno.email = data['email']
    aluno.telefone = data['telefone']
    aluno.endereco = data['endereco']
    aluno.data_de_nascimento = string_para_data(data['data_de_nascimento'])

    db.session.commit()

    return jsonify({"mensagem": "Aluno atualizado com sucesso!", "data": {"matricula": aluno.matricula, "nome": aluno.nome, "email": aluno.email, "telefone": aluno.telefone, "endereco": aluno.endereco, "data_de_nascimento": aluno.data_de_nascimento}}), 200


def remover_aluno(matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Remove um aluno existente do banco de dados.

    Args:
        matrícula (str): A matrícula do aluno a ser removido.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    aluno = db.session.query(Aluno).filter_by(matricula=matricula).first()
    
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"mensagem": "Aluno deletado com sucesso!"}), 200