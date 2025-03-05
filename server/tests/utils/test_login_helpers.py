"""
Este módulo contém testes para as funções de autenticação JWT implementadas no módulo `login_helpers`.

Os testes verificam a geração e validação de tokens JWT para autenticação de usuários.
"""

from app.utils.login_helpers import gerar_token, validar_token
from app import create_app


def test_login_helpers():
    """Testa as funções `gerar_token` e `validar_token` do módulo `login_helpers`.

    Este teste verifica se:
    1. Um token JWT pode ser gerado corretamente para um CPF fornecido.
    2. O token gerado pode ser validado corretamente.
    3. O CPF extraído do token corresponde ao CPF original.

    Cenário Testado:
        1. Geração de um token JWT para o CPF "000.000.000-00".
        2. Validação do token gerado para extrair o CPF.
        3. Verificação de que o CPF extraído é igual ao CPF original.

    Dependências:
        - A aplicação Flask deve ser configurada com um contexto de aplicação (`app.app_context()`).
        - A chave secreta da aplicação (`SECRET_KEY`) deve estar definida para assinar e verificar o token.

    Resultados Esperados:
        - O token gerado não deve ser nulo.
        - O CPF extraído do token deve ser igual ao CPF fornecido na geração.

    Args:
        Nenhum (este é um teste autossuficiente).
    """
    app = create_app()

    with app.app_context():
        # CPF de teste
        cpf_original = "000.000.000-00"

        # Usando gerar_token
        token = gerar_token(cpf_original)

        # Testando o gerar_token
        assert token is not None

        # Usando o validar_token
        cpf = validar_token(token)

        # Testando o validar_token
        assert cpf == cpf_original