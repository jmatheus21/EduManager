import re
from datetime import datetime, timedelta

def validar_telefone(telefone: str) -> bool:
    """
    Valida se o telefone está no formato correto: "DD 9 XXXX-XXXX".

    Args:
        telefone (str): O telefone a ser validado, no formato "DD 9 XXXX-XXXX".

    Returns:
        bool: True se o telefone estiver no formato correto, False caso contrário.
    """
    padrao = r"^(\d{2}) 9 \d{4}-\d{4}$"
    return bool(re.match(padrao, telefone))


def validar_data_de_nascimento(data_de_nascimento: str) -> bool:
    """
    Valida se a data de nascimento está no formato "YYYY-MM-DD" e se o ano de nascimento 
    está dentro do intervalo permitido, definido dinamicamente como:
      - Ano mínimo: (ano atual - 100)
      - Ano máximo: (ano atual - 15)

    Observações:
      - A data deve representar uma data válida.
      - A função retorna True se o formato estiver correto e o ano estiver dentro do intervalo permitido; 
        caso contrário, retorna False.

    Args:
        data_de_nascimento (str): A data de nascimento a ser validada.

    Returns:
        bool: True se a data estiver no formato correto e dentro do intervalo permitido, 
              False caso contrário.
    """
    padrao = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(padrao, data_de_nascimento):
        return False  # Formato inválido

    try:
        ano_de_nascimento = int(data_de_nascimento[:4])
        ano_atual = datetime.now().year
        
        ano_minimo = ano_atual - 100
        ano_maximo = ano_atual - 15  # Ano atual - 15 anos
        
        if not (ano_minimo <= ano_de_nascimento <= ano_maximo):
            return False  # Ano fora do intervalo permitido
        
        return True
    except ValueError:
        return False  # Data inválida (ex: 32-01-2020)


def validar_data_contrato (data_contrato: str) -> bool:
    """
    Valida se a data do contrato está no formato "YYYY-MM-DD" e se representa uma data futura.

    A data é considerada futura se for posterior à data e hora atuais.

    Args:
        data_contrato (str): A data do contrato no formato "YYYY-MM-DD".

    Returns:
        bool: True se a data estiver no formato correto e for uma data futura, 
              False caso contrário.
    """
    padrao = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(padrao, data_contrato):
        return False  # Formato inválido
    
    try:
        # Tenta converter a string para um objeto datetime
        data_contrato_dt = datetime.strptime(data_contrato, "%Y-%m-%d")
    except ValueError:
        # Se ocorrer um ValueError, a data está em um formato inválido
        return False
    
    # Obtém a data e hora atuais
    data_atual = datetime.now()
    
    # Calcula a diferença entre a data do contrato e a data atual
    diferenca = data_contrato_dt - data_atual
    
    # Verifica se a data do contrato é futura
    return diferenca > timedelta(days=0)

import re

import re

def validar_horario_trabalho(horario: str) -> bool:
    """
    Valida o formato do horário de trabalho onde:
    - Dias: primeira letra maiúscula, outras minúsculas
    - Horas: qualquer valor válido entre 00h e 23h
    - Exemplo: "Seg-Sex, 08h-20h"
    """
    
    dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab"]
    for d in dias:
        if horario[:3] == d:
            break
        if horario[4:7] == d:
            return False

    if not horario[:3] in dias or not horario[4:7] in dias:
        return False

    padrao = r"^[A-Z][a-z]{2}-[A-Z][a-z]{2},([01]\d|2[0-3])h-([01]\d|2[0-3])h$"
    return bool(re.match(padrao, horario))


def validar_horario_completo(horario: str) -> bool:
    """
    Valida a lógica do horário de trabalho.

    Realiza a verificação:
    1. Validação se o horário final é maior que o horário inicial

    Args:
        horario (str): String no formato "DiaSemana-DiaSemana,HHh-HHh"
                       Exemplo: "Seg-Sex,08h-17h"

    Returns:
        bool: True a validação foi bem sucedida, False caso contrário

    Observações:
        - Considera apenas horas inteiras (sem minutos)
        - Horário final deve ser necessariamente posterior ao horário inicial
    """
        
    # Extrai horas inicial e final
    horas = re.findall(r"\d{2}", horario)
    h_inicio = int(horas[0])
    h_fim = int(horas[1])
    
    return h_fim > h_inicio



