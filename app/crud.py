from sqlalchemy.orm import Session
from typing import List, Optional
import random
from . import models, schemas

class CRUD:
    def __init__(self, db: Session):
        self.db = db

    # Операторы
    def create_operator(self, operator: schemas.OperatorCreate) -> models.Operator:
        db_operator = models.Operator(**operator.model_dump())
        self.db.add(db_operator)
        self.db.commit()
        self.db.refresh(db_operator)
        return db_operator

    def get_operators(self, skip: int = 0, limit: int = 100) -> List[models.Operator]:
        return self.db.query(models.Operator).offset(skip).limit(limit).all()

    def get_operator(self, operator_id: int) -> Optional[models.Operator]:
        return self.db.query(models.Operator).filter(models.Operator.id == operator_id).first()

    def update_operator(self, operator_id: int, operator: schemas.OperatorCreate) -> Optional[models.Operator]:
        db_operator = self.get_operator(operator_id)
        if db_operator:
            for key, value in operator.model_dump().items():
                setattr(db_operator, key, value)
            self.db.commit()
            self.db.refresh(db_operator)
        return db_operator

    # Источники
    def create_source(self, source: schemas.SourceCreate) -> models.Source:
        db_source = models.Source(**source.model_dump())
        self.db.add(db_source)
        self.db.commit()
        self.db.refresh(db_source)
        return db_source

    def get_sources(self) -> List[models.Source]:
        return self.db.query(models.Source).all()

    # Компетенции
    def set_competence(self, competence: schemas.CompetenceCreate) -> models.OperatorCompetence:
        # Проверяем, существует ли уже такая компетенция
        existing = self.db.query(models.OperatorCompetence).filter(
            models.OperatorCompetence.operator_id == competence.operator_id,
            models.OperatorCompetence.source_id == competence.source_id
        ).first()
        
        if existing:
            existing.weight = competence.weight
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            db_competence = models.OperatorCompetence(**competence.model_dump())
            self.db.add(db_competence)
            self.db.commit()
            self.db.refresh(db_competence)
            return db_competence

    # Лиды и обращения
    def find_or_create_lead(self, lead_data: schemas.LeadCreate) -> models.Lead:
        # Ищем лида по external_id, phone или email
        lead = None
        
        if lead_data.external_id:
            lead = self.db.query(models.Lead).filter(
                models.Lead.external_id == lead_data.external_id
            ).first()
        
        if not lead and lead_data.phone:
            lead = self.db.query(models.Lead).filter(
                models.Lead.phone == lead_data.phone
            ).first()
            
        if not lead and lead_data.email:
            lead = self.db.query(models.Lead).filter(
                models.Lead.email == lead_data.email
            ).first()
        
        if not lead:
            # Создаем нового лида
            lead = models.Lead(**lead_data.model_dump())
            self.db.add(lead)
            self.db.commit()
            self.db.refresh(lead)
        
        return lead

    def get_operator_current_load(self, operator_id: int) -> int:
        # Считаем количество активных обращений у оператора
        return self.db.query(models.Contact).filter(
            models.Contact.operator_id == operator_id
        ).count()

    def distribute_contact(self, source_id: int) -> Optional[int]:
        # Находим доступных операторов для источника
        competences = self.db.query(models.OperatorCompetence).filter(
            models.OperatorCompetence.source_id == source_id
        ).all()
        
        if not competences:
            return None
        
        # Фильтруем операторов по активности и нагрузке
        available_operators = []
        weights = []
        
        for comp in competences:
            operator = comp.operator
            if operator and operator.is_active:
                current_load = self.get_operator_current_load(operator.id)
                if current_load < operator.max_load:
                    available_operators.append(operator.id)
                    weights.append(comp.weight)
        
        if not available_operators:
            return None
        
        # Выбираем оператора случайным образом с учетом весов
        if len(available_operators) == 1:
            return available_operators[0]
        
        total_weight = sum(weights)
        rand_val = random.uniform(0, total_weight)
        cumulative = 0
        
        for i, weight in enumerate(weights):
            cumulative += weight
            if rand_val <= cumulative:
                return available_operators[i]
        
        return available_operators[0]

    def create_contact(self, contact: schemas.ContactCreate) -> models.Contact:
        # Находим или создаем лида
        lead = self.find_or_create_lead(contact.lead_data)
        
        # Распределяем обращение
        operator_id = self.distribute_contact(contact.source_id)
        
        # Создаем обращение
        db_contact = models.Contact(
            lead_id=lead.id,
            source_id=contact.source_id,
            operator_id=operator_id,
            message=contact.message
        )
        
        self.db.add(db_contact)
        self.db.commit()
        self.db.refresh(db_contact)
        
        return db_contact

    def get_contacts(self, skip: int = 0, limit: int = 100) -> List[models.Contact]:
        return self.db.query(models.Contact).offset(skip).limit(limit).all()

    def get_leads(self, skip: int = 0, limit: int = 100) -> List[models.Lead]:
        return self.db.query(models.Lead).offset(skip).limit(limit).all()