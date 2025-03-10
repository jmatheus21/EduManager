import re

def validar_codigo(codigo: str) -> bool:
    """
    Valida se o código da disciplina está no formato correto: três letras maiúsculas seguidas de três números (ex: MAT123).

    Args:
        codigo (str): O código da disciplina a ser validado.

    Returns:
        bool: True se o código da disciplina estiver no formato correto, False caso contrário.
    """
    padrao = r"^[A-Z]{3}\d{3}$"
    return bool(re.match(padrao, codigo))