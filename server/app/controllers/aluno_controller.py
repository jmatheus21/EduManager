"""
Módulo de Controlador para Aluno

Este módulo contém as funções que implementam a lógica de negócio para as operações relacionadas aos Alunos.
Ele interage com o modelo `Aluno` para realizar operações CRUD e valida os dados usando o módulo `validators`.
"""

from flask import request, jsonify
from app.extensions import db
from ..models import Aluno, Turma
from app.utils.validators import validar_aluno
from app.utils.date_helpers import string_para_data
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes

def cadastrar_aluno(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Cadastra um novo aluno no banco de dados.

    Esta função recebe os dados de um aluno via JSON, valida os dados e, se válidos, cadastra o aluno no banco de dados.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados da turma cadastrada, ou uma mensagem de erro em caso de dados inválidos.
    """

    data = request.get_json()

    erros = validar_aluno(nome=data['nome'], email=data['email'], telefone=data['telefone'], endereco=data['endereco'], data_de_nascimento=data['data_de_nascimento'])
    if erros:
        return jsonify({"erro": erros }), 400

    # Verifica se a turma existe
    turma_existente = db.session.get(Turma, data["turma_id"])
    if turma_existente is None:
        return jsonify({"erro": ["Turma não existe"]}), 400

    # criar lógica para matrícula
    id = db.session.query(Aluno).count() + 1
    matricula = f"{turma_existente.calendario_ano_letivo}000{id:05d}"
    
    aluno_existente = db.session.query(Aluno).filter_by(matricula=matricula).first()
    if aluno_existente is not None:
        return jsonify({"erro": ["Matrícula já existe"]}), 400

    email_existente = db.session.query(Aluno).filter_by(email= data['email']).first()
    if email_existente:
        return jsonify({"erro": ["E-mail já existe"]}), 400
    
    # Verifica se a turma está aberta
    # id -> turma_id
    if turma_existente.status != "A":
        return jsonify({"erro": ["A turma está fechada, portanto, não é possível cadastrar mais alunos"]}), 400
    
    novo_aluno = Aluno(matricula=matricula, nome=data['nome'], email=data['email'], telefone=data['telefone'], endereco=data['endereco'], data_de_nascimento=data['data_de_nascimento'])
    novo_aluno.turmas.append(turma_existente)
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify({"mensagem": "Aluno criado com sucesso!", "data": {"matricula": novo_aluno.matricula, "nome": novo_aluno.nome, "email": novo_aluno.email, "telefone": novo_aluno.telefone, "endereco": novo_aluno.endereco, "data_de_nascimento": novo_aluno.data_de_nascimento, "turma_id": turma_existente.id}}), 201

def matricular_aluno(current_user_cpf: str, current_user_role: str) -> jsonify:

    data = request.get_json()

    matricula = data["aluno_matricula"]
    id = data["turma_id"]

    if not matricula or not isinstance(matricula, str) or len(matricula) != 12:
        return jsonify({"erro": ["A matrícula do aluno é inválida"]}), 400
    
    if not id or not isinstance(id, int) or id <= 0:
        return jsonify({"erro": ["O id da turma é inválido"]}), 400
    
    aluno = db.session.get(Aluno, matricula)
    if aluno is None:
        return jsonify({"erro": ["Não existe aluno com essa matrícula"]}), 400
    
    turma = db.session.get(Turma, id)
    if turma is None:
        return jsonify({"erro": ["Não existe turma com esse id"]}), 400
    
    if turma.status != "A":
        return jsonify({"erro": ["A turma informada não está ativa"]}), 400
    
    if turma in aluno.turmas:
        return jsonify({"erro": ["Aluno já está matriculado nessa turma"]}), 400
    
    aluno.turmas.append(turma)

    return jsonify({"messagem": "Aluno matriculado com sucesso!"}), 201


def listar_alunos(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Lista todas os alunos cadastrados no banco de dados.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma lista de alunos com seus respectivos dados.
    """
    alunos = Aluno.query.all()

    return jsonify([{"matricula": aluno.matricula, "nome": aluno.nome, "email": aluno.email, "telefone": aluno.telefone, "endereco": aluno.endereco, "data_de_nascimento": aluno.data_de_nascimento, "turma_id": max(aluno.turmas, key=lambda turma: turma.calendario_ano_letivo).id} for aluno in alunos]), 200


def buscar_aluno(matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Busca um aluno específico pela matrícula.

    Args:
        matricula (str): A matricula do aluno a ser buscado.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo os dados do aluno encontrado.
    """
    aluno = db.session.get(Aluno, matricula)
<<<<<<< Updated upstream
    turma_atual = max(aluno.turmas, key=lambda turma: turma.calendario_ano_letivo)

    if turma_atual.status != "A":
        turma_atual = "Não matriculado"

    return jsonify({"matricula": aluno.matricula, "nome": aluno.nome, "email": aluno.email, "telefone": aluno.telefone, "endereco": aluno.endereco, "data_de_nascimento": aluno.data_de_nascimento, "turma_id": turma_atual.id}), 200
=======
    return jsonify({"matricula": aluno.matricula, "nome": aluno.nome, "email": aluno.email, "telefone": aluno.telefone, "endereco": aluno.endereco, "data_de_nascimento": aluno.data_de_nascimento}), 200
>>>>>>> Stashed changes


def alterar_aluno(matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Altera os dados de um aluno existente.

    Esta função recebe a matrícula de um aluno e os novos dados via JSON, valida os dados e, se válidos, atualiza o aluno no banco de dados.

    Args:
        matricula (str): A matrícula do aluno a ser alterado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados atualizados do aluno, ou uma mensagem de erro em caso de dados inválidos.
    """
    aluno = db.session.query(Aluno).filter_by(matricula=matricula).first()
    data = request.get_json()
    
    erros = validar_aluno(nome=data['nome'], email=data['email'], telefone=data['telefone'], endereco=data['endereco'], data_de_nascimento=data['data_de_nascimento'])
    if erros:
        return jsonify({"erro": erros}), 400

<<<<<<< Updated upstream
    nova_turma = all(turma.id != data['turma_id'] for turma in aluno.turmas) # Indica se a turma já estava relacionada com o aluno

    if nova_turma:
        # Verifica se a turma existe
        turma_existente = db.session.get(Turma, data["turma_id"])
=======
    nova_turma = all(turma.id != data['id_turma'] for turma in aluno.turmas) # Indica se a turma já estava relacionada com o aluno

    if nova_turma:
        # Verifica se a turma existe
        turma_existente = db.session.get(Turma, data["id_turma"])
>>>>>>> Stashed changes
        if turma_existente is None:
            return jsonify({"erro": ["Turma não existe"]}), 400
        
        # Verifica se a turma está aberta
<<<<<<< Updated upstream
        turma_fechada = db.session.query(Turma).filter_by(id=data['turma_id']).first()
=======
        turma_fechada = db.session.query(Turma).filter_by(id=data['id_turma']).first()
>>>>>>> Stashed changes
        if turma_fechada is not None and turma_fechada.status == "C":
            return jsonify({"erro": ["A turma está fechada"]}), 400

    if aluno.email != data['email']:
        email_existente = db.session.query(Aluno).filter_by(email= data['email']).first()
        if email_existente:
            return jsonify({"erro": ["E-mail já existe"]}), 400
        
    aluno.nome = data['nome']
    aluno.email = data['email']
    aluno.telefone = data['telefone']
    aluno.endereco = data['endereco']
    aluno.data_de_nascimento = string_para_data(data['data_de_nascimento'])

    # Caso a turma seja nova, adiciona nova turma ao aluno
    if nova_turma:
<<<<<<< Updated upstream
        turma = db.session.get(Turma, data['turma_id'])
=======
        turma = db.session.get(Turma, data['id_turma'])
>>>>>>> Stashed changes
        aluno.turmas.append(turma)

    db.session.commit()

    return jsonify({"mensagem": "Aluno atualizado com sucesso!", "data": {"matricula": aluno.matricula, "nome": aluno.nome, "email": aluno.email, "telefone": aluno.telefone, "endereco": aluno.endereco, "data_de_nascimento": aluno.data_de_nascimento}}), 200


def remover_aluno(matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Remove um aluno existente do banco de dados.

    Args:
        matrícula (str): A matrícula do aluno a ser removido.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso.
    """
    aluno = db.session.query(Aluno).filter_by(matricula=matricula).first()
    
    db.session.delete(aluno)
    db.session.commit()
<<<<<<< Updated upstream
    return jsonify({"mensagem": "Aluno deletado com sucesso!"}), 200
=======
    return jsonify({"mensagem": "Aluno deletado com sucesso!"}), 200
>>>>>>> Stashed changes
