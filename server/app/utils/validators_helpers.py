import re

def validar_data(data : str) -> bool:
    """Valida se uma string está no formato de data 'YYYY-MM-DD'.

    Esta função utiliza uma expressão regular para verificar se a string fornecida
    segue o formato de data ISO 8601 (ano-mês-dia). O formato esperado é:

        YYYY-MM-DD (exemplo: "2024-03-08")

    Critérios de validação:
    - Deve conter exatamente 4 dígitos para o ano.
    - Deve conter exatamente 2 dígitos para o mês 
    - Deve conter exatamente 2 dígitos para o dia 
    - Deve seguir o padrão com hífens separando os elementos (YYYY-MM-DD).
    - A string não pode conter caracteres adicionais antes ou depois da data.

    Args:
        data (str): A string representando a data a ser validada.

    Returns:
        bool: Retorna `True` se a string corresponder ao formato YYYY-MM-DD, 
              caso contrário, retorna `False`."
    """
    padrao = r"\d{4}-\d{2}-\d{2}$"
    return bool(re.match(padrao, data))