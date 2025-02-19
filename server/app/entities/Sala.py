from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sala(Base):
    numero = Column(Integer, primary_key = True, unique = True),
    localizacao = Column(String(10), nullable = False),
    capacidade = Column(Integer, nullable = False)
