"""
Módulo de Controlador para Aluno

Este módulo contém as funções que implementam a lógica de negócio para as operações relacionadas aos Alunos.
Ele interage com o modelo `Aluno` para realizar operações CRUD e valida os dados usando o módulo `validators`.
"""

from flask import request, jsonify
from app.extensions import db
from ..models import Aluno, Turma
from app.utils.validators import validar_aluno


def cadastrar_aluno() -> jsonify:
    """Cadastra um novo aluno no banco de dados.

    Esta função recebe os dados de um aluno via JSON, valida os dados e, se válidos, cadastra o aluno no banco de dados.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados da turma cadastrada, ou uma mensagem de erro em caso de dados inválidos.
    """

    data = request.get_json()

    #  "202600000001"
    erros = validar_aluno(matricula=data['matricula'], nome=data['nome'], email=data['email'], telefone=data['telefone'], endereco=data['endereco'], data_de_nascimento=data['data_de_nascimento'])
    if erros:
        return jsonify({"erro": erros }), 400
    
    aluno_existente = db.session.query(Aluno).filter_by(matricula=data['matricula']).first()
    if aluno_existente is not None:
        return jsonify({"erro": ["Matrícula já existe"]}), 400

    email_existente = db.session.query(Aluno).filter_by(email= data['email']).first()
    if email_existente:
        return jsonify({"erro": ["E-mail já existe"]}), 400
    
    # Verifica se a turma está aberta
    # id -> turma_id
    turma_fechada = db.session.query(Turma).filter_by(id=data['turma_id']).first()
    if turma_fechada is not None and turma_fechada.status == "C":
        return jsonify({"erro": ["A turma está fechada, portanto, não é possível cadastrar mais alunos"]}), 400

    # Verifica se a turma existe
    # id -> turma_id
    turma_existente = db.session.query(Turma).filter_by(id=data['turma_id']).first()
    if turma_existente is None:
        return jsonify({"erro": ["Turma não existe"]}), 400
    
    novo_aluno = Aluno(matricula=data['matricula'], nome=data['nome'], email=data['email'], telefone=data['telefone'], endereco=data['endereco'], data_de_nascimento=data['data_de_nascimento'])
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify({"mensagem": "Aluno criado com sucesso!", "data": {"matricula": novo_aluno.matricula, "nome": novo_aluno.nome, "email": novo_aluno.email, "telefone": novo_aluno.telefone, "endereco": novo_aluno.endereco, "data_de_nascimento": novo_aluno.data_de_nascimento}}), 201


def listar_alunos() -> jsonify:
    """Lista todas os alunos cadastrados no banco de dados.

    Returns:
        jsonify: Resposta JSON contendo uma lista de alunos com seus respectivos dados.
    """
    alunos = Aluno.query.all()
    
    return jsonify([{"matricula": aluno.matricula, "nome": aluno.nome, "email": aluno.email, "telefone": aluno.telefone, "endereco": aluno.endereco, "data_de_nascimento": aluno.data_de_nascimento} for aluno in alunos]), 200


def buscar_aluno(matricula: str) -> jsonify:
    """Busca um aluno específico pela matrícula.

    Args:
        matricula (str): A matricula do aluno a ser buscado.

    Returns:
        jsonify: Resposta JSON contendo os dados do aluno encontrado.
    """
    aluno = db.session.get(Aluno, matricula)
    return jsonify({"matricula": aluno.matricula, "nome": aluno.nome, "email": aluno.email, "telefone": aluno.telefone, "endereco": aluno.endereco, "data_de_nascimento": aluno.data_de_nascimento}), 200
