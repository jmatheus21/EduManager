from flask import Blueprint, jsonify
from ..controllers import login_controller
from ..middlewares.token_middleware import token_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=['POST'])
def login () -> jsonify:
    return login_controller.login()

@auth_bp.route("/validate", methods=['GET'])
@token_required
def validate (current_user_cpf: str, current_user_role: str) -> jsonify:
    return login_controller.validate(current_user_cpf, current_user_role)

@auth_bp.route("/logout", methods=['GET'])
def logout () -> jsonify:
    return login_controller.logout()