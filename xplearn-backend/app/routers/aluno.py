from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import database
from app.schemas import aluno as schemas
from app.models.aluno import Aluno
from app.models.avatar import Avatar


from datetime import timedelta
from app.security import hash_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.post("/", response_model=schemas.AlunoResponseCreate)
def create_user(aluno: schemas.AlunoCreate, db: Session = Depends(database.get_db)):
    
    try:
        db_aluno = db.query(Aluno).filter(Aluno.matricula == aluno.matricula).first()
        if db_aluno:
            raise HTTPException(status_code=400, detail="Matricula já registrada")
        
        avatar = None
        if aluno.avatar_id_fk:
            avatar = db.query(Avatar).filter(Avatar.id == aluno.avatar_id_fk).first()
            if not avatar:
                raise HTTPException(status_code=404, detail="Avatar não encontrado")
            
        existing_user = db.query(Aluno).filter(Aluno.nickname == aluno.nickname).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Nickname já está em uso")

        hashed_pwd = hash_password(aluno.senha)
        
        new_aluno = Aluno(
            matricula=aluno.matricula,
            senha=hashed_pwd,
            nickname=aluno.nickname,
            nome=aluno.nome,
            xp=aluno.xp,
            nivel=aluno.nivel,
            avatar_id_fk=aluno.avatar_id_fk
        )
        
        db.add(new_aluno)
        db.commit()
        db.refresh(new_aluno)
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(new_aluno.matricula)}, 
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
        db.rollback()
        print(f"Erro no banco de dados ao criar aluno: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no banco de dados: Não foi possível criar o aluno. Detalhe: {e}"
        )
    except Exception as e:
        db.rollback() 
        print(f"Erro inesperado ao criar aluno: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao criar aluno."
        )
    
@router.get("/", response_model=schemas.AlunoResponseList)
def get_alunos(db: Session = Depends(database.get_db)):
    try:
        alunos = db.query(Aluno).all()
        return {"data": alunos}
    except SQLAlchemyError as e:
        print(f"Erro no banco de dados ao listar alunos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro no banco de dados ao buscar lista de alunos."
        )
    except Exception as e:
        print(f"Erro inesperado ao listar alunos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao listar alunos."
        )

@router.get("/{matricula}", response_model=schemas.AlunoResponseSingle)
def get_aluno_by_id(matricula: str, db: Session = Depends(database.get_db)):
    try:
        aluno = db.query(Aluno).filter(Aluno.matricula == matricula).first()
        
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        
        return {"data": aluno}
    except HTTPException as e:
        raise e
    except SQLAlchemyError as e:
        print(f"Erro no banco de dados ao buscar aluno por matrícula: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro no banco de dados ao buscar aluno."
        )
    except Exception as e:
        print(f"Erro inesperado ao buscar aluno por matrícula: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao buscar aluno."
        )