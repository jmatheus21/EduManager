from datetime import date
from .validators_helpers import validar_data
from .date_helpers import string_para_data

"""
Módulo de Validação de Salas.

Este módulo fornece funções para validar os dados de uma entidade.
As validações garantem que os dados estejam dentro dos critérios esperados e retornam uma lista de erros, se houver.
"""


def validar_sala(numero: int, capacidade: int, localizacao: str) -> list:
    """Valida os dados de uma sala.

    Esta função verifica se os dados fornecidos para uma sala estão dentro dos critérios esperados.
    Caso haja erros, eles são retornados em uma lista.

    Args:
        numero (int): O número da sala. Deve ser maior que 0 e menor que 1.000.
        capacidade (int): A capacidade da sala. Deve ser no mínimo 10 e no máximo 500.
        localizacao (str): A localização da sala. Deve ter no mínimo 2 caracteres e no máximo 100.

    Returns:
        list: Uma lista de mensagens de erro, se houver. Caso contrário, retorna uma lista vazia.

    Exemplo:
        >>> erros = validar_sala(101, 30, "Bloco A, 1º Andar")
        >>> print(erros)
        []
    """
    erros = []

    if not numero or not isinstance(numero, int) or numero <= 0 or numero >= 1000:
        erros.append("O atributo 'numero' é obrigatório e deve ser maior que zero e menor que 1.000")

    if not capacidade or not isinstance(capacidade, int) or capacidade < 10 or capacidade > 500:
        erros.append("O atributo 'capacidade' é obrigatório e deve ser no mínimo 10 e no máximo 500")

    if not localizacao or not isinstance(localizacao, str) or len(localizacao) < 2 or len(localizacao) > 100:
        erros.append("O atributo 'localizacao' é obrigatório e deve ter no mínimo 2 letras e no máximo 100")

    return erros


def validar_aluno ():
    pass


def validar_calendario(ano_letivo: int, data_inicio: str, data_fim: str, dias_letivos: int) -> list:
    """Valida os dados de um calendário.

    Esta função verifica se os dados fornecidos para um calendário estão dentro dos critérios esperados.
    Caso haja erros, eles são retornados em uma lista.

    Args:
        ano_letivo (int): O ano letivo referente ao calendário. Deve ser maior ou igual ao ano atual.
        data_inicio (str): A data de início do calendário. Deve ser formato 'YYYY-MM-DD', em que o YYYY representa o ano, MM o mês e DD o dia. Deve ser posterior à data atual e o ano da data deve ser igual ao ano letivo. Além disso, a data de início deve ser anterior à data de fim.
        data_fim (str): A data de fim do calendário. Deve ser formato 'YYYY-MM-DD', em que o YYYY representa o ano, MM o mês e DD o dia. Deve ser posterior à data atual e o ano da data deve ser igual ao ano letivo. Além disso, a data de fim deve ser posterior à data de início.
        dias_letivos (int): A quantidade de dias letivos do calendário. Deve ser entre 50 e 200. 

    Returns:
        list: Uma lista de mensagens de erro, se houver. Caso contrário, retorna uma lista vazia.

    Exemplo:
        >>> erros = validar_calendario(2026, "2026-02-01", "2026-09-01", 125)
        >>> print(erros)
        []
    """
    erros = []

    if not ano_letivo or not isinstance(ano_letivo, int) or ano_letivo < date.today().year:
        erros.append("O atributo 'ano_letivo' é obrigatório e deve ser maior ou igual ao ano atual")

    if not data_inicio or not isinstance(data_inicio, str) or not validar_data(data_inicio):
        erros.append("O atributo 'data_inicio' é obrigatório e deve ter o formato correto")
    else:
        inicio = string_para_data(data_inicio)
        if inicio < date.today() or inicio.year != ano_letivo:
            erros.append("O atributo 'data_inicio' deve ser posterior a data atual e no ano letivo indicado")

    if not data_fim or not isinstance(data_fim, str) or not validar_data(data_fim):
        erros.append("O atributo 'data_fim' é obrigatório e deve ter o formato correto")
    else:
        fim = string_para_data(data_fim)
        if fim < date.today() or fim.year != ano_letivo:
            erros.append("O atributo 'data_fim' deve ser posterior a data atual e no ano letivo indicado.")
 
    if string_para_data(data_fim) < string_para_data(data_inicio):
        erros.append("O atributo 'data_fim' deve ser maior que 'data_inicio'.")
    
    if not dias_letivos or not isinstance(dias_letivos, int) or dias_letivos < 50 or dias_letivos > 200:
        erros.append("O atributo 'dias_letivos' é obrigatório e deve ser entre 50 e 200")

    return erros


def validar_cargo ():
    pass


def validar_disciplina ():
    pass


def validar_turma ():
    pass


def validar_usuario ():
    pass