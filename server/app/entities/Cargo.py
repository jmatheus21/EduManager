from sqlalchemy import Column, Date, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

class Cargo:
    usuario_cpf = Column(String(20), ForeignKey('usuario.id'))
    nome = Column(String(100), nullable=False)
    salario = Column(Numeric(10, 2), nullable=False)
    data_contrato = Column(Date, nullable=False)

    usuario = relationship('Usuario', back_populates='cargo')