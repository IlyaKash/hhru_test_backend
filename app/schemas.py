from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class OperatorBase(BaseModel):
    name: str
    is_active: bool = True
    max_load: int = 10

class OperatorCreate(OperatorBase):
    pass

class Operator(OperatorBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class OperatorWithLoad(Operator):
    current_load: int = 0

class SourceBase(BaseModel):
    name: str

class SourceCreate(SourceBase):
    pass

class Source(SourceBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class CompetenceBase(BaseModel):
    operator_id: int
    source_id: int
    weight: int = 1

class CompetenceCreate(CompetenceBase):
    pass

class Competence(CompetenceBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class LeadBase(BaseModel):
    external_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    operator_id: Optional[int]
    
    model_config = ConfigDict(from_attributes=True)

class ContactBase(BaseModel):
    message: Optional[str] = None
    source_id: int

class ContactCreate(ContactBase):
    lead_data: LeadCreate

class Contact(ContactBase):
    id: int
    lead_id: int
    operator_id: Optional[int]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)