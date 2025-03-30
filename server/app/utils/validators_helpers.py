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


def validar_hora(hora: str) -> bool:
    """Valida se uma string está no formato de hora 'HH:MM'. 

    Esta função utiliza uma expressão regular para verificar se a string fornecida
    segue o formato de data ISO 8601 (horas:minutos). O formato esperado é:

    HH:MM:SS (exemplo: "06:30")

    Critérios de validação:
    - Deve conter exatamente 2 dígitos para as horas.
    - Deve conter exatamente 2 dígitos para os minutos.
    - Deve seguir o padrão com dois-pontos separando os elementos (HH:MM).
    - A string não pode conter caracteres adicionais antes ou depois da hora.

    Args:
        hora (str): A string representando a hora a ser validada.

    Returns:
        bool: Retorna `True` se a string corresponder ao formato HH:MM, 
              caso contrário, retorna `False`."
    """
    padrao = r"^\d{2}:\d{2}$"  # Corrigido para validar a string com o formato correto
    if not re.match(padrao, hora):  # Verifica se a string segue o padrão "HH:MM"
        return False

    padrao_hora = int(hora[:2])  # Converte para inteiro as horas
    padrao_minuto = int(hora[3:])  # Converte para inteiro os minutos

    # Verifica se as horas estão entre 00 e 23 e minutos entre 00 e 59
    if 0 <= padrao_hora <= 23 and 0 <= padrao_minuto <= 59:
        return True
    else:
        return False


def validar_dia_da_semana(dia_da_semana: str) -> bool:
    """Valida se uma string é um dia da semana. 

    Esta função erifica se a string fornecida trata-se de um dia da semana.
    Podendo ser: Segunda, Terça, Quarta, Quinta, Sexta e Sábado

    Critérios de validação:
    - Deve conter no mínimo 5 dígitos caracteres.
    - Deve conter no máximo 7 dígitos caracteres. 
    - Deve seguir um dos padrões estabelecidos.
    - A string não pode conter caracteres adicionais antes ou depois do dia da semana.

    Args:
        dia_da_semana (str): A string representando o dia da semana a ser validado.

    Returns:
        bool: Retorna `True` se a string corresponder a um dos padrões estabelecidos, 
              caso contrário, retorna `False`."
    """
    dias_validos = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]

    for dia in dia_da_semana:
        if dia not in dias_validos:
            return False
    return True


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
    
def validar_data_de_nascimento_aluno(data_de_nascimento: str) -> bool:
    """
    Valida se a data de nascimento está no formato "YYYY-MM-DD" e se o ano de nascimento 
    está dentro do intervalo permitido, definido dinamicamente como:
      - Ano mínimo: (ano atual - 100)
      - Ano máximo: (ano atual - 6)

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
        data_nascimento = datetime.strptime(data_de_nascimento, "%Y-%m-%d")  # Validação da data
        ano_de_nascimento = data_nascimento.year
        ano_atual = datetime.now().year

        ano_minimo = ano_atual - 100
        ano_maximo = ano_atual - 6  

        return ano_minimo <= ano_de_nascimento <= ano_maximo
    except ValueError:
        return False  


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

def validar_matricula(matricula: str) -> bool:
    """
    Valida se a matrícula está no formato correto: "XXXX000XXXXX".

    Args:
        matricula (str): A matrícula a ser validada, no formato "XXXX000XXXXX".

    Returns:
        bool: True se a matrícula estiver no formato correto, False caso contrário.
    """
    padrao = r'^\d{4}000\d{5}$'
    return bool(re.match(padrao, matricula))

