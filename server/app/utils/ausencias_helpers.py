def calcular_intervalo(hora_inicio: str, hora_fim: str) -> float:
    """
    Calcula quantas horas se passaram dado um intervalo de tempo.

    Args:
        hora_inicio (str): String no formato "HH:MM"
        hora_fim (str): String no formato "HH:MM"
                       Exemplo: "16:30"

    Returns:
        float: O número de horas passadas no intervalo de tempo dado.

    Observações:
        - Horário final deve ser necessariamente posterior ao horário inicial
    """
    inicio_horas = int(hora_inicio[:2])
    fim_horas = int(hora_fim[:2])
    
    fim_minutos = int(hora_fim[3:5])
    inicio_minutos = int(hora_inicio[3:5])

    intervalo_total = (fim_horas*60 + fim_minutos) - (inicio_horas*60 + inicio_minutos)
    
    return intervalo_total / 60