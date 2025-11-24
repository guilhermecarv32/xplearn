from pydantic import BaseModel
from typing import List, Optional
from typing import Optional

class AlunoBase(BaseModel):
    matricula: str
    nome: str
    nickname: str
    senha: str
    xp: int
    nivel: int
    icone: str | None = None
    avatar_id_fk: Optional[int] = None
    
class AlunoCreate(AlunoBase):
    pass

class AlunoResponse(BaseModel):
    matricula: str
    nome: str
    nickname: str
    xp: int
    nivel: int
    icone: Optional[str] = None
    avatar_id_fk: int

class AlunoResponseList(BaseModel):
    data: List[AlunoResponse]
        
    class Config:
        from_attributes = True
        
class AlunoResponseSingle(BaseModel):
    data: AlunoResponse
    
    class Config:
        from_attributes = True        

class AlunoResponseCreate(BaseModel):
    data: dict
  
