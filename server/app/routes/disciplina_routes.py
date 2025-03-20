"""
Módulo de Rotas para Disciplinas.

Este módulo define as rotas relacionadas às operações de disciplinas no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `disciplina_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import disciplina_controller
from ..middlewares.token_middleware import token_required

# Cria um Blueprint para as rotas de disciplinas
disciplina_bp = Blueprint("disciplina", __name__)


@disciplina_bp.route("/", methods=['POST'])
@token_required
def cadastrar_disciplina(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para cadastrar uma nova disciplina.

    Esta rota recebe os dados de uma disciplina via JSON e chama o controlador para realizar o cadastro.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados da disciplina cadastrada.
    """
    return disciplina_controller.cadastrar_disciplina(current_user_cpf, current_user_role)


@disciplina_bp.route("/", methods=['GET'])
@token_required
def listar_disciplinas(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para listar todas as disciplinas cadastradas.

    Esta rota retorna uma lista de todas as disciplinas cadastradas no sistema.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma lista de disciplinas.
    """
    return disciplina_controller.listar_disciplinas(current_user_cpf, current_user_role)


@disciplina_bp.route("/<string:codigo>", methods=['GET'])
@token_required
def buscar_disciplina(codigo: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para buscar uma disciplina específica pelo código.

    Esta rota recebe o código de uma disciplina e retorna os dados da disciplina correspondente.

    Args:
        codigo (str): O código da disciplina a ser buscada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo os dados da disciplina encontrada.
    """
    return disciplina_controller.buscar_disciplina(codigo, current_user_cpf, current_user_role)


@disciplina_bp.route("/<string:codigo>", methods=['PUT'])
@token_required
def alterar_disciplina(codigo: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para alterar os dados de uma disciplina existente.

    Esta rota recebe o código de uma disciplina e os novos dados via JSON, e chama o controlador para realizar a atualização.

    Args:
        código (str): O código da disciplina a ser alterada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados atualizados da disciplina.
    """
    return disciplina_controller.alterar_disciplina(codigo, current_user_cpf, current_user_role)


@disciplina_bp.route("/<string:codigo>", methods=['DELETE'])
@token_required
def remover_disciplina(codigo: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para remover uma disciplina existente.

    Esta rota recebe o código de uma disciplina e chama o controlador para realizar a remoção.

    Args:
        codigo (str): O código da disciplina a ser removida.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    return disciplina_controller.remover_disciplina(codigo, current_user_cpf, current_user_role)