from flask import request, jsonify, make_response
from app.extensions import db
from ..utils.login_helpers import gerar_token
from ..utils.usuario_helpers import checar_senha
from ..models import Usuario
from datetime import timedelta


def login() -> jsonify:

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
        # secure=true        isso aqui só deve ser descomentado se por algum milagre usar HTTPS
        httponly=True,
        samesite="Lax"
    )

    return response

def validate(current_user_cpf: str, current_user_role: str) -> jsonify:
    
    usuario = db.session.query(Usuario).filter_by(cpf=current_user_cpf).first()
    if not usuario:
        return jsonify({ "autenticado": False, "mensagem": "Usuário não existe"}), 401
    
    return jsonify({ "autenticado": True, "usuario": {"nome": usuario.nome, "role": current_user_role } }), 200

def logout() -> jsonify:

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