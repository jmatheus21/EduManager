"""
Módulo de Rotas para Notas.

Este módulo define as rotas relacionadas às operações de notas no sistema.
Ele utiliza Flask Blueprint para organizar as rotas e delega a lógica de negócio ao módulo `notas_controller`.
"""

from flask import Blueprint, jsonify
from ..controllers import notas_controller
from ..middlewares.token_middleware import token_required

# Cria um Blueprint para as rotas de notas
notas_bp = Blueprint("notas", __name__)

@notas_bp.route("/", methods=['POST'])
@token_required
def cadastrar_notas(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para cadastrar as notas dos alunos referentes à uma aula específica.

    Esta rota recebe os dados de uma aula via JSON e chama o controlador para realizar o cadastro das notas dos alunos.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem confirmando o cadastro das notas dos alunos.
    """
    return notas_controller.cadastrar_notas(current_user_cpf, current_user_role)


@notas_bp.route("/<int:aula_id>", methods=['GET'])
@token_required
def buscar_notas_aula(aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para buscar notas de todos os alunos associados a uma aula específica

    Esta rota recebe o id da aula e retorna as notas de todos os alunos referentes à aula.

    Args:
        aula_id (int): O id da aula a ser buscada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo as notas de todos os alunos da aula.
    """
    return notas_controller.buscar_notas_aula(aula_id, current_user_cpf, current_user_role)


@notas_bp.route("/<string:aluno_matricula>/<int:aula_id>", methods=['GET'])
@token_required
def buscar_notas_aluno(aluno_matricula: str, aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para buscar as notas de um aluno específico pela id da turma, código da disciplina e matrícula do aluno.

    Esta rota recebe o id da turma, código da disciplina e matrícula do aluno e retorna as notas de um aluno específico referentes à uma aula específica.

    Args:
        aluno_matricula (str): A matrícula do aluno.
        aula_id (int): O id da aula que o aluno faz parte.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo as notas do aluno encontrado.
    """
    return notas_controller.buscar_notas_aluno(aluno_matricula, aula_id, current_user_cpf, current_user_role)


@notas_bp.route("/<string:aluno_matricula>/<int:aula_id>", methods=['PUT'])
@token_required
def alterar_notas(aluno_matricula: str, aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Rota para alterar as notas de um aluno associado à uma aula específica.

    Esta rota recebe a matrícula do aluno, o id da turma e o código da disciplina e as novas notas via JSON, e chama o controlador para realizar a atualização.

    Args:
        aluno_matricula (str): A matrícula do aluno.
        aula_id (int): O id da aula que o aluno faz parte.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de confirmação de atualização das notas.
    """
    return notas_controller.alterar_notas(aluno_matricula, aula_id, current_user_cpf, current_user_role)