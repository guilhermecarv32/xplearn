from pyexpat import model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .aluno_turma import aluno_turma
from app.database import Base

class Turma(Base):
    __tablename__ = "Turma"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    
    professor_matricula_fk = Column(String, ForeignKey("Professor.matricula"), nullable=True)

    professor = relationship("Professor", backref="Turma")

    alunos = relationship(
        "Aluno",
        secondary=aluno_turma,
        back_populates="turmas"
    )