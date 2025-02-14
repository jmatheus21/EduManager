from sqlalchemy import Column, String
import Usuario

class Professor(Usuario):
    formacao = Column(String(255), nullable=False)