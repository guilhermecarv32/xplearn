from pydantic import BaseModel

class LoginAlunoBase(BaseModel):
    matricula: str
    senha: str
    
class LoginAlunoResponse(BaseModel):
    data: dict

class LoginProfessorBase(BaseModel):
    matricula: str
    senha: str
    
class LoginProfessorResponse(BaseModel):
    data: dict