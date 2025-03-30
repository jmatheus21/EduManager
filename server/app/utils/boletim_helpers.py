from flask import jsonify
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def criar_cabecalho(titulo: str, aluno=None, turma=None, ano_letivo=None):
    """Cria um cabeçalho genérico para documentos escolares
    
    Args:
        titulo (str): Título do documento (ex: "Boletim Escolar" ou "Histórico Escolar")
        aluno: Objeto aluno com nome e matrícula
        turma: Objeto turma (opcional para histórico)
        ano_letivo: Ano letivo (opcional quando não vem da turma)
    """
    styles = getSampleStyleSheet()
    
    # Estilo para o título principal
    estilo_titulo = styles["Title"]
    estilo_titulo.fontName = 'Helvetica-Bold'
    estilo_titulo.fontSize = 16
    estilo_titulo.leading = 18
    estilo_titulo.alignment = 1  # Centralizado
    
    # Estilo para informações do aluno
    estilo_info = styles["Normal"]
    estilo_info.fontName = 'Helvetica'
    estilo_info.fontSize = 12
    estilo_info.leading = 14

    elementos = []
    
    if aluno:
        elementos = [
            Paragraph(titulo, estilo_titulo),
            Spacer(1, 12),
            
            Paragraph(f"<b>Aluno:</b> {aluno["nome"]}", estilo_info),
            Paragraph(f"<b>Matrícula:</b> {aluno["matricula"]}", estilo_info),
        ]
    
    # Adiciona informações específicas se for boletim ou se tiver turma no histórico
    if turma:
        elementos.extend([
            Paragraph(f"<b>Turma:</b> {turma["ano"]}° Ano {turma["serie"]} - {turma["nivel_de_ensino"]}", estilo_info),
            Paragraph(f"<b>Ano Letivo:</b> {turma["ano_letivo"]}", estilo_info),
        ])
    elif ano_letivo:
        elementos.append(Paragraph(f"<b>Ano Letivo:</b> {turma["ano_letivo"]}", estilo_info))
    
    elementos.append(Spacer(1, 24))
    
    return elementos

def criar_tabela_dados(cabecalho: list, dados: list, col_widths: list = None):
    """Cria uma tabela estilizada com os dados fornecidos
    
    Args:
        cabecalho: Lista com os textos do cabeçalho
        dados: Lista de listas com os dados das linhas
        col_widths: Larguras das colunas (opcional)
    """
    tabela_dados = [cabecalho]
    tabela_dados.extend(dados)
    
    # Larguras padrão se não fornecidas
    if not col_widths:
        col_widths = [120] + [60] * (len(cabecalho)-1)
    
    tabela = Table(tabela_dados, colWidths=col_widths)
    
    estilo = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ])
    
    tabela.setStyle(estilo)
    return tabela

def gerar_pdf_boletim(aluno, turma, dados):
    """Gera um boletim escolar com uma única tabela"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    elementos = criar_cabecalho("BOLETIM ESCOLAR", aluno, turma)
    
    cabecalho = ["Disciplina", "1° Unid.", "2° Unid.", "3° Unid.", "4° Unid.", "Média Final","Ausências", "Situação"]
    tabela = criar_tabela_dados(cabecalho, dados)
    
    elementos.append(tabela)
    doc.build(elementos)
    
    buffer.seek(0)
    return buffer

def gerar_pdf_historico(aluno, turmas):
    """Gera um histórico escolar com múltiplas tabelas (uma por turma)"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    elementos = []
    
    # Título geral do histórico
    elementos.extend(criar_cabecalho("HISTÓRICO ESCOLAR", aluno))

    for turma in turmas:
        # Adiciona cabeçalho específico para cada turma
        elementos.extend(criar_cabecalho("", turma=turma))

        # Cria tabela para a turma
        cabecalho = ["Disciplina", "1° Unid.", "2° Unid.", "3° Unid.", "4° Unid.", "Média Final", "Ausências", "Situação"]
        tabela = criar_tabela_dados(cabecalho, turma['aulas'], [80, 60, 60, 60, 60, 60, 60, 80])
        elementos.append(tabela)

        # Adiciona quebra de página exceto após a última turma
        if turma != turmas[-1]:
            elementos.append(PageBreak())
    
    doc.build(elementos)
    buffer.seek(0)
    return buffer