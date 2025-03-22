from datetime import datetime


def hora_para_string(hora: datetime.time) -> str:
    """Converte um objeto date para uma string no formato 'HH:MM:SS'.

    Args:
        hora (datetime.time): Objeto time a ser convertido.

    Returns:
        str: Hora no formato 'HH:MM:SS'.
    """
    return hora.strftime('%H:%M:%S')


def string_para_hora(hora_str: str) -> datetime.time:
    """Converte uma string no formato 'HH:MM:SS' para um objeto hour.

    Args:
        hora_str (str): Hora no formato 'HH:MM:SS'.

    Returns:
        datetime.date: Objeto date correspondente à hora fornecida.
    """

    return datetime.strptime(hora_str, "%H:%M:%S").time()