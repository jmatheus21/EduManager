"""
Módulo de Rotas para Turmas.

Este módulo define as rotas relacionadas às operações de turmas no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `turma_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import turma_controller

# Cria um Blueprint para as rotas de turmas
turma_bp = Blueprint("turma", __name__)


@turma_bp.route("/", methods=['POST'])
def cadastrar_turma() -> jsonify:
    """Rota para cadastrar uma nova turma.

    Esta rota recebe os dados de uma turma via JSON e chama o controlador para realizar o cadastro.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados da turma cadastrada.
    """
    return turma_controller.cadastrar_turma()


@turma_bp.route("/", methods=['GET'])
def listar_turmas() -> jsonify:
    """Rota para listar todas as turmas cadastradas.

    Esta rota retorna uma lista de todas as turmas cadastradas no sistema.

    Returns:
        jsonify: Resposta JSON contendo uma lista de turmas.
    """
    return turma_controller.listar_turmas()


@turma_bp.route("/<int:id>", methods=['GET'])
def buscar_turmas(id: int) -> jsonify:
    """Rota para buscar uma turma específica pelo id.

    Esta rota recebe o id de uma turma e retorna os dados da turma correspondente.

    Args:
        id (int): O id da turma a ser buscada.

    Returns:
        jsonify: Resposta JSON contendo os dados da turma encontrada.
    """
    return turma_controller.buscar_turma(id)


@turma_bp.route("/<int:id>", methods=['PUT'])
def alterar_turma(id: int) -> jsonify:
    """Rota para alterar os dados de uma turma existente.

    Esta rota recebe o id de uma turma e os novos dados via JSON, e chama o controlador para realizar a atualização.

    Args:
        id (int): O id da turma a ser alterada.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados atualizados da turma.
    """
    return turma_controller.alterar_turma(id)


@turma_bp.route("/<int:id>", methods=['DELETE'])
def remover_turma(id: int) -> jsonify:
    """Rota para remover uma turma existente.

    Esta rota recebe o id de uma turma e chama o controlador para realizar a remoção.

    Args:
        id (int): O id da turma a ser removida.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    return turma_controller.remover_turma(id)