"""
Módulo de Rotas para Ausências.

Este módulo define as rotas relacionadas às operações de ausências no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `ausencias_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import ausencias_controller
from ..middlewares.token_middleware import token_required


# Cria um Blueprint para as rotas de aulas
ausencias_bp = Blueprint("ausencias", __name__)


@ausencias_bp.route("/<int:aula_id>", methods=['PUT'])
@token_required
def registrar_ausencias(aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para registrar as ausencias dos alunos de uma aula.

    Esta rota recebe o id de uma aula e os novos dados via JSON, e chama o controlador para realizar a atualização.

    Args:
        aula_id (int): Id da aula. 
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem e os dados atualizados da ausência.
    """
    return ausencias_controller.registrar_ausencias(aula_id, current_user_cpf, current_user_role)


@ausencias_bp.route("/<int:aula_id>", methods=['GET'])
@token_required
def buscar_ausencias_aula(aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para listar todos os alunos cadastrados nas aulas específicas.

    Esta rota retorna uma lista de todos os alunos cadastradas num aula específica.

    Args:
        aula_id (int): Id da aula. 
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma lista de alunos.
    """
    return ausencias_controller.buscar_ausencias_aula(aula_id, current_user_cpf, current_user_role)


@ausencias_bp.route("/<int:aula_id>/<string:aluno_matricula>", methods=['GET'])
@token_required
def buscar_ausencias_aluno(aluno_matricula: str, aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para buscar um aluno e uma aula específica específico pela matrícula e pelo id da turma e codigo da disciplina.

    Esta rota recebe o id de uma aula, a matrícula do aluno e retorna os dados da aula correspondente.

    Args:
        aluno_matricula (str): A matrícula do aluno a ser buscado.
        aula_id (int): O ID da aula.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo os dados da aula encontrada.
    """
    return ausencias_controller.buscar_ausencias_aluno(aluno_matricula, aula_id, current_user_cpf, current_user_role)


@ausencias_bp.route("/<int:aula_id>/<string:aluno_matricula>", methods=['PUT'])
@token_required
def alterar_ausencia(aluno_matricula: str, aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
     """Rota para alterar as ausencias de um aluno em uma aula.

     Esta rota recebe o id de uma aula, a matrícula do aluno e os novos dados via JSON, e chama o controlador para realizar a atualização.

     Args:
        aluno_matricula (str): A matrícula do aluno a ser buscado.
        aula_id (int): O ID da aula.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

     Returns:
         jsonify: Resposta JSON contendo uma mensagem e os dados atualizados da ausência.
     """
     return ausencias_controller.alterar_ausencia(aluno_matricula, aula_id, current_user_cpf, current_user_role)
