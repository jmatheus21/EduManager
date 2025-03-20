from app.utils.login_helpers import gerar_token

def usuario_entra_no_sistema (client, app):
    with app.app_context():
        token = gerar_token(usuario_cpf="12345678910", usuario_tipo="f")
        client.set_cookie("auth_token", token, domain="localhost")