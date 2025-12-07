from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import hashlib
import os

from .. import models, schemas
from ..database import get_db
from ..services import pdf_service, mapping_service

router = APIRouter(
    prefix="/templates",
    tags=["templates"],
)

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_file_hash(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()

@router.post("/", response_model=schemas.Template)
async def create_template(
    file: UploadFile = File(...),
    template_name: str = Form(None),
    tenant_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Upload a new PDF template.
    - Extracts fields from the PDF
    - Auto-suggests GraphDB mappings
    - Stores template and field mappings
    """
    try:
        # Read file content
        content = await file.read()
        file_hash = get_file_hash(content)
        
        # Check if template already exists
        existing = db.query(models.Template).filter(
            models.Template.tenant_id == tenant_id,
            models.Template.template_hash == file_hash
        ).first()
        
        if existing:
            print(f"✓ Template already exists: {existing.id}")
            return existing
            
        # Save PDF file
        file_path = os.path.join(UPLOAD_DIR, f"{file_hash}.pdf")
        with open(file_path, "wb") as f:
            f.write(content)
        
        print(f"✓ Saved PDF: {file_path}")
        
        # Extract fields from PDF
        extracted_fields = pdf_service.extract_fields_from_pdf(content)
        print(f"✓ Extracted {len(extracted_fields)} fields")
        
        # Create template record
        db_template = models.Template(
            tenant_id=tenant_id,
            template_hash=file_hash,
            template_name=template_name or file.filename,
            file_path=file_path
        )
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        
        print(f"✓ Created template: {db_template.id}")
        
        # Create field mappings with auto-suggestions
        for field in extracted_fields:
            source, entity, prop = mapping_service.suggest_mapping(field['label_text'])
            
            db_mapping = models.FieldMapping(
                template_id=db_template.id,
                field_name=field['field_name'],
                label_text=field['label_text'],
                source=source,
                entity_type=entity,
                property_name=prop
            )
            db.add(db_mapping)
            print(f"  - {field['field_name']}: {source} ({entity}.{prop if prop else 'N/A'})")
        
        db.commit()
        db.refresh(db_template)
        
        print(f"✓ Template created successfully with {len(extracted_fields)} fields")
        return db_template
        
    except Exception as e:
        import traceback
        error_msg = f"Error creating template: {str(e)}"
        print(f"✗ {error_msg}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/{template_id}/fields", response_model=schemas.Template)
def get_template_fields(template_id: int, db: Session = Depends(get_db)):
    """
    Get all fields and their mappings for a template.
    """
    template = db.query(models.Template).filter(models.Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.post("/{template_id}/fields/mapping", response_model=schemas.Template)
def update_mapping(
    template_id: int,
    mapping_update: schemas.MappingUpdate,
    db: Session = Depends(get_db)
):
    """
    Update field mappings (admin confirms GraphDB vs Manual).
    """
    template = db.query(models.Template).filter(models.Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
        
    for update in mapping_update.fields:
        field = db.query(models.FieldMapping).filter(
            models.FieldMapping.template_id == template_id,
            models.FieldMapping.field_name == update.field_name
        ).first()
        
        if field:
            if update.source == "manual":
                field.source = "manual"
                field.entity_type = None
                field.property_name = None
                print(f"✓ Set {field.field_name} to MANUAL")
                
            elif update.source == "graphdb":
                # Re-apply mapping rules
                _, entity, prop = mapping_service.suggest_mapping(field.label_text)
                if not entity:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"No GraphDB mapping available for '{field.label_text}'"
                    )
                
                field.source = "graphdb"
                field.entity_type = entity
                field.property_name = prop
                print(f"✓ Set {field.field_name} to GRAPHDB ({entity}.{prop})")
            
            db.add(field)
            
    db.commit()
    db.refresh(template)
    return template

@router.get("/{template_id}/diagnose")
def diagnose_pdf_fields(template_id: int, db: Session = Depends(get_db)):
    """
    Diagnostic endpoint to inspect PDF form fields.
    Returns detailed information about all fields in the PDF.
    """
    template = db.query(models.Template).filter(models.Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if not os.path.exists(template.file_path):
        raise HTTPException(status_code=500, detail="Template PDF file not found")
    
    try:
        import fitz
        doc = fitz.open(template.file_path)
        
        diagnostic_info = {
            "template_id": template_id,
            "template_name": template.template_name,
            "file_path": template.file_path,
            "total_pages": len(doc),
            "fields": []
        }
        
        for page_num, page in enumerate(doc):
            widgets = page.widgets()
            if widgets:
                for widget in widgets:
                    field_info = {
                        "page": page_num + 1,
                        "field_name": widget.field_name,
                        "field_type": widget.field_type,
                        "field_type_string": widget.field_type_string,
                        "current_value": widget.field_value,
                        "text_color": widget.text_color,
                        "text_fontsize": widget.text_fontsize,
                        "border_color": widget.border_color,
                        "fill_color": widget.fill_color,
                    }
                    diagnostic_info["fields"].append(field_info)
        
        doc.close()
        
        diagnostic_info["total_fields"] = len(diagnostic_info["fields"])
        return diagnostic_info
        
    except Exception as e:
        import traceback
        print(f"✗ Error diagnosing PDF: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error diagnosing PDF: {str(e)}")

