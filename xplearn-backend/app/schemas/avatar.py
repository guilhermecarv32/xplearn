from typing import Optional, List
from pydantic import BaseModel

class AvatarBase(BaseModel):
    caminho_foto: str
    nome: Optional[str] = None
    
class AvatarCreate(AvatarBase):
    pass
    
class AvatarResponse(AvatarBase):
    id: int
    
    class Config:
        from_attributes = True

class AvatarResponseList(BaseModel):
    data: List[AvatarResponse]
    
    class Config:
        from_attributes = True

class AvatarResponseSingle(BaseModel):
    data: AvatarResponse
    
    class Config:
        from_attributes = True