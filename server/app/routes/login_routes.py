"""
Módulo de Rotas para Login.

Este módulo define as rotas relacionadas às operações de login no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `login_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import login_controller
from ..middlewares.token_middleware import token_required

# Cria um Blueprint para as rotas de login
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=['POST'])
def login () -> jsonify:
    """Rota para realizar o login do usuário.

    Esta rota recebe os dados de um usuário via JSON, valida os dados e, se válidos, realiza o login do usuário no sistema.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem confirmando o login.
    """
    return login_controller.login()


@auth_bp.route("/validate", methods=['GET'])
@token_required
def validate (current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para validar o login do usuário.

    Esta rota recebe os dados de um usuário via banco de dados, valida os dados e, se válidos, valida a entrada do usuário no sistema.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem confirmando o login.
    """
    return login_controller.validate(current_user_cpf, current_user_role)


@auth_bp.route("/logout", methods=['GET'])
def logout () -> jsonify:
    """Rota para realizar o logout do usuário.

    Esta rota recebe os dados de um usuário via JSON, valida os dados e, se válidos, realiza o logout do usuário no sistema.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem confirmando o logout.
    """
    return login_controller.logout()