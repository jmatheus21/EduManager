from datetime import datetime

def data_para_string(data: datetime.date) -> str:
    """
    Converte um objeto date para uma string no formato 'YYYY-MM-DD'.

    Args:
        data (datetime.date): Objeto date a ser convertido.

    Returns:
        str: Data no formato 'YYYY-MM-DD'.
    """
    return data.strftime('%Y-%m-%d')


def string_para_data(data_str: str) -> datetime.date:
    """
    Converte uma string no formato 'YYYY-MM-DD' para um objeto date.

    Args:
        data_str (str): Data no formato 'YYYY-MM-DD'.

    Returns:
        datetime.date: Objeto date correspondente à data fornecida.
    """
    return datetime.strptime(data_str, '%Y-%m-%d').date()

