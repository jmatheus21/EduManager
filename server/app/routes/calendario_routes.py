"""
Módulo de Rotas para Calendários.

Este módulo define as rotas relacionadas às operações dos calendários no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `calendario_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import calendario_controller

# Cria um Blueprint para as rotas de calendário
calendario_bp = Blueprint("calendario", __name__)


@calendario_bp.route("/", methods=['POST'])
def cadastrar_calendario() -> jsonify:
    """Rota para cadastrar um novo calendário.

    Esta rota recebe os dados de um calendário via JSON e chama o controlador para realizar o cadastro.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados do calendário cadastrado.
    """
    return calendario_controller.cadastrar_calendario()


@calendario_bp.route("/", methods=['GET'])
def listar_calendarios() -> jsonify:
    """Rota para listar todos os calendários cadastrados.

    Esta rota retorna uma lista de todos os calendários cadastrados no sistema.

    Returns:
        jsonify: Resposta JSON contendo uma lista de calendários.
    """
    return calendario_controller.listar_calendarios()


@calendario_bp.route("/<int:ano_letivo>", methods=['GET'])
def buscar_calendario(ano_letivo: int) -> jsonify:
    """Rota para buscar um calendário específico pelo ano letivo.

    Esta rota recebe o ano letivo de um calendário e retorna os dados do calendário correspondente.

    Args:
        ano_letivo (int): O ano letivo do calendário a ser buscado.

    Returns:
        jsonify: Resposta JSON contendo os dados do calendário encontrado.
    """
    return calendario_controller.buscar_calendario(ano_letivo)