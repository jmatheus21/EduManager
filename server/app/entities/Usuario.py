from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuario(Base):
    __abstract__ = True

    cpf = Column(String(20), primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)
    telefone = Column(String(50), nullable=True)
    endereco = Column(String(255), nullable=True)
    horario_de_trabalho = Column(String(20), nullable=False)

    def __repr__(self):
        return f"<Usuario(nome={self.nome}, email={self.email})>"