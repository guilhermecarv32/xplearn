from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class Avatar(Base):
    __tablename__ = "Avatar"
    
    id = Column(Integer, primary_key=True, index=True)
    caminho_foto = Column(String, nullable=False)
    nome = Column(String, nullable=True)