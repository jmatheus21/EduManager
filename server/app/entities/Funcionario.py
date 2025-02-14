from sqlalchemy import Column, String
import Usuario

class Professor(Usuario):
    escolaridade = Column(String(255), nullable=False)
    habilidades = Column(String(255), nullable=False)