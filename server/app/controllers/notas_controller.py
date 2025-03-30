"""
Módulo de Controlador para Notas.

Este módulo contém as funções que implementam a lógica de negócio para as operações relacionadas às notas.
"""

from flask import jsonify, request
from app.extensions import db
from app.utils.validators import validar_notas_cadastradas, validar_nota_alterada
from ..models import Aula, Aluno, Boletim, Turma


def cadastrar_notas(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Cadastra uma nova nota no banco de dados.

    Esta função recebe os dados de um aluno via JSON, valida os dados e, se válidos, cadastra a nota no banco de dados.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso, ou uma mensagem de erro em caso de dados inválidos.
    """
    data = request.get_json()

    erros = validar_notas_cadastradas(alunos=data["alunos"], aula_id=data["aula_id"])
    if erros:
        return jsonify({"erro": erros }), 400

    # validar aula
    aula = db.session.get(Aula, data['aula_id'])
    if not aula:
        return jsonify({"erro": ["O 'id_aula' não corresponde a nenhuma aula"]}), 400
    
    # verificar se aula é de turma ativa
    turma = db.session.get(Turma, aula.turma_id)
    if not turma or turma.status != "A":
        return jsonify({"erro": ["A aula está em uma turma já consolidada"]}), 400

    for aluno in data['alunos']:
        aluno_existente = db.session.get(Aluno, aluno["matricula"])
        if not aluno_existente:
            return jsonify({"erro": ["Algum aluno não foi encontrado"]}), 400

        boletim = db.session.query(Boletim).filter_by(aluno_matricula=aluno["matricula"], aula_id=data['aula_id']).first()
        if not boletim:
            return jsonify({"erro": ["Algum aluno não possui boletim para essa aula"]}), 400
        elif len(boletim.notas) >= 4:
            return jsonify({"erro": ["Todas as notas já foram cadastradas para essa aula"]}), 400

        boletim.notas = boletim.notas + [aluno["nota"]]

    db.session.commit()

    return jsonify({"mensagem": "Notas cadastradas com sucesso!"}), 201


def buscar_notas_aula(aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Busca as notas de todos os alunos vinculados à uma aula em específico.

    Args:
        cpf (id): O id da aula.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo as notas de todos os aulas da aula.
    """
    # verificar existência de aula
    aula = db.session.get(Aula, aula_id)
    if not aula:
        return jsonify({"erro": ["O 'id_aula' não corresponde a nenhuma aula"]}), 400
    
    # verificar se aula é de uma turma ativa
    turma = db.session.get(Turma, aula.turma_id)
    if not turma or turma.status != "A":
        return jsonify({"erro": ["A aula está em uma turma já consolidada"]}), 400

    # pegar todos os alunos da aula
    boletins = db.session.query(Boletim).filter_by(aula_id=aula_id).all()

    # retornar todos os alunos dessa aula
    return jsonify({"aula_id": aula.id, "alunos": [{"matricula": boletim.aluno.matricula, "nome": boletim.aluno.nome} for boletim in boletins]}), 200


def buscar_notas_aluno (aluno_matricula: str, aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Busca todas as notas de um aluno.

    Args:
        aluno_matricula (str): A matrícula do aluno.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo as notas de todos os aulas da aula.
    """
    aula = db.session.get(Aula, aula_id)
    if not aula:
        return jsonify({"erro": ["Nenhuma aula foi encontrada"]}), 400
    
    aluno = db.session.get(Aluno, aluno_matricula)
    if not aluno:
        return jsonify({"erro": ["A matrícula informada não corresponde a nenhuma aluno"]}), 400
    
    boletim = db.session.query(Boletim).filter_by(aluno_matricula=aluno.matricula, aula_id=aula.id).first()
    if not boletim:
        return jsonify({"erro": ["Boletim não foi encontrado"]}), 400
    
    return jsonify({"aula_id": aula.id, "matricula": aluno.matricula, "nome": aluno.nome, "notas": boletim.notas, "situacao": boletim.situacao }), 200


def alterar_notas(aluno_matricula: str, aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Altera as notas de um aluno.

    Esta função recebe a matrícula de um aluno e os novos dados via JSON, valida os dados e, se válidos, atualiza as notas do aluno no banco de dados.

    Args:
        aluno_matricula (str): A matrícula do aluno.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados atualizados do usuário, ou uma mensagem de erro em caso de dados inválidos.
    """
    data = request.get_json()

    # validar o json
    erros = validar_nota_alterada(aluno_matricula=aluno_matricula, notas=data["notas"])
    if erros:
        return jsonify({"erro": erros }), 400

    # verifica aula
    aula = db.session.get(Aula, aula_id)
    if not aula:
        return jsonify({"erro": ["Nenhuma aula foi encontrada"]}), 400
    
    # verificar existência do aluno
    aluno = db.session.get(Aluno, aluno_matricula)
    if not aluno:
        return jsonify({"erro": ["A matrícula informada não corresponde a nenhum aluno"]}), 400
    
    # verificar existência de boletim
    boletim = db.session.query(Boletim).filter_by(aluno_matricula=aluno_matricula, aula_id=aula.id).first()
    if not boletim:
        return jsonify({"erro": ["Boletim não foi encontrado"]}), 400

    # alterar o valor da nota
    boletim.notas = data["notas"]
    db.session.commit()

    # retornar mensagem de sucesso
    return jsonify({"mensagem": "Notas alteradas com sucesso!", "notas": boletim.notas }), 200