from datetime import date
from .validators_helpers import validar_data_contrato, validar_telefone, validar_data, validar_data_de_nascimento, validar_data_de_nascimento_aluno, validar_horario_completo, validar_horario_trabalho
from .date_helpers import string_para_data
from .disciplina_helpers import validar_codigo


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


"""
Módulo de Validação de Alunos.

Este módulo fornece funções para validar os dados de uma entidade.
As validações garantem que os dados estejam dentro dos critérios esperados e retornam uma lista de erros, se houver.
"""


def validar_aluno(matricula: str, nome: str, email: str, telefone: str, endereco: str, data_de_nascimento: str):
    """Valida os dados de um aluno.

    Esta função verifica se os dados fornecidos para uma aluno estão dentro dos critérios esperados.
    Caso haja erros, eles são retornados em uma lista.

    Args:
        matricula (str): A matrícula do aluno. Deve ter no mínimo 12 e máximo 50 caracteres.
        nome (str): O nome do aluno. Deve ser no mínimo 3 e no máximo 100.
        email (str): O email do aluno. Deve ter entre 3 e 100 caracteres, além disso, deve ter um caractere '@'.
        telefone (str): O telefone do aluno. Deve ser fornecido no formato "DD 9 XXXX-XXXX", onde X é um caractere númerico inteiro.
        endereco (strr): O endereço do aluno. Deve ter no mínimo 10 caracteres e no máximo 255 caracteres.
        data_de_nascimento: A data de nascimento do aluno. Deve seguir o formato 'YYYY-MM-DD', em que YYYY representa o ano, MM o mês e DD o dia. Além disso, deve ser uma data válida e o aluno deve ter entre 6 e 100 anos.

    Returns:
        list: Uma lista de mensagens de erro, se houver. Caso contrário, retorna uma lista vazia.

    Exemplo:
        >>> erros = validar_aluno("202600000001", "João Pedro dos Santos", "joaopedro@email.com", "79 9 1234-5678", "Bairro X, Rua A", "2011-09-10")
        >>> print(erros)
        []
    """
    erros = []

    if not matricula or not isinstance(matricula, str) or len(matricula) < 12 or len(matricula) > 15:
        erros.append("O atributo 'matrícula' é obrigatório e deve ter no mínimo 12 caracteres e no máximo 15 caracteres")
        
    if not nome or not isinstance(nome, str) or len(nome) < 3 or len(nome) > 100:
        erros.append("O atributo 'nome' é obrigatório e deve ter no mínimo 3 caracteres e no máximo 100 caracteres")
    
    if not email or not isinstance(email, str) or len(email) < 3 or len(email) > 100 or ('@' not in email):
        erros.append("O atributo 'email' é obrigatório e deve ter no mínimo 3 caracteres e no máximo 100 caracteres, além de precisar ter o @")

    if not telefone or not isinstance(telefone, str) or not validar_telefone(telefone):
        erros.append("O atributo 'telefone' é obrigatório e não segue o formato estabelecido 'XX 9 XXXX-XXXX'")

    if not endereco or not isinstance(endereco, str) or len(endereco) < 10 or len(endereco) > 100:
        erros.append("O atributo 'endereço' é obrigatório e deve ter no mínimo 10 letras e no máximo 255 caracteres")

    if not data_de_nascimento or not isinstance(data_de_nascimento, str) or not validar_data_de_nascimento_aluno(data_de_nascimento):
        erros.append("O atributo 'data_de_nascimento' é obrigatório, deve ser uma data válida e o aluno deve ter entre 6 e 100 anos")

    return erros


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


def validar_cargo (nome : str, salario : float, data_contrato : str) -> list:
    """Valida os dados de um cargo.

    Esta função verifica se os dados fornecidos para um cargo estão dentro dos critérios esperados.
    Caso haja erros, eles são retornados em uma lista

    Args:
        nome (str): O nome do cargo. Deve ter no mínimo 5 caracteres e no máximo 100 caracteres.
        salario (float): O salário recebido. Deve ser entre R$ 100 e R$ 999.999.999,0.
        data_contrato (str): A data final de contrato. Deve seguir o formato 'YYYY-MM-DD', em que YYYY representa o ano, MM o mês e DD o dia. Além de ser uma data futura.

    Returns:
        list: Uma lista de mensagens de erro, se houver. Caso contrário, retorna uma lista vazia.

      Exemplo:
        >>> erros = validar_cargo("Zelador", 1200.00, "2027-12-11")
        >>> print(erros)
        []
    """
    erros = []

    if not nome or not isinstance(nome, str) or len(nome) < 5 or len(nome) > 100:
        erros.append("O atributo 'nome' é obrigatório e deve ter no mínimo 5 caracteres e no máximo 100 caracteres")

    try:
        salario = float(salario)  # Tenta converter para float
    except ValueError:
        erros.append("O atributo 'salario' deve ser um número válido.")

    if not salario or not (100 <= salario <= 999999999):
        erros.append("O atributo 'salario' é obrigatório e deve ser entre R$100,00 e R$999.999.999,00")

    if not data_contrato or not isinstance(data_contrato, str) or not validar_data_contrato(data_contrato):
        erros.append("O atributo 'data_contrato' é obrigatório e precisa ser uma data futura")

    return erros


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

    if not codigo or not isinstance(codigo, str) or len(codigo) < 6 or len(codigo) > 10 or not validar_codigo(codigo):
        erros.append("O atributo 'codigo' é obrigatório e deve ter no minimo 6 caracteres e no máximo 10. Além do formato ser composto por três letras maiúsculas seguidas de três números (ex: MAT123)")

    if not nome or not isinstance(nome, str) or len(nome) < 3 or len(nome) > 50:
        erros.append("O atributo 'nome' é obrigatório e deve ter no mínimo 3 caracteres e no máximo 50")

    if not carga_horaria or not isinstance(carga_horaria, int) or carga_horaria < 15 or carga_horaria > 120:
        erros.append("O atributo 'carga_horaria' é obrigatório e deve ser no mínimo 15 e no máximo 120")

    if not isinstance(ementa, str) or len(ementa) < 0 or len(ementa) > 255:
        erros.append("O atributo 'ementa' não é obrigatório e deve ter no máximo 255 caracteres")

    if not isinstance(bibliografia, str) or len(bibliografia) < 0 or len(bibliografia) > 255:
        erros.append("O atributo 'bibliografia' não é obrigatório e deve ter no máximo 255 caracteres")

    return erros


def validar_turma (ano: int, serie: str, nivel_de_ensino: str, turno: str, status: str, sala_numero: int, calendario_ano_letivo: int):
    """Valida os dados de uma turma.

    Esta função verifica se os dados fornecidos para uma turma estão dentro dos critérios esperados.
    Caso haja erros, eles são retornados em uma lista.

    Args:
        ano (int): O ano da disciplina. Deve ser no mínimo 1 e no máximo 9.
        serie (str): A série da disciplina. Deve ser representado por um único carácter.
        nivel_de_ensino (str): O nível de ensino. Deve ter no mínimo 2 caracteres e no máximo 30 caracteres.
        turno (str): O turno em que a turma será lecionada. Deve ser representado por um único carácter.
        status (str): O status da turma. Deve ser representado por um único carácter.
        sala_numero(int): O número da sala de aula. Deve ser maior que 0 e menor que 1.000.
        calendario_ano_letivo(int): O ano letivo do calendário da turma. Deve ser maior ou igual ao ano atual.
    Returns:
        list: Uma lista de mensagens de erro, se houver. Caso contrário, retorna uma lista vazia.

    Exemplo:
        >>> erros = validar_turma(9, A, "Ensino Fundamental", D, A, 101, 2026)
        >>> print(erros)
        []
    """
    erros = []

    if not ano or not isinstance(ano, int) or ano < 1 or ano > 9:
        erros.append("O atributo 'ano' é obrigatório e deve ser no mínimo 1 e no máximo 9")

    if not serie or not isinstance(serie, str) or len(serie) != 1:
        erros.append("O atributo 'serie' é obrigatório e deve ter apenas 1 caractere")

    if not nivel_de_ensino or not isinstance(nivel_de_ensino, str) or len(nivel_de_ensino) < 2 or len(nivel_de_ensino) > 30:
        erros.append("O atributo 'nivel_de_ensino' é obrigatório e deve ter no mínimo 2 caracteres máximo 30")
    
    if not nivel_de_ensino in ["Ensino Fundamental", "Ensino Médio"]:
        erros.append("O atributo 'nivel_de_ensino' não tem um valor válido")

    if not turno or not isinstance(turno, str) or len(turno) != 1:
        erros.append("O atributo 'turno' é obrigatório e deve ter apenas 1 caractere")
    
    if not turno in ["M", "V", "N"]:
        erros.append("O atributo 'turno' não tem um valor válido")

    if not status or not isinstance(status, str) or len(status) != 1:
        erros.append("O atributo 'status' é obrigatório e deve ter apenas 1 caractere")
    
    if not status in ["A", "C"]:
        erros.append("O atributo 'status' não tem um valor válido")

    if not isinstance(sala_numero, int) or sala_numero < 0 or sala_numero > 1000:
        erros.append("O atributo 'sala_numero' deve ser no maior que 0 e menor que 1000")

    if not calendario_ano_letivo or not isinstance(calendario_ano_letivo, int) or calendario_ano_letivo < date.today().year:
        erros.append("O atributo 'calendario_ano_letivo' é obrigatório e deve ser maior ou igual ao ano atual")

    return erros


def validar_usuario (cpf : str, nome : str, email : str, senha : str, telefone : str, endereco : str, horario_de_trabalho : str, data_de_nascimento: str, tipo : str, formacao : str, escolaridade : str, habilidades : str, disciplinas : list, cargos : list, new_user : bool = True) -> list:
    """Valida os dados de um usuário.

    Esta função verifica se os dados fornecidos para um usuário estão dentro dos critérios esperados.
    Caso haja erros, eles são retornados em uma lista.

    Args:
        cpf (str): O CPF do usuário. Deve ter obrigatoriamente 11 caracteres.
        nome (str): O nome do usuário. Deve ter entre 3 e 100 caracteres.
        email (str): O email do usuário. Deve ter entre 3 e 100 caracteres, além disso, deve ter um caractere '@'.
        senha (str): A senha do usuário. Deve ter entre 5 e 100 caracteres
        telefone (str): O telefone do usuário. Deve ser fornecido no formato "DD 9 XXXX-XXXX", onde X é um caractere númerico inteiro.
        endereco (str): O endereço do usuário. Deve ter no mínimo 10 caracteres e no máximo 255 caracteres.
        horario_de_trabalho (str): O horário de trabalho do usuário. Deve ter no mínimo 5 caracteres e no máximo 20 caracteres.
        data_de_nascimento (str): A data de nascimento do usuário. Deve seguir o formato 'YYYY-MM-DD', em que YYYY representa o ano, MM o mês e DD o dia. Além disso, deve ser uma data válida e o usuário deve ter entre 15 e 100 anos.
        tipo (char): O tipo de usuário. Deve ser 'f' ou 'p' (funcionário ou professor).
        formacao (str): A formação do usuário. Deve ter no mínimo 10 caracteres e no máximo 255 caracteres.
        escolaridade (str): O grau de escolaridade do usuário. Deve ter no mínimo 5 caracteres e no máximo 255 caracteres.
        habilidades (str): As habilidades do usuário. Deve ter no mínimo 10 caracteres e no máximo 255 caracteres.
        disciplinas (list): A lista de códigos das disciplinas que o usuário do tipo professor pode ministrar. Cada elemento deve ser do tipo 'string' e ter entre 6 caracteres e 10 caracteres.
        cargos (list): A lista dos cargos do usuário. Cada elemento deve ser validado no validar cargos.

    Returns:
        list: Uma lista de mensagens de erro, se houver. Caso contrário, retorna uma lista vazia.

      Exemplo:
        >>> erros = validar_usuario("12345678912", "Alan Ferreira dos Santos", "alanferreira@terra.com", "bocaAberta123", "79 9 9999-8888", "Bairro X, Rua A", "Seg-Sex,7h-12h", "1998-05-17", "p", None, "Licenciatura em Matemática", ["MAT123", "FIS789"], [2])
        >>> print(erros)
        []
    """
    erros = []

    if not cpf or not isinstance(cpf, str) or len(cpf) != 11:
        erros.append("O atributo 'cpf' é obrigatório e deve ter obrigatoriamente 11 caracteres")

    if not nome or not isinstance(nome, str) or len(nome) < 3 or len(nome) > 100:
        erros.append("O atributo 'nome' é obrigatório e deve ter no mínimo 3 caracteres e no máximo 100 caracteres")

    if not email or not isinstance(email, str) or len(email) < 3 or len(email) > 100 or ('@' not in email):
        erros.append("O atributo 'email' é obrigatório e deve ter no mínimo 3 caracteres e no máximo 100 caracteres, além de precisar ter o @")

    if new_user and (not senha or not isinstance(senha, str) or len(senha) < 5 or len(senha) > 100):
        erros.append("O atributo 'senha' é obrigatório e deve ter no mínimo 5 caracteres e no máximo 100 caracteres")

    if not telefone or not isinstance(telefone, str) or not validar_telefone(telefone):
        erros.append("O atributo 'telefone' é obrigatório e não segue o formato estabelecido 'XX 9 XXXX-XXXX'")
    
    if not endereco or not isinstance(endereco, str) or len(endereco) < 10 or len(endereco) > 255:
        erros.append("O atributo 'endereco' é obrigatório e deve ter no mínimo 10 caracteres e no máximo 255 caracteres")

    if not horario_de_trabalho or not isinstance(horario_de_trabalho, str) or len(horario_de_trabalho) < 5 or len(horario_de_trabalho) > 20 or not validar_horario_completo(horario_de_trabalho):
        erros.append("O atributo 'horario_de_trabalho' é obrigatório e deve ter no mínimo 10 caracteres e no máximo 20 caracteres")
    elif not validar_horario_trabalho(horario_de_trabalho):
        erros.append("O atributo 'horario de trabalho' precisa estar no formato AAA-AAA,HHh-HHh, em que AAA é a abreviação de 3 letras maiúsculas para dias (ex: Seg, Sex) e HH representa as horas")
    elif not validar_horario_completo(horario_de_trabalho):
        erros.append("No atributo 'horario_de_trabalho', a hora início deve ser anterior a hora final.")
    
    if not data_de_nascimento or not isinstance(data_de_nascimento, str) or not validar_data_de_nascimento(data_de_nascimento):
        erros.append("O atributo 'data_de_nascimento' é obrigatório, deve ser uma data válida e o usuário deve ter entre 15 e 100 anos")

    if not tipo or not isinstance(tipo, str) or (tipo not in ['f', 'p']):
        erros.append("O atributo 'tipo' é obrigatório e deve ser 'f' ou 'p'")

    if tipo == "p":
        if not isinstance(formacao, str) or len(formacao) < 10 or len(formacao) > 255:
            erros.append("O atributo 'formacao' deve ter no mínimo 10 caracteres e no máximo 255 caracteres")
        
        if not isinstance(disciplinas, list) or not all(isinstance(d, str) and 6 <= len(d) <= 10 for d in disciplinas):
            erros.append("Cada código de disciplina deve ser do tipo 'string' e ter entre 6 caracteres e 10 caracteres")
    
    if tipo == "f":
        if not isinstance(escolaridade, str) or len(escolaridade) < 5 or len(escolaridade) > 255:
            erros.append("O atributo 'escolaridade' deve ter no mínimo 10 caracteres e no máximo 255 caracteres")

        if not isinstance(habilidades, str) or len(habilidades) < 10 or len(habilidades) > 255:
            erros.append("O atributo 'habilidades' deve ter no mínimo 10 caracteres e no máximo 255 caracteres")
    
    erros_cargos = []
    if isinstance(cargos, list):
        for c in cargos:
            if isinstance(c, dict) and 'nome' in c and 'salario' in c and 'data_contrato' in c:
                erros_cargos.extend(validar_cargo(c['nome'], c['salario'], c['data_contrato']))
            else:
                erros_cargos.append("Cada item de 'cargos' deve ser um dicionário com as chaves 'nome', 'salario' e 'data_contrato'")
    else:
        erros_cargos.append("O atributo 'cargos' deve ser uma lista de dicionários")

    if erros_cargos:
        erros.extend(erros_cargos)

    return erros




