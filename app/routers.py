from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import engine, get_db

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

router =APIRouter()

# Операторы
@router.post("/operators/", response_model=schemas.Operator)
def create_operator(operator: schemas.OperatorCreate, db: Session = Depends(get_db)):
    return crud.CRUD(db).create_operator(operator)

@router.get("/operators/", response_model=List[schemas.OperatorWithLoad])
def read_operators(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    operators = crud.CRUD(db).get_operators(skip=skip, limit=limit)
    result = []
    for op in operators:
        op_dict = {
            "id": op.id,
            "name": op.name,
            "is_active": op.is_active,
            "max_load": op.max_load,
            "current_load": crud.CRUD(db).get_operator_current_load(op.id)
        }
        result.append(schemas.OperatorWithLoad(**op_dict))
    return result

@router.put("/operators/{operator_id}", response_model=schemas.Operator)
def update_operator(operator_id: int, operator: schemas.OperatorCreate, db: Session = Depends(get_db)):
    db_operator = crud.CRUD(db).update_operator(operator_id, operator)
    if db_operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")
    return db_operator

# Источники
@router.post("/sources/", response_model=schemas.Source)
def create_source(source: schemas.SourceCreate, db: Session = Depends(get_db)):
    return crud.CRUD(db).create_source(source)

@router.get("/sources/", response_model=List[schemas.Source])
def read_sources(db: Session = Depends(get_db)):
    return crud.CRUD(db).get_sources()

# Компетенции
@router.post("/competences/", response_model=schemas.Competence)
def set_competence(competence: schemas.CompetenceCreate, db: Session = Depends(get_db)):
    return crud.CRUD(db).set_competence(competence)

# Обращения
@router.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.CRUD(db).create_contact(contact)

@router.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.CRUD(db).get_contacts(skip=skip, limit=limit)

# Лиды
@router.get("/leads/", response_model=List[schemas.Lead])
def read_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.CRUD(db).get_leads(skip=skip, limit=limit)


