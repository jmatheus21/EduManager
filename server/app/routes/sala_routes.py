"""
Módulo de Rotas para Salas.

Este módulo define as rotas relacionadas às operações de salas no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `sala_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import sala_controller
from ..middlewares.token_middleware import token_required


# Cria um Blueprint para as rotas de salas
sala_bp = Blueprint("sala", __name__)


@sala_bp.route("/", methods=['POST'])
@token_required
def cadastrar_sala(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para cadastrar uma nova sala.

    Esta rota recebe os dados de uma sala via JSON e chama o controlador para realizar o cadastro.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados da sala cadastrada.
    """
    return sala_controller.cadastrar_sala(current_user_cpf, current_user_role)


@sala_bp.route("/", methods=['GET'])
@token_required
def listar_salas(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para listar todas as salas cadastradas.

    Esta rota retorna uma lista de todas as salas cadastradas no sistema.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma lista de salas.
    """
    return sala_controller.listar_salas(current_user_cpf, current_user_role)


@sala_bp.route("/<int:numero>", methods=['GET'])
@token_required
def buscar_sala(numero: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para buscar uma sala específica pelo número.

    Esta rota recebe o número de uma sala e retorna os dados da sala correspondente.

    Args:
        numero (int): O número da sala a ser buscada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo os dados da sala encontrada.
    """
    return sala_controller.buscar_sala(numero, current_user_cpf, current_user_role
)


@sala_bp.route("/<int:numero>", methods=['PUT'])
@token_required
def alterar_sala(numero: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para alterar os dados de uma sala existente.

    Esta rota recebe o número de uma sala e os novos dados via JSON, e chama o controlador para realizar a atualização.

    Args:
        numero (int): O número da sala a ser alterada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados atualizados da sala.
    """
    return sala_controller.alterar_sala(numero, current_user_cpf, current_user_role)


@sala_bp.route("/<int:numero>", methods=['DELETE'])
@token_required
def remover_sala(numero: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para remover uma sala existente.

    Esta rota recebe o número de uma sala e chama o controlador para realizar a remoção.

    Args:
        numero (int): O número da sala a ser removida.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    return sala_controller.remover_sala(numero, current_user_cpf, current_user_role)