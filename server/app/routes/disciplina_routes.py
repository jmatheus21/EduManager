"""
Módulo de Rotas para Disciplinas.

Este módulo define as rotas relacionadas às operações de disciplinas no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `disciplina_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import disciplina_controller

# Cria um Blueprint para as rotas de disciplinas
disciplina_bp = Blueprint("disciplina", __name__)


@disciplina_bp.route("/", methods=['POST'])
def cadastrar_disciplina() -> jsonify:
    """Rota para cadastrar uma nova disciplina.

    Esta rota recebe os dados de uma disciplina via JSON e chama o controlador para realizar o cadastro.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados da disciplina cadastrada.
    """
    return disciplina_controller.cadastrar_disciplina()


@disciplina_bp.route("/", methods=['GET'])
def listar_disciplinas() -> jsonify:
    """Rota para listar todas as disciplinas cadastradas.

    Esta rota retorna uma lista de todas as disciplinas cadastradas no sistema.

    Returns:
        jsonify: Resposta JSON contendo uma lista de disciplinas.
    """
    return disciplina_controller.listar_disciplinas


@disciplina_bp.route("/<string:codigo>", methods=['GET'])
def buscar_disciplina(codigo: str) -> jsonify:
    """Rota para buscar uma disciplina específica pelo código.

    Esta rota recebe o código de uma disciplina e retorna os dados da disciplina correspondente.

    Args:
        codigo (str): O código da disciplina a ser buscada.

    Returns:
        jsonify: Resposta JSON contendo os dados da disciplina encontrada.
    """
    return disciplina_controller.buscar_disciplina(codigo)


@disciplina_bp.route("/<string:codigo>", methods=['PUT'])
def alterar_disciplina(codigo: str) -> jsonify:
    """Rota para alterar os dados de uma disciplina existente.

    Esta rota recebe o código de uma disciplina e os novos dados via JSON, e chama o controlador para realizar a atualização.

    Args:
        código (str): O código da disciplina a ser alterada.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados atualizados da disciplina.
    """
    return disciplina_controller.alterar_disciplina(codigo)


@disciplina_bp.route("/<string:codigo>", methods=['DELETE'])
def remover_disciplina(codigo: str) -> jsonify:
    """Rota para remover uma disciplina existente.

    Esta rota recebe o código de uma disciplina e chama o controlador para realizar a remoção.

    Args:
        codigo (str): O código da disciplina a ser removida.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    return disciplina_controller.remover_disciplina(codigo)