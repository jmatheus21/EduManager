"""
Módulo de Controlador para Salas.

Este módulo contém as funções que implementam a lógica de negócio para as operações relacionadas às salas.
Ele interage com o modelo `Sala` para realizar operações CRUD e valida os dados usando o módulo `validators`.
"""

from flask import request, jsonify
from app.extensions import db
from ..models import Sala
from app.utils.validators import validar_sala


def cadastrar_sala() -> jsonify:
    """Cadastra uma nova sala no banco de dados.

    Esta função recebe os dados de uma sala via JSON, valida os dados e, se válidos, cadastra a sala no banco de dados.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados da sala cadastrada, ou uma mensagem de erro em caso de dados inválidos.
    """
    data = request.get_json()

    erros = validar_sala(numero=data['numero'], localizacao=data['localizacao'], capacidade=data['capacidade'])
    if erros:
        return jsonify({"erro": erros}), 400
    
    sala_existente = db.session.get(Sala, data['numero'])
    if sala_existente is not None:
        return jsonify({"erro": ["Sala já existe"]}), 400

    nova_sala = Sala(numero=data['numero'], localizacao=data['localizacao'], capacidade=data['capacidade'])
    db.session.add(nova_sala)
    db.session.commit()
    return jsonify({"mensagem": "Sala criada com sucesso!", "data": {"numero": nova_sala.numero, "localizacao": nova_sala.localizacao, "capacidade": nova_sala.capacidade}}), 201


def listar_salas() -> jsonify:
    """Lista todas as salas cadastradas no banco de dados.

    Returns:
        jsonify: Resposta JSON contendo uma lista de salas com seus respectivos dados.
    """
    salas = Sala.query.all()
    return jsonify([{"numero": sala.numero, "localizacao": sala.localizacao, "capacidade": sala.capacidade} for sala in salas]), 200


def buscar_sala(numero: int) -> jsonify:
    """Busca uma sala específica pelo número.

    Args:
        numero (int): O número da sala a ser buscada.

    Returns:
        jsonify: Resposta JSON contendo os dados da sala encontrada.
    """
    sala = db.session.get(Sala, numero)
    return jsonify({"numero": sala.numero, "localizacao": sala.localizacao, "capacidade": sala.capacidade}), 200


def alterar_sala(numero: int) -> jsonify:
    """Altera os dados de uma sala existente.

    Esta função recebe o número de uma sala e os novos dados via JSON, valida os dados e, se válidos, atualiza a sala no banco de dados.

    Args:
        numero (int): O número da sala a ser alterada.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados atualizados da sala, ou uma mensagem de erro em caso de dados inválidos.
    """
    sala = db.session.get(Sala, numero)
    data = request.get_json()

    erros = validar_sala(numero=data['numero'], localizacao=data['localizacao'], capacidade=data['capacidade'])
    if erros:
        return jsonify({"erro": erros}), 400
    
    if numero != data['numero']:
        sala_existente = db.session.get(Sala, data['numero']);
        if sala_existente is not None:
            return jsonify({"erro": ["Sala já existe"]}), 400;

    sala.numero = data['numero']
    sala.localizacao = data['localizacao']
    sala.capacidade = data['capacidade']
    db.session.commit()

    return jsonify({"mensagem": "Sala atualizada com sucesso!", "data": {"numero": sala.numero, "localizacao": sala.localizacao, "capacidade": sala.capacidade}}), 200


def remover_sala(numero: int) -> jsonify:
    """Remove uma sala existente do banco de dados.

    Args:
        numero (int): O número da sala a ser removida.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    sala = db.session.get(Sala, numero)
    db.session.delete(sala)
    db.session.commit()
    return jsonify({"mensagem": "Sala deletada com sucesso!"}), 200