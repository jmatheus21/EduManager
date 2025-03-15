"""
Módulo de Controlador para Usuários.

Este módulo contém as funções que implementam a lógica de negócio para as operações relacionadas aos usuários.
Ele interage com o modelo `Usuário` para realizar operações CRUD e valida os dados usando o módulo `validators`.
"""

from flask import request, jsonify
from app.extensions import db
from ..models import Usuario, Disciplina, Cargo
from app.utils.validators import validar_usuario
from datetime import datetime
from app.utils.usuario_helpers import gerar_hashing
from app.utils.date_helpers import string_para_data


def cadastrar_usuario() -> jsonify:
    """Cadastra um novo usuário no banco de dados.

    Esta função recebe os dados de um usuário via JSON, valida os dados e, se válidos, cadastra o usuário no banco de dados.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados do usuário cadastrado, ou uma mensagem de erro em caso de dados inválidos.
    """
    data = request.get_json()

    erros = validar_usuario(cpf=data['cpf'], nome=data['nome'], email=data['email'], senha=data['senha'], telefone=data['telefone'], endereco=data['endereco'], horario_de_trabalho=data['horario_de_trabalho'], data_de_nascimento=data['data_de_nascimento'], tipo=data['tipo'], formacao=data['formacao'], escolaridade=data['escolaridade'], habilidades=data['habilidades'], disciplinas=data['disciplinas'], cargos=data['cargos'])
    if erros:
        return jsonify({"erro": erros}), 400
    
    usuario_existente = db.session.get(Usuario, data['cpf'])
    if usuario_existente:
        return jsonify({"erro": ["Usuário já existe"]}), 400

    email_existente = db.session.query(Usuario).filter_by(email= data['email']).first()
    if email_existente:
        return jsonify({"erro": ["E-mail já existe"]}), 400
    
    data['data_de_nascimento'] = string_para_data(data['data_de_nascimento'])
    
    # verificar o tipo, se for professor, verificar disciplinas e colocar os campos que não são do tipo professor como nulo
    if data['tipo'].lower() == 'p':

        data['escolaridade'] = None
        data['habilidades'] = None

        disciplinas_invalidas = []

        for codigo in data['disciplinas']:
            disciplina_existente = db.session.get(Disciplina, codigo)

            if not disciplina_existente:
                disciplinas_invalidas.append(codigo)
            
        if disciplinas_invalidas:
            return jsonify({"erro": [f"Disciplinas inválidas: {', '.join(disciplinas_invalidas)}"]}), 400
    else:
        data['formacao'] = None
        data['disciplinas'] = None  
    
    novo_usuario = Usuario(cpf=data['cpf'], nome=data['nome'], email=data['email'], senha=gerar_hashing(data['senha']), telefone=data['telefone'], endereco=data['endereco'], horario_de_trabalho=data['horario_de_trabalho'], data_de_nascimento=data['data_de_nascimento'], tipo=data['tipo'], formacao=data['formacao'], escolaridade=data['escolaridade'], habilidades=data['habilidades'])
    db.session.add(novo_usuario)
    db.session.commit()

    # adicionando disciplinas ao usuário
    if novo_usuario.tipo == 'p':
        for codigo in data['disciplinas']:
            disciplina = db.session.get(Disciplina, codigo)
            novo_usuario.disciplinas.append(disciplina)

    
    for cargo in data['cargos']:
        cargo['data_contrato'] = string_para_data(cargo['data_contrato'])

        cargo_existente = db.session.query(Cargo).filter_by(nome=cargo['nome'], usuario_cpf=novo_usuario.cpf).first()

        if cargo_existente:
            return jsonify({"erro": ["Usuário não pode ter dois cargos com o mesmo nome"]}), 400
            
        novo_cargo = Cargo(nome = cargo['nome'], salario = cargo['salario'], data_contrato = cargo['data_contrato'], usuario_cpf=novo_usuario.cpf)
        db.session.add(novo_cargo)
        db.session.commit()
    
    return jsonify({"mensagem": "Usuário criado com sucesso!", "data": {"cpf": novo_usuario.cpf, "nome": novo_usuario.nome, "email": novo_usuario.email, "senha": novo_usuario.senha, "telefone": novo_usuario.telefone, "endereco": novo_usuario.endereco, "horario_de_trabalho": novo_usuario.horario_de_trabalho, "data_de_nascimento": novo_usuario.data_de_nascimento, "tipo": novo_usuario.tipo, "formacao": novo_usuario.formacao, "escolaridade": novo_usuario.escolaridade, "habilidades": novo_usuario.habilidades, "disciplinas": [d.codigo for d in novo_usuario.disciplinas], "cargos": [{"nome": c.nome, "salario": c.salario, "data_contrato": c.data_contrato} for c in novo_usuario.cargos]}}), 201


def listar_usuarios() -> jsonify:
    """Lista todas os usuários cadastradas no banco de dados.

    Returns:
        jsonify: Resposta JSON contendo uma lista dos usuários com seus respectivos dados.
    """
    usuarios = Usuario.query.all()
    return jsonify([{"cpf": usuario.cpf, "nome": usuario.nome, "email": usuario.email, "senha": usuario.senha, "telefone": usuario.telefone, "endereco": usuario.endereco, "horario_de_trabalho": usuario.horario_de_trabalho, "data_de_nascimento": usuario.data_de_nascimento, "tipo": usuario.tipo, "formacao": usuario.formacao, "escolaridade": usuario.escolaridade, "habilidades": usuario.habilidades, "disciplinas": [{"codigo": disciplina.codigo, "nome": disciplina.nome} for disciplina in usuario.disciplinas], "cargos": [{"nome": cargo.nome, "salario": cargo.salario, "dataContrato": cargo.data_contrato} for cargo in usuario.cargos]} for usuario in usuarios]), 200


def buscar_usuario(cpf : str):
    """Busca um usuário específico pelo cpf.

    Args:
        cpf (str): O cpf do usuário a ser buscado.

    Returns:
        jsonify: Resposta JSON contendo os dados do usuário encontrado.
    """
    usuario = db.session.get(Usuario, cpf)
    return jsonify({"cpf": usuario.cpf, "nome": usuario.nome, "email": usuario.email, "senha": usuario.senha, "telefone": usuario.telefone, "endereco": usuario.endereco, "horario_de_trabalho": usuario.horario_de_trabalho, "data_de_nascimento": usuario.data_de_nascimento, "tipo": usuario.tipo, "formacao": usuario.formacao, "escolaridade": usuario.escolaridade, "habilidades": usuario.habilidades, "disciplinas": [{"codigo": disciplina.codigo, "nome": disciplina.nome} for disciplina in usuario.disciplinas], "cargos": [{"nome": cargo.nome, "salario": cargo.salario, "dataContrato": cargo.data_contrato} for cargo in usuario.cargos]}), 200