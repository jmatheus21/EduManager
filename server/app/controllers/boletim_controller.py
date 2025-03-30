"""
Módulo de Controlador para Boletins

Este módulo contém as funções que implementam a lógica de negócio para as operações relacionadas aos Boletins.
Ele interage com o modelo `Boletim` para realizar operações CRUD e valida os dados usando o módulo `validators`.
"""

from flask import jsonify, send_file
from app.extensions import db
from ..models import Aula, Usuario, Turma, Disciplina, Aluno, Boletim
from app.utils.boletim_helpers import gerar_pdf_boletim, gerar_pdf_historico


def listar_aulas_professor (current_user_cpf: str, current_user_role: str) -> jsonify:
    """Lista todas as aulas, vinculadas à um determinado professor, cadastradas no banco de dados.

    Args:
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo uma lista de aulas com seus respectivos dados.
    """
    usuario = db.session.query(Usuario).filter_by(cpf = current_user_cpf).first()
    if usuario.tipo != current_user_role:
        return jsonify({"erro": ["O usuário não tem permissão para acessar a página"]})
    
    aulas = db.session.query(Aula).filter_by(usuario_id=usuario.id)

    resposta = {"turmas": [], "disciplinas": []}
    for aula in aulas:
        turma = db.session.get(Turma, aula.turma_id)
        if turma.status == "A":
            turma_atual = {
                "id": turma.id,
                "ano": turma.ano,
                "serie": turma.serie,
                "nivel_de_ensino": turma.nivel_de_ensino
            }

            if turma_atual not in resposta["turmas"]:
                resposta["turmas"].append(turma_atual)
            
            disciplina = db.session.get(Disciplina, aula.disciplina_codigo)
            resposta["disciplinas"].append({
                "turma_id": turma.id,
                "codigo": disciplina.codigo,
                "nome": disciplina.nome,
                "aula_id": aula.id
            })

    return jsonify(resposta), 200


def buscar_boletim (aluno_matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Busca um boletim específico pela matrícula do aluno.

    Args:
        aluno_matricula (str): A matrícula do aluno a ser buscada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        jsonify: Resposta JSON contendo os dados do boletim encontrado.
    """
    aluno = db.session.get(Aluno, aluno_matricula)
    if not aluno:
        return jsonify({"erro": ["Aluno não existe"]}), 400
    
    turma_atual = max(aluno.turmas, key=lambda turma: turma.calendario_ano_letivo)
    if not turma_atual:
        return jsonify({"erro": ["Aluno não está matriculado em nenhuma turma!"]}), 400
    
    boletins = {
        b.aula_id: b for b in db.session.query(Boletim)
        .filter_by(aluno_matricula=aluno.matricula)
        .filter(Boletim.aula_id.in_([a.id for a in turma_atual.aulas]))
        .all()
    }
    
    data = []
    for aula in turma_atual.aulas:
        boletim = boletins.get(aula.id)
        if not boletim:
            return jsonify({"erro": ["O aluno não está associado a todas as aulas da turma"]}), 400
        
        notas_boletim = boletim.notas

        notas = (notas_boletim + [None] * 4)[:4] if notas_boletim else [None] * 4
        
        situacao_map = {"A": "Aprovado", "R": "Reprovado", "M": "Cursando"}
        situacao = situacao_map.get(boletim.situacao, "Cursando")

        # Calcula a média
        if all(n is not None for n in notas):
            media = sum(notas) / len(notas)
            media_formatada = f"{media:.1f}"
        else:
            media_formatada = "---"
        
        data.append([
            aula.disciplina.nome,
            f"{notas[0]:.1f}" if notas[0] is not None else "---",
            f"{notas[1]:.1f}" if notas[1] is not None else "---",
            f"{notas[2]:.1f}" if notas[2] is not None else "---",
            f"{notas[3]:.1f}" if notas[3] is not None else "---",
            str(boletim.ausencias),
            media_formatada,
            situacao
        ])
    
    return jsonify({"aluno_matricula": aluno.matricula, "aluno_nome": aluno.nome, "turma_ano": turma_atual.ano, "turma_serie": turma_atual.serie, "turma_nivel_de_ensino": turma_atual.nivel_de_ensino, "boletim": [{"disciplina": b[0], "u1": b[1], "u2": b[2], "u3": b[3], "u4": b[4], "media": b[5], "ausencias": b[6], "situacao": b[7]} for b in data]}), 200


def gerar_boletim(aluno_matricula: str, current_user_cpf: str, current_user_role: str):
    """Gera um boletim específico, em formato .pdf, pela matrícula do aluno.

    Args:
        aluno_matricula (str): A matrícula do aluno a ser gerado o boletim.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        PDF: Resposta .pdf contendo os dados do boletim gerado.
    """
    aluno = db.session.get(Aluno, aluno_matricula)
    if not aluno:
        return jsonify({"erro": ["Aluno não existe"]}), 400
    
    if not aluno.turmas:
        return jsonify({"erro": ["Aluno não está matriculado em nenhuma turma!"]}), 400
    
    turma_atual = max(aluno.turmas, key=lambda turma: turma.calendario_ano_letivo)
    
    boletins = {
        b.aula_id: b for b in db.session.query(Boletim)
        .filter_by(aluno_matricula=aluno.matricula)
        .filter(Boletim.aula_id.in_([a.id for a in turma_atual.aulas]))
        .all()
    }
    
    # Verifica se todas as aulas têm boletim
    for aula in turma_atual.aulas:
        if aula.id not in boletins:
            return jsonify({"erro": ["O aluno não está associado a todas as aulas da turma"]}), 400
    
    # Prepara dados para o PDF
    data_aluno = {"nome": aluno.nome, "matricula": aluno.matricula}
    data_turma = {
        "ano": turma_atual.ano,
        "serie": turma_atual.serie,
        "nivel_de_ensino": turma_atual.nivel_de_ensino,
        "ano_letivo": turma_atual.calendario_ano_letivo,
    }
    
    data = []
    for aula in turma_atual.aulas:
        boletim = boletins[aula.id]
        notas_boletim = boletim.notas

        notas = (notas_boletim + [None] * 4)[:4] if notas_boletim else [None] * 4

        situacao = {"A": "Aprovado", "R": "Reprovado", "M": "Cursando"}.get(boletim.situacao, "Cursando")

        # Calcula a média
        if all(n is not None for n in notas):
            media = sum(notas) / len(notas)
            media_formatada = f"{media:.1f}"
        else:
            media_formatada = "---"
        
        data.append([
            aula.disciplina.nome,
            *[f"{n:.1f}" if n is not None else "---" for n in notas],
            media_formatada,
            str(boletim.ausencias),
            situacao
        ])
    
    # Gera o PDF
    pdf_buffer = gerar_pdf_boletim(data_aluno, data_turma, data)
    
    # Limpa qualquer resposta que possa ter sido iniciada
    response = send_file(
        pdf_buffer,
        mimetype='application/pdf',
        download_name=f'boletim_{aluno_matricula}.pdf',
        as_attachment=True
    )
    
    # Fecha o buffer explicitamente após o envio
    response.call_on_close(pdf_buffer.close)
    return response


def buscar_historico (aluno_matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Busca o histórico pela matrícula do aluno.

    Args:
        aluno_matricula (str): A matrícula do aluno a ser buscada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        PDF: Resposta .pdf contendo os dados do histórico buscado.
    """
    aluno = db.session.get(Aluno, aluno_matricula)
    if not aluno:
        return jsonify({"erro": ["Aluno não existe"]}), 400
    
    if not aluno.turmas:
        return jsonify({"erro": ["Aluno não está matriculado em nenhuma turma!"]}), 400
    
    boletins = {
        b.aula_id: b for b in db.session.query(Boletim)
        .filter_by(aluno_matricula=aluno.matricula)
        .all()
    }

    data_historico = []
    for turma in aluno.turmas:
        data_turma = {
            "ano": turma.ano,
            "serie": turma.serie,
            "nivel_de_ensino": turma.nivel_de_ensino,
            "ano_letivo": turma.calendario_ano_letivo,
            "aulas": []
        }
        for aula in turma.aulas:
            boletim = boletins.get(aula.id)
            if not boletim:
                return jsonify({"erro": ["O aluno não está associado a todas as aulas das turmas"]}), 400

            notas_boletim = boletim.notas
            notas = (notas_boletim + [None] * 4)[:4] if notas_boletim else [None] * 4
            
            situacao = {"A": "Aprovado", "R": "Reprovado", "M": "Cursando"}.get(boletim.situacao, "Cursando")

            # Calcula a média
            if all(n is not None for n in notas):
                media = sum(notas) / len(notas)
                media_formatada = f"{media:.1f}"
            else:
                media_formatada = "---"
            
            data_turma["aulas"].append([
                aula.disciplina.nome,
                f"{notas[0]:.1f}" if notas[0] is not None else "---",
                f"{notas[1]:.1f}" if notas[1] is not None else "---",
                f"{notas[2]:.1f}" if notas[2] is not None else "---",
                f"{notas[3]:.1f}" if notas[3] is not None else "---",
                media_formatada,
                str(boletim.ausencias),
                situacao
            ])
        data_historico.append(data_turma)
    
    return jsonify({"aluno_matricula": aluno.matricula, "aluno_nome": aluno.nome, "turmas": [{"ano": t["ano"], "serie": t["serie"], "nivel_de_ensino": t["nivel_de_ensino"], "ano_letivo": t["ano_letivo"], "aulas": [{"disciplina": b[0], "u1": b[1], "u2": b[2], "u3": b[3], "u4": b[4], "media": b[5], "ausencias": b[6], "situacao": b[7]} for b in t["aulas"]]} for t in data_historico]})


def gerar_historico (aluno_matricula: str, current_user_cpf: str, current_user_role: str) -> jsonify:
    """Gera o histórico pela matrícula do aluno.

    Args:
        aluno_matricula (str): A matrícula do aluno a ser gerada.
        current_user_cpf (str): O cpf do usuário autenticado.
        current_user_role (str): O role do usuário autenticado.

    Returns:
        PDF: Resposta .pdf contendo os dados do histórico gerado.
    """
    aluno = db.session.get(Aluno, aluno_matricula)
    if not aluno:
        return jsonify({"erro": ["Aluno não existe"]}), 400
    
    if not aluno.turmas:
        return jsonify({"erro": ["Aluno não está matriculado em nenhuma turma!"]}), 400
    
    boletins = {
        b.aula_id: b for b in db.session.query(Boletim)
        .filter_by(aluno_matricula=aluno.matricula)
        .all()
    }

    data_aluno = {
        "nome": aluno.nome,
        "matricula": aluno.matricula
    }

    data_historico = []
    for turma in aluno.turmas:
        data_turma = {
            "ano": turma.ano,
            "serie": turma.serie,
            "nivel_de_ensino": turma.nivel_de_ensino,
            "ano_letivo": turma.calendario_ano_letivo,
            "aulas": []
        }
        for aula in turma.aulas:
            boletim = boletins.get(aula.id)
            if not boletim:
                return jsonify({"erro": ["O aluno não está associado a todas as aulas das turmas"]}), 400

            notas_boletim = boletim.notas
            notas = (notas_boletim + [None] * 4)[:4] if notas_boletim else [None] * 4
            
            situacao = {"A": "Aprovado", "R": "Reprovado", "M": "Cursando"}.get(boletim.situacao, "Cursando")

            # Calcula a média
            if all(n is not None for n in notas):
                media = sum(notas) / len(notas)
                media_formatada = f"{media:.1f}"
            else:
                media_formatada = "---"
            
            data_turma["aulas"].append([
                aula.disciplina.nome,
                f"{notas[0]:.1f}" if notas[0] is not None else "---",
                f"{notas[1]:.1f}" if notas[1] is not None else "---",
                f"{notas[2]:.1f}" if notas[2] is not None else "---",
                f"{notas[3]:.1f}" if notas[3] is not None else "---",
                media_formatada,
                str(boletim.ausencias),
                situacao
            ])
        data_historico.append(data_turma)
    
    pdf_buffer = gerar_pdf_historico(data_aluno, data_historico)
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        download_name=f'boletim_{aluno_matricula}.pdf',
        as_attachment=True
    )