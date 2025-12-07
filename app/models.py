from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    template_hash = Column(String, unique=True, index=True)
    template_name = Column(String)
    confirm_threshold = Column(Integer, default=2)
    file_path = Column(String)

    fields = relationship("FieldMapping", back_populates="template", lazy="joined")

class FieldMapping(Base):
    __tablename__ = "field_mappings"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("templates.id"))
    field_name = Column(String)
    label_text = Column(String)
    source = Column(String)  # 'graphdb' or 'manual'
    entity_type = Column(String, nullable=True)
    property_name = Column(String, nullable=True)
    confirm_count = Column(Integer, default=0)
    is_locked = Column(Boolean, default=False)

    template = relationship("Template", back_populates="fields")
