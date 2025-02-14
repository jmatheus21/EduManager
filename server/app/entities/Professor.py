from sqlalchemy import Column, Integer, String
import Usuario

class Professor(Usuario):
    __tablename__ = 'professores'

    formacao = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Professor(nome={self.nome}, email={self.email}, disciplina={self.disciplina})>"
