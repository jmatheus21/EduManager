from datetime import datetime


def hora_para_string(data: datetime.time) -> str:
    """Converte um objeto date para uma string no formato 'HH:MM'.

    Args:
        data (datetime.time): Objeto time a ser convertido.

    Returns:
        str: Hora no formato 'HH:MM'.
    """
    return data.strftime('%H:%M')


def string_para_hora(hora_str: str) -> datetime.time:
    """Converte uma string no formato 'HH:MM' para um objeto hour.

    Args:
        data_str (str): Data no formato 'HH:MM'.

    Returns:
        datetime.date: Objeto date correspondente à hora fornecida.
    """

    return datetime.strptime(hora_str, "%H:%M").time