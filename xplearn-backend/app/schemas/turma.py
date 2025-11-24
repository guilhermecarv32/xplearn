from pydantic import BaseModel
from typing import List, Optional

class TurmaBase(BaseModel):
    nome: str
    professor_matricula_fk: str
    
class TurmaCreate(TurmaBase):
    pass

class TurmaResponse(TurmaBase):
    id: int
    nome: str
    professor_matricula_fk: str
                
class TurmaResponseList(BaseModel):
    data: List[TurmaResponse]
        
    class Config:
        from_attributes = True
        
class TurmaResponseSingle(BaseModel):
    data: TurmaResponse     
     
    class Config:
        from_attributes = True