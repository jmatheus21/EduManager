"""
Módulo de Controlador para Calendários.

Este módulo contém as funções que implementam a lógica de negócio para as operações relacionadas àos calendários.
Ele interage com o modelo `Calendário` para realizar operações CRUD e valida os dados usando o módulo `validators`.
"""

from flask import request, jsonify
from app.extensions import db
from ..models import Calendario
from app.utils.validators import validar_calendario
from app.utils.date_helpers import string_para_data

def cadastrar_calendario() -> jsonify:
    """Cadastra um novo calendário no banco de dados.

    Esta função recebe os dados de um calendário via JSON, valida os dados e, se válidos, cadastra o calendário no banco de dados.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados do calendário cadastrado, ou uma mensagem de erro em caso de dados inválidos.
    """
    data = request.get_json()

    erros = validar_calendario(ano_letivo=data['ano_letivo'], data_inicio=data['data_inicio'], data_fim=data['data_fim'], dias_letivos=data['dias_letivos'])
    if erros:
        return jsonify({"erro": erros}), 400
    
    calendario_existente = db.session.get(Calendario, data['ano_letivo'])
    if calendario_existente is not None:
        return jsonify({"erro": ["Calendário já existe"]}), 400

    novo_calendario = Calendario(ano_letivo=data['ano_letivo'], data_inicio=string_para_data(data['data_inicio']), data_fim=string_para_data(data['data_fim']), dias_letivos=data['dias_letivos'])
    db.session.add(novo_calendario)
    db.session.commit()
    return jsonify({"mensagem": "Calendário criado com sucesso!", "data": {"ano_letivo": novo_calendario.ano_letivo, "data_inicio": novo_calendario.data_inicio, "data_fim": novo_calendario.data_fim, "dias_letivos": novo_calendario.dias_letivos}}), 201


def listar_calendarios() -> jsonify:
    """Lista todos os calendários cadastrados no banco de dados.

    Returns:
        jsonify: Resposta JSON contendo uma lista de calendários com seus respectivos dados.
    """
    calendarios = Calendario.query.all()
    return jsonify([{"ano_letivo": calendario.ano_letivo, "data_inicio": calendario.data_inicio, "data_fim": calendario.data_fim, "dias_letivos": calendario.dias_letivos} for calendario in calendarios]), 200


def buscar_calendario(ano_letivo: int) -> jsonify:
    """Busca um calendário específico pelo ano letivo correspondente.

    Args:
        ano_letivo (int): O ano letivo do calendário a ser buscado.

    Returns:
        jsonify: Resposta JSON contendo os dados do calendário encontrado.
    """
    calendario = db.session.get(Calendario, ano_letivo)
    return jsonify({"ano_letivo": calendario.ano_letivo, "data_inicio": calendario.data_inicio, "data_fim": calendario.data_fim, "dias_letivos": calendario.dias_letivos}), 200