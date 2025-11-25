from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Operator(Base):
    __tablename__ = "operators"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    max_load = Column(Integer, default=10)
    
    competencies = relationship("OperatorCompetence", back_populates="operator")
    leads = relationship("Lead", back_populates="operator")

class Source(Base):
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    competencies = relationship("OperatorCompetence", back_populates="source")
    contacts = relationship("Contact", back_populates="source")

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    operator_id = Column(Integer, ForeignKey("operators.id"))
    
    operator = relationship("Operator", back_populates="leads")
    contacts = relationship("Contact", back_populates="lead")

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    message = Column(String, nullable=True)
    
    lead = relationship("Lead", back_populates="contacts")
    source = relationship("Source", back_populates="contacts")
    operator = relationship("Operator")

class OperatorCompetence(Base):
    __tablename__ = "operator_competences"
    
    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("operators.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))
    weight = Column(Integer, default=1)
    
    operator = relationship("Operator", back_populates="competencies")
    source = relationship("Source", back_populates="competencies")