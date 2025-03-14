"""
Módulo de Controlador para Turmas

Este módulo contém as funções que implementam a lógica de negócio para as operações relacionadas às Turmas.
Ele interage com o modelo `Turma` para realizar operações CRUD e valida os dados usando o módulo `validators`.
"""

from flask import request, jsonify
from app.extensions import db
from ..models import Turma, Calendario, Sala
from app.utils.validators import validar_turma


def cadastrar_turma() -> jsonify:
    """Cadastra uma nova turma no banco de dados.

    Esta função recebe os dados de uma turma via JSON, valida os dados e, se válidos, cadastra a turma no banco de dados.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados da turma cadastrada, ou uma mensagem de erro em caso de dados inválidos.
    """
    data = request.get_json()

    erros = validar_turma(ano=data['ano'], serie=data['serie'], nivel_de_ensino=data['nivel_de_ensino'], turno=data['turno'], status=data['status'], sala_numero=data['sala_numero'], calendario_ano_letivo=data['calendario_ano_letivo'])
    if erros:
        return jsonify({"erro": erros}), 400
    
    turma_existente = db.session.query(Turma).filter_by(ano=data['ano'], serie=data['serie'], nivel_de_ensino=data['nivel_de_ensino'], turno=data['turno'], sala_numero=data['sala_numero'], calendario_ano_letivo=data['calendario_ano_letivo']).first()
    if turma_existente is not None:
        return jsonify({"erro": ["Turma já existe"]}), 400
    
    calendario_existente = db.session.query(Calendario).filter_by(ano_letivo=data['calendario_ano_letivo']).first()
    if calendario_existente is None:
        return jsonify({"erro": ["Calendário não existe"]}), 400
    
    sala_existente = db.session.query(Sala).filter_by(numero=data['sala_numero']).first()
    if sala_existente is None:
        return jsonify({"erro": ["Sala não existe"]}), 400
    
    nova_turma = Turma(ano=data['ano'], serie=data['serie'], nivel_de_ensino=data['nivel_de_ensino'], turno=data['turno'], status=data['status'], sala_numero=data['sala_numero'], calendario_ano_letivo=data['calendario_ano_letivo'])
    db.session.add(nova_turma)
    db.session.commit()
    return jsonify({"mensagem": "Turma criada com sucesso!", "data": {"id": nova_turma.id, "ano": nova_turma.ano, "serie": nova_turma.serie, "nivel_de_ensino": nova_turma.nivel_de_ensino, "turno": nova_turma.turno, "status": nova_turma.status, "sala_numero": nova_turma.sala_numero, "calendario_ano_letivo": nova_turma.calendario_ano_letivo}}), 201


def listar_turmas() -> jsonify:
    """Lista todas as turmas cadastradas no banco de dados.

    Returns:
        jsonify: Resposta JSON contendo uma lista de turmas com seus respectivos dados.
    """
    turmas = Turma.query.all()
    return jsonify([{"id": turma.id, "ano": turma.ano, "serie": turma.serie, "nivel_de_ensino": turma.nivel_de_ensino, "turno": turma.turno, "status": turma.status, "sala_numero": turma.sala_numero, "calendario_ano_letivo": turma.calendario_ano_letivo} for turma in turmas]), 200


def buscar_turma(id: int) -> jsonify:
    """Busca uma turma específica pelo número.

    Args:
        id (int): O id da turma a ser buscada.

    Returns:
        jsonify: Resposta JSON contendo os dados da turma encontrada.
    """
    turma = db.session.get(Turma, id)
    return jsonify({"id": turma.id, "ano": turma.ano, "serie": turma.serie, "nivel_de_ensino": turma.nivel_de_ensino, "turno": turma.turno, "status": turma.status, "sala_numero": turma.sala_numero, "calendario_ano_letivo": turma.calendario_ano_letivo}), 200


def alterar_turma(id: int) -> jsonify:
    """Altera os dados de uma turma existente.

    Esta função recebe o id de uma turma e os novos dados via JSON, valida os dados e, se válidos, atualiza a turma no banco de dados.

    Args:
        id (int): O número da turma a ser alterada.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados atualizados da turma, ou uma mensagem de erro em caso de dados inválidos.
    """
    turma = db.session.get(Turma, id)
    if not turma:
        return jsonify({"erro": "Turma não encontrada"}), 404
    
    data = request.get_json()

    erros = validar_turma(ano=data['ano'], serie=data['serie'], nivel_de_ensino=data['nivel_de_ensino'], turno=data['turno'], status=data['status'], sala_numero=data['sala_numero'], calendario_ano_letivo=data['calendario_ano_letivo'])
    if erros:
        return jsonify({"erro": erros}), 400
    
    turma_existente = Turma.query.filter_by(ano=data['ano'], serie=data['serie'], nivel_de_ensino=data['nivel_de_ensino'], turno=data['turno'], status=data['status'], sala_numero=data['sala_numero'], calendario_ano_letivo=data['calendario_ano_letivo']).first()
    if turma_existente is not None:
        return jsonify({"erro": ["Turma já existe"]}), 400

    turma.ano = data['ano']
    turma.serie = data['serie']
    turma.nivel_de_ensino = data['nivel_de_ensino']
    turma.turno = data['turno']
    turma.status = data['status']
    turma.sala_numero = data['sala_numero']
    turma.calendario_ano_letivo = data['calendario_ano_letivo']
    db.session.commit()

    return jsonify({"mensagem": "Turma atualizada com sucesso!", "data": {"id": turma.id, "ano": turma.ano, "serie": turma.serie, "nivel_de_ensino": turma.nivel_de_ensino, "turno": turma.turno, "status": turma.status, "sala_numero": turma.sala_numero, "calendario_ano_letivo": turma.calendario_ano_letivo}}), 200


def remover_turma(id: int) -> jsonify:
    """Remove uma turm existente do banco de dados.

    Args:
        id (int): O id da turma a ser removida.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    turma = db.session.get(Turma, id)
    db.session.delete(turma)
    db.session.commit()
    return jsonify({"mensagem": "Turma deletada com sucesso!"}), 200