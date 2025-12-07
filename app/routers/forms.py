from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
import os

from .. import models, schemas
from ..database import get_db
from ..services import pdf_service, graph_service

router = APIRouter(
    prefix="/forms",
    tags=["forms"],
)

# Initialize graph service
graph_svc = graph_service.GraphService()

@router.post("/open")
def open_form(
    request: schemas.FormOpenRequest,
    db: Session = Depends(get_db)
):
    """
    Open a form and auto-fill locked GraphDB fields.
    Returns auto-filled values and list of manual fields.
    """
    template = db.query(models.Template).filter(
        models.Template.id == request.template_id
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    print(f"\n📋 Opening form for template: {template.template_name}")
    
    # Partition fields
    locked_graph_fields = []
    unlocked_graph_fields = []
    manual_fields = []
    graph_mappings_to_fetch = []
    
    for field in template.fields:
        if field.source == "manual":
            manual_fields.append({
                "field_name": field.field_name,
                "label_text": field.label_text
            })
            
        elif field.source == "graphdb":
            if field.is_locked:
                locked_graph_fields.append(field)
                graph_mappings_to_fetch.append({
                    "entity_type": field.entity_type,
                    "property_name": field.property_name,
                    "field_name": field.field_name
                })
            else:
                unlocked_graph_fields.append({
                    "field_name": field.field_name,
                    "label_text": field.label_text,
                    "confirm_count": field.confirm_count,
                    "is_locked": False
                })
    
    # Fetch data for locked GraphDB fields
    auto_filled_values = {}
    if graph_mappings_to_fetch:
        print(f"🔍 Fetching {len(graph_mappings_to_fetch)} locked fields from GraphDB")
        auto_filled_values = graph_svc.fetch_values(graph_mappings_to_fetch, request.graph_keys)
        print(f"✓ Retrieved {len(auto_filled_values)} values")
    
    print(f"  - Locked fields: {len(locked_graph_fields)}")
    print(f"  - Unlocked fields: {len(unlocked_graph_fields)}")
    print(f"  - Manual fields: {len(manual_fields)}")
    
    return {
        "template_id": template.id,
        "template_name": template.template_name,
        "auto_filled_values": auto_filled_values,
        "manual_fields": manual_fields,
        "unlocked_graph_fields": unlocked_graph_fields
    }

@router.post("/submit")
def submit_form(
    request: schemas.FormSubmitRequest,
    db: Session = Depends(get_db)
):
    """
    Submit form and generate filled PDF.
    Updates confirmation counts and locks fields when threshold is reached.
    """
    template = db.query(models.Template).filter(
        models.Template.id == request.template_id
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    print(f"\n📝 Submitting form for template: {template.template_name}")
    
    # Update confirmation counts for unlocked GraphDB fields
    for field in template.fields:
        if field.source == "graphdb" and not field.is_locked:
            field.confirm_count += 1
            print(f"  - {field.field_name}: confirm_count = {field.confirm_count}/{template.confirm_threshold}")
            
            if field.confirm_count >= template.confirm_threshold:
                field.is_locked = True
                print(f"    🔒 Field locked!")
            
            db.add(field)
    
    db.commit()
    
    # Fill PDF
    if not os.path.exists(template.file_path):
        raise HTTPException(status_code=500, detail="Template PDF file not found")
    
    try:
        filled_pdf_bytes = pdf_service.fill_pdf_fields(template.file_path, request.final_values)
        print(f"✓ PDF filled successfully with {len(request.final_values)} values")
        
        return Response(
            content=filled_pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=filled_{template.template_name}.pdf"
            }
        )
    except Exception as e:
        import traceback
        print(f"✗ Error filling PDF: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error filling PDF: {str(e)}")
