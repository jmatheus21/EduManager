"""
Módulo de Rotas para Calendários.

Este módulo define as rotas relacionadas às operações dos calendários no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `calendario_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import calendario_controller
from ..middlewares.token_middleware import token_required

# Cria um Blueprint para as rotas de calendário
calendario_bp = Blueprint("calendario", __name__)


@calendario_bp.route("/", methods=['POST'])
@token_required
def cadastrar_calendario(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para cadastrar um novo calendário.

    Esta rota recebe os dados de um calendário via JSON e chama o controlador para realizar o cadastro.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados do calendário cadastrado.
    """
    return calendario_controller.cadastrar_calendario(current_user_cpf, current_user_role)


@calendario_bp.route("/", methods=['GET'])
@token_required
def listar_calendarios(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para listar todos os calendários cadastrados.

    Esta rota retorna uma lista de todos os calendários cadastrados no sistema.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma lista de calendários.
    """
    return calendario_controller.listar_calendarios(current_user_cpf, current_user_role)


@calendario_bp.route("/<int:ano_letivo>", methods=['GET'])
@token_required
def buscar_calendario(ano_letivo: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para buscar um calendário específico pelo ano letivo.

    Esta rota recebe o ano letivo de um calendário e retorna os dados do calendário correspondente.

    Args:
        ano_letivo (int): O ano letivo do calendário a ser buscado.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo os dados do calendário encontrado.
    """
    return calendario_controller.buscar_calendario(ano_letivo, current_user_cpf, current_user_role)


@calendario_bp.route("/<int:ano_letivo>", methods=['PUT'])
@token_required
def alterar_calendario(ano_letivo: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para alterar os dados de um calendário existente.

    Esta rota recebe o ano letivo de um calendário e os novos dados via JSON, e chama o controlador para realizar a atualização.

    Args:
        ano_letivo (int): O ano letivo do calendário a ser alterada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados atualizados do calendário.
    """
    return calendario_controller.alterar_calendario(ano_letivo, current_user_cpf, current_user_role)


@calendario_bp.route("/<int:ano_letivo>", methods=['DELETE'])
@token_required
def remover_calendario(ano_letivo: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para remover um calendário existente.

    Esta rota recebe o ano letivo de um calendário e chama o controlador para realizar a remoção.

    Args:
        ano_letivo (int): O ano letivo do calendário a ser removido.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    return calendario_controller.remover_calendario(ano_letivo, current_user_cpf, current_user_role)