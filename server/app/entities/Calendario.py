from sqlalchemy import Column, Date, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Calendario(Base):
    anoLetivo = Column(Integer, primary_key = True, unique = True),
    dataInicio = Column(Date, nullable = False),
    dataFim = Column(Date, nullable = False),
    diasLetivos = Column(Integer, nullable = False)