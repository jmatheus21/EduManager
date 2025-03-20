from functools import wraps
from flask import request, jsonify
from ..utils.login_helpers import validar_token
import jwt
from flask import current_app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "auth_token" in request.cookies:
            token = request.cookies.get("auth_token")

        if not token:
            return jsonify({"erro": "Token de autenticação ausente"}), 401

        try:
            payload = validar_token(token)

            current_user_cpf = payload["usuario_cpf"]
            current_user_role = payload["role"]

            kwargs["current_user_cpf"] = current_user_cpf
            kwargs["current_user_role"] = current_user_role
        
        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido"}), 401

        return f(*args, **kwargs)

    return decorated