"""
Módulo de Rotas para Turmas.

Este módulo define as rotas relacionadas às operações de turmas no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `turma_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import turma_controller
from ..middlewares.token_middleware import token_required


# Cria um Blueprint para as rotas de turmas
turma_bp = Blueprint("turma", __name__)


@turma_bp.route("/", methods=['POST'])
@token_required
def cadastrar_turma(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para cadastrar uma nova turma.

    Esta rota recebe os dados de uma turma via JSON e chama o controlador para realizar o cadastro.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados da turma cadastrada.
    """
    return turma_controller.cadastrar_turma(current_user_cpf, current_user_role)


@turma_bp.route("/", methods=['GET'])
@token_required
def listar_turmas(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para listar todas as turmas cadastradas.

    Esta rota retorna uma lista de todas as turmas cadastradas no sistema.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma lista de turmas.
    """
    return turma_controller.listar_turmas(current_user_cpf, current_user_role)


@turma_bp.route("/<int:id>", methods=['GET'])
@token_required
def buscar_turmas(id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para buscar uma turma específica pelo id.

    Esta rota recebe o id de uma turma e retorna os dados da turma correspondente.

    Args:
        id (int): O id da turma a ser buscada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo os dados da turma encontrada.
    """
    return turma_controller.buscar_turma(id, current_user_cpf, current_user_role)


@turma_bp.route("/<int:id>", methods=['PUT'])
@token_required
def alterar_turma(id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para alterar os dados de uma turma existente.

    Esta rota recebe o id de uma turma e os novos dados via JSON, e chama o controlador para realizar a atualização.

    Args:
        id (int): O id da turma a ser alterada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados atualizados da turma.
    """
    return turma_controller.alterar_turma(id, current_user_cpf, current_user_role)


@turma_bp.route("/<int:id>", methods=['DELETE'])
@token_required
def remover_turma(id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para remover uma turma existente.

    Esta rota recebe o id de uma turma e chama o controlador para realizar a remoção.

    Args:
        id (int): O id da turma a ser removida.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    return turma_controller.remover_turma(id, current_user_cpf, current_user_role)