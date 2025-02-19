from sqlalchemy import Column, Integer, String, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sala import Sala
from calendario import Calendario

Base = declarative_base()

class Turma(Base):
    idTurma = Column(Integer, primary_key = True, autoincrement = True),
    ano = Column(Integer, nullable = False),
    serie = Column(CHAR(1), nullable = False),
    nivelEnsino = Column(String(30), nullable = False),
    turno = Column(CHAR(1), nullable = False),
    status = Column(CHAR(1), nullable = False),
    numSala = Column(Integer, ForeignKey('sala.numero'), nullable = False),
    anoLetivoCalendario = Column(Integer, ForeignKey('calendario.anoLetivo'), nullable = False)

    sala = relationship('Sala', backref = 'sala'),
    calendario = relationship('Calendario', backref = 'calendario')


