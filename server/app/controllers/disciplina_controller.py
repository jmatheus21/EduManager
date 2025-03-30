"""
Módulo de Controlador para Disciplinas.

Este módulo contém as funções que implementam a lógica de negócio para as operações relacionadas às disciplinas.
Ele interage com o modelo `Disciplina` para realizar operações CRUD e valida os dados usando o módulo `validators`.
"""

from flask import request, jsonify
from app.extensions import db
from ..models import Disciplina
from app.utils.validators import validar_disciplina


def cadastrar_disciplina(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Cadastra uma nova disciplina no banco de dados.

    Esta função recebe os dados de uma disciplina via JSON, valida os dados e, se válidos, cadastra a disciplina no banco de dados.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados da disciplina cadastrada, ou uma mensagem de erro em caso de dados inválidos.
    """
    data = request.get_json()

    erros = validar_disciplina(codigo=data['codigo'], nome=data['nome'], carga_horaria=data['carga_horaria'], ementa=data['ementa'], bibliografia=data['bibliografia'])
    if erros:
        return jsonify({"erro": erros}), 400
    
    disciplina_existente = db.session.get(Disciplina, data['codigo'])
    if disciplina_existente is not None:
        return jsonify({"erro": ["Disciplina já existe"]}), 400
    
    nova_disciplina = Disciplina(codigo=data['codigo'], nome=data['nome'], carga_horaria=data['carga_horaria'], ementa=data['ementa'], bibliografia=data['bibliografia'])
    db.session.add(nova_disciplina)
    db.session.commit()
    return jsonify({"mensagem": "Disciplina criada com sucesso!", "data": {"codigo": nova_disciplina.codigo, "nome": nova_disciplina.nome, "carga_horaria": nova_disciplina.carga_horaria, "ementa": nova_disciplina.ementa, "bibliografia": nova_disciplina.bibliografia}}), 201


def listar_disciplinas(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Lista todas as disciplinas cadastradas no banco de dados.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma lista de disciplinas com seus respectivos dados.
    """
    disciplinas = Disciplina.query.all()
    return jsonify([{"codigo": disciplina.codigo, "nome": disciplina.nome, "carga_horaria": disciplina.carga_horaria, "ementa": disciplina.ementa, "bibliografia": disciplina.bibliografia} for disciplina in disciplinas]), 200


def buscar_disciplina(codigo: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Busca uma disciplina específica pelo código.

    Args:
        codigo (str): O código da disciplina a ser buscada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo os dados da disciplina encontrada.
    """
    disciplina = db.session.get(Disciplina, codigo)
    return jsonify({"codigo": disciplina.codigo, "nome": disciplina.nome, "carga_horaria": disciplina.carga_horaria, "ementa": disciplina.ementa, "bibliografia": disciplina.bibliografia}), 200


def alterar_disciplina(codigo: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Altera os dados de uma disciplina existente.

    Esta função recebe o código de uma disciplina e os novos dados via JSON, valida os dados e, se válidos, atualiza a disciplina no banco de dados.

    Args:
        codigo (str): O código da disciplina a ser alterada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados atualizados da disciplina, ou uma mensagem de erro em caso de dados inválidos.
    """
    disciplina = db.session.get(Disciplina, codigo)
    data = request.get_json()

    erros = validar_disciplina(codigo=data['codigo'], nome=data['nome'], carga_horaria=data['carga_horaria'], ementa=data['ementa'], bibliografia=data['bibliografia'])
    if erros:
        return jsonify({"erro": erros}), 400
    
    if codigo != data['codigo']:
        disciplina_existente = db.session.get(Disciplina, data['codigo']);
        if disciplina_existente is not None:
            return jsonify({"erro": ["Disciplina já existe"]}), 400;

    disciplina.codigo = data['codigo']
    disciplina.nome = data['nome']
    disciplina.carga_horaria = data['carga_horaria']
    disciplina.ementa = data['ementa']
    disciplina.bibliografia = data['bibliografia']
    db.session.commit()

    return jsonify({"mensagem": "Disciplina atualizada com sucesso!", "data": {"codigo": disciplina.codigo, "nome": disciplina.nome, "carga_horaria": disciplina.carga_horaria, "ementa": disciplina.ementa, "bibliografia": disciplina.bibliografia}}), 200


def remover_disciplina(codigo: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Remove uma disciplina existente do banco de dados.

    Args:
        codigo (str): O código da disciplina a ser removida.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    disciplina = db.session.get(Disciplina, codigo)
    db.session.delete(disciplina)
    db.session.commit()
    return jsonify({"mensagem": "Disciplina deletada com sucesso!"}), 200