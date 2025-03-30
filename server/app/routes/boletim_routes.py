"""
Módulo de Rotas para Boletins.

Este módulo define as rotas relacionadas às operações de boletins no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `boletim_controller`.
"""

from flask import Blueprint, jsonify, request
from ..controllers import boletim_controller
from ..middlewares.token_middleware import token_required


# Cria um Blueprint para as rotas de notas
boletim_bp = Blueprint("boletim", __name__)


@boletim_bp.route("/", methods=['GET'])
@token_required
def listar_aulas_professor(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para listar todas as turmas e disciplinas do professor.

    Esta rota retorna uma lista de todas as turmas e disciplinas associadas ao professor que estão cadastrados no sistema.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma lista de turmas e disciplinas do professor.
    """
    return boletim_controller.listar_aulas_professor(current_user_cpf, current_user_role)


@boletim_bp.route("/<string:aluno_matricula>", methods=['GET'])
@token_required
def gerar_boletim(aluno_matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para gerar o boletim do aluno.

    Esta rota retorna o boletim do aluno.

    Args:
        aluno_matricula (str): A matrícula do aluno.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo o boletim do aluno.
    """
    if request.args.get('preview'):
        return boletim_controller.buscar_boletim(aluno_matricula, current_user_cpf, current_user_role)
    else:
        return boletim_controller.gerar_boletim(aluno_matricula, current_user_cpf, current_user_role)


@boletim_bp.route("/historico/<string:aluno_matricula>", methods=['GET'])
@token_required
def gerar_historico(aluno_matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para gerar o histórico do aluno.

    Esta rota retorna o histórico do aluno.

    Args:
        aluno_matricula (str): A matrícula do aluno.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo o histórico do aluno.
    """
    if request.args.get('preview'):
        return boletim_controller.buscar_historico(aluno_matricula, current_user_cpf, current_user_role)
    else:
        return boletim_controller.gerar_historico(aluno_matricula, current_user_cpf, current_user_role)