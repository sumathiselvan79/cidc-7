from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class FieldMappingBase(BaseModel):
    field_name: str
    label_text: str
    source: str
    entity_type: Optional[str] = None
    property_name: Optional[str] = None
    confirm_count: int = 0
    is_locked: bool = False

class FieldMapping(FieldMappingBase):
    id: int
    template_id: int
    
    model_config = ConfigDict(from_attributes=True)

class TemplateBase(BaseModel):
    template_name: Optional[str] = None
    tenant_id: str

class Template(TemplateBase):
    id: int
    template_hash: str
    confirm_threshold: int
    fields: List[FieldMapping] = []
    
    model_config = ConfigDict(from_attributes=True)

class FieldUpdate(BaseModel):
    field_name: str
    source: str

class MappingUpdate(BaseModel):
    fields: List[FieldUpdate]

class FormOpenRequest(BaseModel):
    template_id: int
    graph_keys: dict
    existing_manual_values: Optional[dict] = None

class FormSubmitRequest(BaseModel):
    template_id: int
    graph_keys: dict
    final_values: dict
