"""
Módulo de Controlador para Ausências. 

Este módulo contém as funções que implementam a lógica de negócio para as operações relacionadas às ausências.
"""

from flask import request, jsonify
from app.extensions import db
from ..models import Boletim, Aula, Aluno, Turma, Disciplina
from app.utils.validators import validar_ausencias_registradas, validar_ausencias_alteradas
from app.utils.ausencias_helpers import calcular_intervalo
from app.utils.hour_helpers import hora_para_string


def registrar_ausencias(aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Registra ausências no banco de dados.

    Esta função recebe os dados de vários alunos, disciplina e turma via JSON, valida os dados e, se válidos, registra as ausências no banco de dados.

    Args: 
        aula_id (int): Id da aula.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados da ausência registrada, ou uma mensagem de erro em caso de dados inválidos.
    """
    data = request.get_json()

    # validar json
    erros = validar_ausencias_registradas(alunos=data['alunos'])
    if erros:
        return jsonify({"erro": erros}), 400

    # verificar existência de aula
    aula = db.session.get(Aula, aula_id)
    if aula is None:
        return jsonify({"erro": ["Aula não existe"]}), 400

    #Verificar existência de disciplina
    disciplina = db.session.get(Disciplina, aula.disciplina_codigo)
    if disciplina is None:
        return jsonify({"erro": ["Disciplina não existe"]}), 400

    # Limite de ausências dos alunos
    limite_ausencias = disciplina.carga_horaria / calcular_intervalo(hora_para_string(aula.hora_inicio), hora_para_string(aula.hora_fim))

    # verificar se aula é de uma turma ativa
    turma = db.session.get(Turma, aula.turma_id)
    if turma is None:
        return jsonify({"erro": ["Turma não existe"]}), 400
    
    if turma.status != 'A':
        return jsonify({"erro": ["Turma inativa"]}), 400

    # Para cada aluno, buscar o boletim relacionado a ele e a aula e cadastrar a ausência
    for aluno in data["alunos"]:
        # pegar o aluno
        if aluno['ausencia']:
            aluno_existente = db.session.get(Aluno, aluno['matricula'])
            if aluno_existente is None:
                return jsonify({"erro": ["Algum aluno não foi encontrado"]}), 400
            
            # pegar o boletim
            boletim = db.session.query(Boletim).filter_by(aluno_matricula=aluno['matricula'], aula_id=aula.id).first()
            # tratar um possivel erro
            if boletim is None:
                return jsonify({"erro": ["Algum boletim não foi encontrado"]}), 400
            
            # adicionar ausencia
            boletim.ausencias += 1

            # verificar se aluno reprovou por falta
            if boletim.ausencias >= limite_ausencias and boletim.situacao != 'R':
                boletim.situacao = 'R'
    
    db.session.commit()

    return jsonify({"mensagem": "Ausências cadastradas com sucesso!"}), 200


def buscar_ausencias_aula(aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Busca ausências de todos os alunos em uma determinada aula no banco de dados.

    Esta função recebe os dados de vários alunos, disciplina e turma via JSON, valida os dados e, se válidos, busca as ausências de todos os alunos 
    em uma determinada aula no banco de dados.

    Args: 
        aula_id (int): Id da aula.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados da ausência de cada aluno, ou uma mensagem de erro em caso de dados inválidos.
    """
    # verificar existência de aula
    aula = db.session.get(Aula, aula_id)
    if aula is None:
        return jsonify({"erro": ["Aula não existe"]}), 400

    # verificar se aula é de uma turma ativa
    turma = db.session.get(Turma, aula.turma_id)
    if turma is None:
        return jsonify({"erro": ["Turma não existe"]}), 400
    
    if turma.status != 'A':
        return jsonify({"erro": ["Turma inativa"]}), 400
    
    # pegar todos os boletins da aula
    boletins = db.session.query(Boletim).filter_by(aula_id=aula_id)

    # tratar um possivel erro
    if boletins is None:
        return jsonify({"erro": ["Nenhum boletim foi encontrado"]}), 400
    
    # retornar todos os alunos dessa aula
    return jsonify({"aula_id": aula.id, "alunos": [{"matricula": boletim.aluno.matricula, "nome": boletim.aluno.nome} for boletim in boletins]}), 200


def buscar_ausencias_aluno (aluno_matricula: str, aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Busca ausências de um aluno em específico no banco de dados.

    Esta função recebe os dados de disciplina e turma via JSON, valida os dados e, se válidos, busca as ausências de um aluno no banco de dados.

    Args: 
        aluno_matricula (str): Matrícula do aluno.
        aula_id (int): Id da aula.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados da ausência de um aluno, ou uma mensagem de erro em caso de dados inválidos.
    """
    # pegar a aula
    aula = db.session.get(Aula, aula_id)
    if aula is None:
        return jsonify({"erro": ["Aula não existe"]}), 400

    # pegar o aluno
    aluno = db.session.get(Aluno, aluno_matricula)
    if aluno is None:
        return jsonify({"erro": ["Aluno não existe"]}), 400

    # pegar o boletim do aluno
    boletim = db.session.query(Boletim).filter_by(aluno_matricula=aluno_matricula, aula_id=aula_id).first()
    if boletim is None:
        return jsonify({"erro": ["Boletim não existe"]}), 400

    return jsonify({"aula_id": aula.id, "matricula": aluno.matricula, "nome": aluno.nome, "ausencias": boletim.ausencias }), 200


# essa aqui é a função que vai alterar a ausência de um aluno específico
def alterar_ausencia(aluno_matricula: str, aula_id: int, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Altera ausências de um aluno em específico no banco de dados.

    Esta função recebe os dados de disciplina e turma via JSON, valida os dados e, se válidos, altera as ausências de um aluno no banco de dados.

    Args: 
        aluno_matricula (str): Matrícula do aluno.
        aula_id (int): Id da aula.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma mensagem de sucesso e os dados da ausência de um aluno, ou uma mensagem de erro em caso de dados inválidos.
    """
    data = request.get_json()

    # validar json
    erros = validar_ausencias_alteradas(ausencias=data['ausencias'])
    if erros:
        return jsonify({"erro": erros}), 400
    
    # pegar aula
    aula = db.session.get(Aula, aula_id)
    if aula is None:
        return jsonify({"erro": ["Aula não existe"]}), 400

    # pegar aluno
    aluno = db.session.get(Aluno, aluno_matricula)
    if aluno is None:
        return jsonify({"erro": ["Aluno não existe"]}), 400

    # pegar boletim
    boletim = db.session.query(Boletim).filter_by(aluno_matricula=aluno_matricula, aula_id=aula_id).first()
    if boletim is None:
        return jsonify({"erro": ["Boletim não existe"]}), 400

    # alterar ausencia do boletim
    boletim.ausencias = data['ausencias']

    db.session.commit()

    return jsonify({"mensagem": "Ausências alteradas com sucesso!", "ausencias": boletim.ausencias }), 200