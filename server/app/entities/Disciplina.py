from sqlalchemy import Column, Integer, String

class Disciplina:
    codigo = Column(String(10), primary_key = True, unique = True),
    nome = Column(String(50), nullable = False),
    cargaHoraria = Column(Integer, nullable = False),
    ementa = Column(String(100), nullable = True),
    bibliografia = Column(String(100), nullable = True)