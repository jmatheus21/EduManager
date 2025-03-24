"""
Módulo de Rotas para Usuários.

Este módulo define as rotas relacionadas às operações dos usuários no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `usuario_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import usuario_controller
from ..middlewares.token_middleware import token_required


# Cria um Blueprint para as rotas de usuários
usuario_bp = Blueprint("usuario", __name__)


@usuario_bp.route("/", methods = ['POST'])
def cadastrar_usuario() -> jsonify:
    """Rota para cadastrar um novo usuário.

    Esta rota recebe os dados de um usuário via JSON e chama o controlador para realizar o cadastro.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados do usuário cadastrado.
    """
    return usuario_controller.cadastrar_usuario()


@usuario_bp.route("/", methods=['GET'])
@token_required
def listar_usuarios(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para listar todos os usuários cadastrados.

    Esta rota retorna uma lista de todos os usuários cadastrados no sistema.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma lista de usuários.
    """
    return usuario_controller.listar_usuarios(current_user_cpf, current_user_role)


@usuario_bp.route("/<string:cpf>", methods=['GET'])
@token_required
def buscar_usuario(cpf : str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para buscar um usuário específico pelo cpf.

    Esta rota recebe o cpf de um usuário e retorna os dados do usuário correspondente.

    Args:
        cpf (str): O cpf do usuário a ser buscado.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo os dados do usuário encontrado.
    """
    return usuario_controller.buscar_usuario(cpf, current_user_cpf, current_user_role)

@usuario_bp.route("/<string:cpf>", methods=['PUT'])
@token_required
def alterar_usuario(cpf: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para alterar os dados de uma usuário existente.

    Esta rota recebe o cpf de um usuário e os novos dados via JSON, e chama o controlador para realizar a atualização.

    Args:
        cpf (str): O cpf do usuário a ser alterado.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados atualizados do usuário.
    """
    return usuario_controller.alterar_usuario(cpf, current_user_cpf, current_user_role)

@usuario_bp.route("/<string:cpf>", methods=['DELETE'])
@token_required
def remover_usuario(cpf: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para remover um usuário existente.

    Esta rota recebe o cpf de um usuário e chama o controlador para realizar a remoção.

    Args:
        cpf (str): O CPF do usuário a ser removido.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    return usuario_controller.remover_usuario(cpf, current_user_cpf, current_user_role)