from datetime import timedelta
from app import database
from app.models.aluno import Aluno
from app.models.professor import Professor
from app.schemas import login as schemas
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/aluno", response_model=schemas.LoginAlunoResponse)
def login_aluno(aluno: schemas.LoginAlunoBase, db: Session = Depends(database.get_db)):
    
    try:
        db_aluno = db.query(Aluno).filter(Aluno.matricula == aluno.matricula).first()
        
        if db_aluno is None:
            raise HTTPException(status_code=404, detail="Matricula não registrada")
        
        senha_corresponde = verify_password(plain_password=aluno.senha, hashed_password=db_aluno.senha)
        
        if not senha_corresponde:
            raise HTTPException(status_code=401, detail="Usuário e/ou senha incorretas.")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(db_aluno.matricula)},
            expires_delta=access_token_expires
        )
        
        return {
            "data": {
                "matricula": aluno.matricula, "access_token": access_token
            }
        }
    
    except HTTPException as e:
        raise e
    except SQLAlchemyError as e:
        print(f"Erro no banco de dados durante o login do aluno: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro no banco de dados ao tentar realizar o login."
        )
    except Exception as e:
        print(f"Erro inesperado no login do aluno: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao tentar realizar o login."
        )

@router.post("/professor", response_model=schemas.LoginProfessorResponse)
def login_professor(professor: schemas.LoginProfessorBase, db: Session = Depends(database.get_db)):  
    try:
        db_prof = db.query(Professor).filter(Professor.matricula == professor.matricula).first()
        
        if db_prof is None:
            raise HTTPException(status_code=404, detail="Matricula não registrada")
        
        senha_corresponde = verify_password(plain_password=professor.senha, hashed_password=db_prof.senha)
        
        if not senha_corresponde:
            raise HTTPException(status_code=401, detail="Usuário e/ou senha incorretas.")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(db_prof.matricula)},
            expires_delta=access_token_expires
        )
        
        return {
            "data": {
                "matricula": professor.matricula, "access_token": access_token
            }
        }
    
    except HTTPException as e:
        raise e
    except SQLAlchemyError as e:
        print(f"Erro no banco de dados durante o login do professor: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro no banco de dados ao tentar realizar o login."
        )
    except Exception as e:
        print(f"Erro inesperado no login do professor: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao tentar realizar o login."
        )