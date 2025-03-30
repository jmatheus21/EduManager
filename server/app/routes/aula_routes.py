"""
Módulo de Rotas para Aulas.

Este módulo define as rotas relacionadas às operações de aulas no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `aula_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import aula_controller
from ..middlewares.token_middleware import token_required


# Cria um Blueprint para as rotas de aulas
aula_bp = Blueprint("aula", __name__)


@aula_bp.route("/", methods=['POST'])
@token_required
def cadastrar_aula(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para cadastrar uma nova aula.

    Esta rota recebe os dados de uma aula via JSON e chama o controlador para realizar o cadastro.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados da aula cadastrada.
    """
    return aula_controller.cadastrar_aula(current_user_cpf, current_user_role)


@aula_bp.route("/", methods=['GET'])
@token_required
def listar_aulas(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para listar todas as aulas cadastradas.

    Esta rota retorna uma lista de todas as aulas cadastradas no sistema.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma lista de aulas.
    """
    return aula_controller.listar_aulas(current_user_cpf, current_user_role)


@aula_bp.route("/<int:id>", methods=['GET'])
@token_required
def buscar_aulas(id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para buscar uma aula específica pelo id.

    Esta rota recebe o id de uma aula e retorna os dados da aula correspondente.

    Args:
        id (int): O id da aula a ser buscada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo os dados da aula encontrada.
    """
    return aula_controller.buscar_aula(id, current_user_cpf, current_user_role)


@aula_bp.route("/<int:id>", methods=['PUT'])
@token_required
def alterar_aula(id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para alterar os dados de uma aula existente.

    Esta rota recebe o id de uma aula e os novos dados via JSON, e chama o controlador para realizar a atualização.

    Args:
        id (int): O id da aula a ser alterada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados atualizados da aula.
    """
    return aula_controller.alterar_aula(id, current_user_cpf, current_user_role)


@aula_bp.route("/<int:id>", methods=['DELETE'])
@token_required
def remover_aula(id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para remover uma aula existente.

    Esta rota recebe o id de uma aula e chama o controlador para realizar a remoção.

    Args:
        id (int): O id da aula a ser removida.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    return aula_controller.remover_aula(id, current_user_cpf, current_user_role)