from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import database
from app.models.aluno import Aluno
from app.schemas import badge as schemas
from app.models.badge import Badge
from app.models.aluno_badge import AlunoBadge

router = APIRouter(prefix="/badges", tags=["Badges"])

@router.post('/', response_model=schemas.BadgeResponseSingle)
def create_badge(badge: schemas.BadgeCreate, db: Session = Depends(database.get_db)):
    
    try:
        new_badge = Badge(
            nome=badge.nome,
            requisito=badge.requisito,
            icone=badge.icone
        )
        
        db.add(new_badge)
        db.commit()
        db.refresh(new_badge)
        
        return {"data": new_badge}
    
    except SQLAlchemyError as e:
        db.rollback() 
        print(f"Erro no banco de dados ao criar badge: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no banco de dados: Não foi possível criar o badge. Detalhe: {e}"
        )
    except Exception as e:
        db.rollback() 
        print(f"Erro inesperado ao criar badge: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao criar badge."
        )

@router.get("/", response_model=schemas.BadgeResponseList)
def get_badges(db: Session = Depends(database.get_db)):
    try:
        badges = db.query(Badge).all()
        return {"data": badges}
    except SQLAlchemyError as e:
        print(f"Erro no banco de dados ao listar badges: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro no banco de dados ao buscar lista de badges."
        )
    except Exception as e:
        print(f"Erro inesperado ao listar badges: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao listar badges."
        )

@router.get("/{id}", response_model=schemas.BadgeResponseSingle)
def get_badge_by_id(id: int, db: Session = Depends(database.get_db)):
    try:
        badge = db.query(Badge).filter(Badge.id == id).first()
        
        if not badge:
            raise HTTPException(status_code=404, detail="Badge não encontrado")
        
        return {"data": badge}
    except HTTPException as e:
        raise e
    except SQLAlchemyError as e:
        print(f"Erro no banco de dados ao buscar badge por ID: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro no banco de dados ao buscar badge."
        )
    except Exception as e:
        print(f"Erro inesperado ao buscar badge por ID: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao buscar badge."
        )

@router.post("/{badge_id}/alunos/{matricula}")
def conquistar_badge(matricula: str, badge_id: int, db: Session = Depends(database.get_db)):
    
    try:
        aluno = db.get(Aluno, matricula)
        badge = db.get(Badge, badge_id)
    
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        if not badge:
            raise HTTPException(status_code=404, detail="Badge não encontrada")
        
        conquista = AlunoBadge(
            aluno_matricula_fk=matricula,
            badge_id_fk=badge_id, 
            data_conquista=date.today()
        )
        
        db.add(conquista)
        db.commit()
        return {"data": "Badge conquistado com sucesso"}
    
    except HTTPException as e:
        raise e
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro no banco de dados ao registrar conquista: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no banco de dados: Não foi possível registrar a conquista. Detalhe: {e}"
        )
    except Exception as e:
        db.rollback()
        print(f"Erro inesperado ao registrar conquista: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao registrar conquista."
        )

@router.get("/alunos/{matricula}")
def get_badges_aluno(matricula: str, db: Session = Depends(database.get_db)):
    
    try:
        aluno = db.get(Aluno, matricula)
        
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        
        conquistas = (
            db.query(AlunoBadge)
            .join(Badge, AlunoBadge.badge_id_fk == Badge.id)
            .filter(AlunoBadge.aluno_matricula_fk == matricula)
            .all()
        )
        
        return {"data": [
            {
                "badge_id": conquista.badge_id_fk,
                "badge_nome": conquista.badge.nome,
                "data_conquista": conquista.data_conquista,
            }
            for conquista in conquistas
        ]}
    except HTTPException as e:
        raise e
    except SQLAlchemyError as e:
        print(f"Erro no banco de dados ao buscar badges do aluno: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro no banco de dados ao buscar badges do aluno."
        )
    except Exception as e:
        print(f"Erro inesperado ao buscar badges do aluno: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao buscar badges do aluno."
        )