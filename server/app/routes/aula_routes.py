"""
Módulo de Rotas para Aulas.

Este módulo define as rotas relacionadas às operações de aulas no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `aula_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import aula_controller


# Cria um Blueprint para as rotas de aulas
aula_bp = Blueprint("aula", __name__)


@aula_bp.route("/", methods=['POST'])
def cadastrar_aula() -> jsonify:
    """Rota para cadastrar uma nova aula.

    Esta rota recebe os dados de uma aula via JSON e chama o controlador para realizar o cadastro.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados da aula cadastrada.
    """
    return aula_controller.cadastrar_aula()


@aula_bp.route("/", methods=['GET'])
def listar_aulas() -> jsonify:
    """Rota para listar todas as aulas cadastradas.

    Esta rota retorna uma lista de todas as aulas cadastradas no sistema.

    Returns:
        jsonify: Resposta JSON contendo uma lista de aulas.
    """
    return aula_controller.listar_aulas()


@aula_bp.route("/<int:id>", methods=['GET'])
def buscar_aulas(id: int) -> jsonify:
    """Rota para buscar uma aula específica pelo id.

    Esta rota recebe o id de uma aula e retorna os dados da aula correspondente.

    Args:
        id (int): O id da aula a ser buscada.

    Returns:
        jsonify: Resposta JSON contendo os dados da aula encontrada.
    """
    return aula_controller.buscar_aula(id)


# @aula_bp.route("/<int:id>", methods=['PUT'])
# def alterar_aula(id: int) -> jsonify:
#     """Rota para alterar os dados de uma aula existente.

#     Esta rota recebe o id de uma aula e os novos dados via JSON, e chama o controlador para realizar a atualização.

#     Args:
#         id (int): O id da aula a ser alterada.

#     Returns:
#         jsonify: Resposta JSON contendo uma mensagem e os dados atualizados da aula.
#     """
#     return aula_controller.alterar_aula(id)


# @aula_bp.route("/<int:id>", methods=['DELETE'])
# def remover_aula(id: int) -> jsonify:
#     """Rota para remover uma aula existente.

#     Esta rota recebe o id de uma aula e chama o controlador para realizar a remoção.

#     Args:
#         id (int): O id da aula a ser removida.

#     Returns:
#         jsonify: Resposta JSON contendo uma mensagem de sucesso.
#     """
#     return aula_controller.remover_aula(id)