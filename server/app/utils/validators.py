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


"""
Módulo de Validação de Disciplinas.

Este módulo fornece funções para validar os dados de uma entidade.
As validações garantem que os dados estejam dentro dos critérios esperados e retornam uma lista de erros, se houver.
"""


def validar_disciplina (codigo: str, nome: str, carga_horaria: int, ementa: str, bibliografia: str) -> list:
    """ Valida os dados de uma disciplina.

    Esta função verifica se os dados fornecidos para uma disciplina estão dentro dos critérios esperados.
    Caso haja erros, eles são retornados em uma lista.

    Args:
        codigo (str): O código da disciplina. Deve ter no mínimo 6 caracteres e no máximo 10.
        nome (str): O nome da disciplina. Deve ter no mínimo 3 caracteres e no máximo 50 caracteres.
        carga_horaria (int): A carga horária da disciplina. Deve ser no mínimo 15 e no máximo 120.
        ementa (str): A ementa da disciplina. Deve ter no máximo 255 caracteres. Este argumento pode ser nulo.
        bibliografia (str): A bibliografia da disciplina. Deve ter no máximo 255 caracteres. Este argumento pode ser nulo.
        
    Returns:
        list: Uma lista de mensagens de erro, se houver. Caso contrário, retorna uma lista vazia.

    Exemplo:
        >>> erros = validar_disciplina("MAT001", "Matemática", 30, 
        "Aritmética, Álgebra, Geometria, Estatística e Probabilidade, com foco na compreensão das relações entre esses conceitos.", 
        "STEWART, Ian. Aventuras matemáticas: vacas no labirinto e outros enigmas lógicos. 1. Ed. Rio de Janeiro:"Zahar, 2014.")
        >>> print(erros)
        []
    """
    erros = []

    if not codigo or not isinstance(codigo, str) or len(codigo) < 6 or len(codigo) > 10:
        erros.append("O atributo 'codigo' é obrigatório e deve ter no minimo 6 caracteres e no máximo 10")

    if not nome or not isinstance(nome, str) or len(nome) < 3 or len(nome) > 50:
        erros.append("O atributo 'nome' é obrigatório e deve ter no mínimo 3 caracteres e no máximo 50")

    if not carga_horaria or not isinstance(carga_horaria, int) or carga_horaria < 15 or carga_horaria > 120:
        erros.append("O atributo 'carga_horaria' é obrigatório e deve ser no mínimo 15 e no máximo 120")

    if not isinstance(ementa, str) or len(ementa) < 0 or len(ementa) > 255:
        erros.append("O atributo 'ementa' não é obrigatório e deve ter no máximo 255 caracteres")

    if not isinstance(bibliografia, str) or len(bibliografia) < 0 or len(bibliografia) > 255:
        erros.append("O atributo 'bibliografia' não é obrigatório e deve ter no máximo 255 caracteres")

    return erros


def validar_turma ():
    pass


def validar_usuario ():
    pass