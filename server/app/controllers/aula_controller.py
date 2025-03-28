"""
Módulo de Controlador para Aulas

Este módulo contém as funções que implementam a lógica de negócio para as operações relacionadas às Aulas.
Ele interage com o modelo `Aula` para realizar operações CRUD e valida os dados usando o módulo `validators`.
"""

from flask import request, jsonify
from app.extensions import db
from ..models import Aula, Usuario, Disciplina, Turma
from app.utils.validators import validar_aula
from app.utils.hour_helpers import hora_para_string


def cadastrar_aula(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Cadastra uma nova aula no banco de dados.

    Esta função recebe os dados de uma aula via JSON, valida os dados e, se válidos, cadastra a aula no banco de dados.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados da aula cadastrada, ou uma mensagem de erro em caso de dados inválidos.
    """
    data = request.get_json()

    erros = validar_aula(hora_inicio=data['hora_inicio'], hora_fim=data['hora_fim'], dias_da_semana=data['dias_da_semana'], usuario_cpf=data['usuario_cpf'], disciplina_codigo=data['disciplina_codigo'], turma_id=data['turma_id'])
    if erros:
        return jsonify({"erro": erros }), 400
    
    disciplina_existente = db.session.query(Disciplina).filter_by(codigo=data['disciplina_codigo']).first()
    if disciplina_existente is None:
        return jsonify({"erro": ["Disciplina não existe"]}), 400

    turma_existente = db.session.query(Turma).filter_by(id=data['turma_id']).first()
    if turma_existente is None:
        return jsonify({"erro": ["Turma não existe"]}), 400
        
    aula_existente = db.session.query(Aula).filter_by(disciplina_codigo=data['disciplina_codigo'], turma_id=data['turma_id']).first()
    if aula_existente is not None:
        return jsonify({"erro": ["Aula já existe"]}), 400
    
    usuario_existente = db.session.query(Usuario).filter_by(cpf=data['usuario_cpf']).first()
    if usuario_existente is None:
        return jsonify({"erro": ["Usuário não existe"]}), 400
    elif usuario_existente.tipo != "p":
        return jsonify({"erro": ["O usuário não é do tipo 'professor'"]}), 400
    
    aula_no_mesmo_horario_com_mesmo_usuario = db.session.query(Aula).filter_by(
        hora_inicio=data['hora_inicio'], 
        hora_fim=data['hora_fim'], 
        dias_da_semana=data['dias_da_semana'], 
        turma_id=data['turma_id']
    ).first()

    if aula_no_mesmo_horario_com_mesmo_usuario is not None:
        return jsonify({"erro": ["Já existe uma aula no mesmo horário, com o mesmo professor"]}), 400

    elif data['disciplina_codigo'] not in [disciplina.codigo for disciplina in usuario_existente.disciplinas]:
        return jsonify({"erro": ["O 'professor' não pode ensinar essa 'disciplina'"]}), 400

    nova_aula = Aula(hora_inicio=data['hora_inicio'], hora_fim=data['hora_fim'], dias_da_semana=data['dias_da_semana'], usuario_id=usuario_existente.id, disciplina_codigo=data['disciplina_codigo'], turma_id=data['turma_id'])
    db.session.add(nova_aula)

    # AAAAAA

    db.session.commit()

    # Usando a função hora_para_string para converter os objetos time para string
    hora_inicio_str = hora_para_string(nova_aula.hora_inicio)
    hora_fim_str = hora_para_string(nova_aula.hora_fim)

    return jsonify({"mensagem": "Aula criada com sucesso!", "data": {"id": nova_aula.id, "hora_inicio": hora_inicio_str, "hora_fim": hora_fim_str, "dias_da_semana": nova_aula.dias_da_semana, "usuario_id": nova_aula.usuario_id, "disciplina_codigo": nova_aula.disciplina_codigo, "turma_id": nova_aula.turma_id}}), 201


def listar_aulas(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Lista todas as aulas cadastradas no banco de dados.

    Returns:
        jsonify: Resposta JSON contendo uma lista de aulas com seus respectivos dados.
    """
    aulas = Aula.query.all()

    return jsonify([{"id": aula.id, "hora_inicio": hora_para_string(aula.hora_inicio), "hora_fim": hora_para_string(aula.hora_fim), "dias_da_semana": aula.dias_da_semana, "professor_id": aula.professor.id, "professor_nome": aula.professor.nome, "disciplina_codigo": aula.disciplina_codigo, "turma_id": aula.turma_id} for aula in aulas]), 200


def buscar_aula(id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Busca uma aula específica pelo número.

    Args:
        id (int): O id da aula a ser buscada.

    Returns:
        jsonify: Resposta JSON contendo os dados da aula encontrada.
    """
    aula = db.session.get(Aula, id)

    return jsonify({"id": aula.id, "hora_inicio": hora_para_string(aula.hora_inicio), "hora_fim": hora_para_string(aula.hora_fim), "dias_da_semana": [dia_da_semana for dia_da_semana in aula.dias_da_semana], "professor_id": aula.professor.id, "professor_nome": aula.professor.nome, "professor_cpf": aula.professor.cpf, "disciplina_codigo": aula.disciplina_codigo, "disciplina_nome": aula.disciplina.nome, "turma_id": aula.turma_id, "turma_ano": aula.turma.ano, "turma_serie": aula.turma.serie, "turma_nivel_de_ensino": aula.turma.nivel_de_ensino}), 200


def alterar_aula(id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Altera os dados de uma aula existente.

    Esta função recebe o id de uma aula e os novos dados via JSON, valida os dados e, se válidos, atualiza a aula no banco de dados.

    Args:
        id (int): O número da aula a ser alterada.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados atualizados da aula, ou uma mensagem de erro em caso de dados inválidos.
    """
    aula = db.session.get(Aula, id)
    if not aula:
        return jsonify({"erro": "Aula não encontrada"}), 400
    
    data = request.get_json()

    erros = validar_aula(hora_inicio=data['hora_inicio'], hora_fim=data['hora_fim'], dias_da_semana=data['dias_da_semana'], usuario_cpf=data['usuario_cpf'], disciplina_codigo=data['disciplina_codigo'], turma_id=data['turma_id'])
    if erros:
        return jsonify({"erro": erros}), 400
    
    disciplina_existente = db.session.query(Disciplina).filter_by(codigo=data['disciplina_codigo']).first()
    if disciplina_existente is None:
        return jsonify({"erro": ["Disciplina não existe"]}), 400

    turma_existente = db.session.query(Turma).filter_by(id=data['turma_id']).first()
    if turma_existente is None:
        return jsonify({"erro": ["Turma não existe"]}), 400
    
    aula_existente = db.session.query(Aula).filter_by(disciplina_codigo=data['disciplina_codigo'], turma_id=data['turma_id']).first()
    if aula_existente is not None and id != aula_existente.id:
        return jsonify({"erro": ["Aula já existe"]}), 400
    
    usuario_existente = db.session.query(Usuario).filter_by(cpf=data["usuario_cpf"]).first()
    if usuario_existente is None:
        return jsonify({"erro": ["Usuário não existe"]}), 400
    elif usuario_existente.tipo != "p":
        return jsonify({"erro": ["O usuário não é do tipo 'professor'"]}), 400
    
    aula_no_mesmo_horario_com_mesmo_usuario = db.session.query(Aula).filter_by(hora_inicio=data['hora_inicio'], hora_fim=data['hora_fim'], dias_da_semana=data['dias_da_semana'], turma_id=data['turma_id']).first()
    if aula_no_mesmo_horario_com_mesmo_usuario is not None:
        return jsonify({"erro": ["Já existe uma aula no mesmo horário, com o mesmo professor"]}), 400
    
    aula.hora_inicio = data['hora_inicio']
    aula.hora_fim = data['hora_fim']
    aula.dias_da_semana = data['dias_da_semana']
    aula.usuario_id = usuario_existente.id
    aula.disciplina_codigo = data['disciplina_codigo']
    aula.turma_id = data['turma_id']
    db.session.commit()

    # Usando a função hora_para_string para converter os objetos time para string
    hora_inicio_str = hora_para_string(aula.hora_inicio)
    hora_fim_str = hora_para_string(aula.hora_fim)

    return jsonify({"mensagem": "Aula atualizada com sucesso!", "data": {"id": aula.id, "hora_inicio": hora_inicio_str, "hora_fim": hora_fim_str, "dias_da_semana": aula.dias_da_semana, "usuario_id": aula.usuario_id, "disciplina_codigo": aula.disciplina_codigo, "turma_id": aula.turma_id}}), 200


def remover_aula(id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Remove uma aula existente do banco de dados.

    Args:
        id (int): O id da aula a ser removida.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    aula = db.session.get(Aula, id)
    db.session.delete(aula)
    db.session.commit()
    return jsonify({"mensagem": "Aula deletada com sucesso!"}), 200