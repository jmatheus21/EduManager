"""
Módulo de autenticação JWT.

Este módulo fornece funções para gerar e validar tokens JWT (JSON Web Tokens) usados para autenticação de usuários na aplicação.
"""

import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app


def gerar_token(usuario_cpf: str, usuario_tipo: str) -> str:
    """Gera um token JWT para autenticação de um usuário.

    O token gerado contém o CPF do usuário e uma data de expiração (6 hora a partir da geração).

    Args:
        usuario_cpf (str): O CPF do usuário que será incluído no token.
        usuario_tipo (str): O tipo do usuário (Funcionário ou Professor)

    Returns:
        str: O token JWT gerado, codificado como uma string.

    Exemplo:
        >>> token = gerar_token("000.000.000-00")
        >>> print(token)
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    """
    payload = {
        "usuario_cpf": usuario_cpf,
        "role": usuario_tipo,
        "exp": datetime.now(timezone.utc) + timedelta(hours=6)
    }

    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def validar_token(token: str | bytes) -> str | None:
    """Valida um token JWT e retorna o CPF do usuário associado.

    Se o token for inválido ou expirado, a função retorna `None`.

    Args:
        token (str | bytes): O token JWT a ser validado.

    Returns:
        str | None: O CPF do usuário associado ao token, ou `None` se o token for inválido ou expirado.

    Exemplo:
        >>> cpf = validar_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        >>> print(cpf)
        "000.000.000-00"
    """
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None