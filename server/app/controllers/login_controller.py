"""
Módulo de Controlador para Login.

Este módulo contém as funções que implementam a lógica de negócio para as operações relacionadas às login.
"""

from flask import request, jsonify, make_response
from app.extensions import db
from ..utils.login_helpers import gerar_token
from ..utils.usuario_helpers import checar_senha
from ..models import Usuario
from datetime import timedelta


def login() -> jsonify:
    """Realiza o login de um usuário.

    Esta função recebe os dados de um usuário via JSON, valida os dados e, se válidos, realiza o login do usuário no sistema.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso, ou uma mensagem de erro em caso de dados inválidos.
    """
    data = request.get_json()

    usuario = db.session.query(Usuario).filter(Usuario.email == data['email']).first()
    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    
    if not checar_senha(data['senha'], usuario.senha):
        return jsonify({"erro": "Senha incorreta"}), 401
    
    token = gerar_token(usuario.cpf, usuario.tipo)

    response = make_response(jsonify({"mensagem": "Login realizado"}))
    response.set_cookie(
        key="auth_token",
        value=token,
        max_age=timedelta(hours=6),
        # secure=true        Isso aqui só deve ser descomentado se usar HTTPS
        httponly=True,
        samesite="Lax"
    )

    return response


def validate(current_user_cpf: str, current_user_role: str) -> jsonify:
    """Valida o login do usuário no sistema.

    Esta função recebe os dados de um usuário via banco de dados, valida os dados e, se válidos, valida a entrada do usuário no sistema.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso, ou uma mensagem de erro em caso de dados inválidos.
    """
    usuario = db.session.query(Usuario).filter_by(cpf=current_user_cpf).first()
    if not usuario:
        return jsonify({ "autenticado": False, "mensagem": "Usuário não existe"}), 401
    
    return jsonify({ "autenticado": True, "usuario": {"nome": usuario.nome, "role": current_user_role } }), 200


def logout() -> jsonify:
    """Realiza o logout de um usuário.

    Esta função recebe os dados de um usuário via JSON, valida os dados e, se válidos, realiza o logout do usuário no sistema.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso, ou uma mensagem de erro em caso de dados inválidos.
    """
    response = make_response(jsonify({"mensagem": "Logout bem-sucedido"}))
    response.set_cookie(
        key="auth_token",
        value="", 
        expires=0, 
        httponly=True,
        # secure=True,
        samesite="Lax"
    )

    return response