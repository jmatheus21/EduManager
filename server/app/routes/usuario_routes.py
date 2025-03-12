"""
Módulo de Rotas para Usuários.

Este módulo define as rotas relacionadas às operações dos usuários no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `usuario_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import usuario_controller

# Cria um Blueprint para as rotas de usuários
usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/", methods = ['POST'])
def cadastrar_usuario() -> jsonify:
    """Rota para cadastrar um novo usuário.

    Esta rota recebe os dados de um usuário via JSON e chama o controlador para realizar o cadastro.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados do usuário cadastrado.
    """
    return usuario_controller.cadastrar_usuario()


@usuario_bp.route("/", methods=['GET'])
def listar_usuarios() -> jsonify:
    """Rota para listar todos os usuários cadastrados.

    Esta rota retorna uma lista de todos os usuários cadastrados no sistema.

    Returns:
        jsonify: Resposta JSON contendo uma lista de usuários.
    """
    return usuario_controller.listar_usuarios()


@usuario_bp.route("/<string:cpf>", methods=['GET'])
def buscar_usuario(cpf : str) -> jsonify:
    """Rota para buscar um usuário específico pelo cpf.

    Esta rota recebe o cpf de um usuário e retorna os dados do usuário correspondente.

    Args:
        cpf (str): O cpf do usuário a ser buscado.

    Returns:
        jsonify: Resposta JSON contendo os dados do usuário encontrado.
    """
    return usuario_controller.buscar_usuario(cpf)