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


def validar_calendario ():
    pass


def validar_cargo ():
    pass


def validar_disciplina ():
    pass


def validar_turma ():
    pass


def validar_usuario ():
    pass