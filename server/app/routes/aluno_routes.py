"""
Módulo de Rotas para Alunos.

Este módulo define as rotas relacionadas às operações de alunos no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `aluno_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import aluno_controller
from app.middlewares.token_middleware import token_required


# Cria um Blueprint para as rotas de alunos
aluno_bp = Blueprint("aluno", __name__)


@aluno_bp.route("/", methods=['POST'])
@token_required
def cadastrar_aluno(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para cadastrar um novo aluno.

    Esta rota recebe os dados de um aluno via JSON e chama o controlador para realizar o cadastro.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo um mensagem e os dados do aluno cadastrado.
    """
    return aluno_controller.cadastrar_aluno(current_user_cpf, current_user_role)


@aluno_bp.route("/matricula", methods=['POST'])
@token_required
def matricular_aluno(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para matricular um aluno.

    Esta rota permite associar um aluno a uma nova turma.
    
    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    return aluno_controller.matricular_aluno(current_user_cpf, current_user_role)


@aluno_bp.route("/", methods=['GET'])
@token_required
def listar_alunos(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para listar todos os alunos cadastrados.

    Esta rota retorna uma lista de todos os alunos cadastrados no sistema.
    
    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma lista de alunos.
    """
    return aluno_controller.listar_alunos(current_user_cpf, current_user_role)


@aluno_bp.route("/<string:matricula>", methods=['GET'])
@token_required
def buscar_alunos(matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para buscar um aluno específico pela matricula.

    Esta rota recebe a matricula de uma aluno e retorna os dados da aluno correspondente.

    Args:
        matricula (str): A matricula da aluno a ser buscada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo os dados do aluno encontrado.
    """
    return aluno_controller.buscar_aluno(matricula, current_user_cpf, current_user_role)


@aluno_bp.route("/<string:matricula>", methods=['PUT'])
@token_required
def alterar_aluno(matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para alterar os dados de um aluno existente.

    Esta rota recebe a matrícula de um aluno e os novos dados via JSON, e chama o controlador para realizar a atualização.

    Args:
        matricula (str): A matricula do aluno a ser alterado.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados atualizados do aluno.
    """
    return aluno_controller.alterar_aluno(matricula, current_user_cpf, current_user_role)


@aluno_bp.route("/<string:matricula>", methods=['DELETE'])
@token_required
def remover_aluno(matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para remover um aluno existente.

    Esta rota recebe a matricula de um aluno e chama o controlador para realizar a remoção.

    Args:
        matricula (str): A matricula do aluno a ser removido.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    return aluno_controller.remover_aluno(matricula, current_user_cpf, current_user_role)