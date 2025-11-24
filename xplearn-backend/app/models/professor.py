from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Professor(Base):
    __tablename__ = "Professor"
    
    matricula = Column(String, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    senha = Column(String, nullable=True)
    avatar_id_fk = Column(Integer, ForeignKey("Avatar.id"), nullable=True)

    avatar = relationship("Avatar", backref="Professor")