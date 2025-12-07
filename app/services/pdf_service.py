import fitz  # PyMuPDF
import os

def extract_fields_from_pdf(pdf_bytes):
    """
    Extracts fields and attempts to find their labels.
    Returns list of dicts with field_name and label_text
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        fields = []
        
        for page in doc:
            widgets = page.widgets()
            if widgets:
                for widget in widgets:
                    field_name = widget.field_name
                    if not field_name:
                        continue
                        
                    # Attempt to find label text near the field
                    rect = widget.rect
                    # Search area: left of the field
                    search_rect = fitz.Rect(rect.x0 - 150, rect.y0, rect.x0, rect.y1)
                    text = page.get_text("text", clip=search_rect).strip()
                    
                    if not text:
                        # Try above
                        search_rect = fitz.Rect(rect.x0, rect.y0 - 20, rect.x1, rect.y0)
                        text = page.get_text("text", clip=search_rect).strip()
                    
                    label_text = text if text else field_name
                    
                    fields.append({
                        "field_name": field_name,
                        "label_text": label_text
                    })
        
        doc.close()
        return fields
    except Exception as e:
        print(f"Error extracting PDF fields: {e}")
        return []

def fill_pdf_fields(pdf_path, values):
    """
    Fills the PDF with the provided values.
    Returns PDF bytes
    """
    try:
        doc = fitz.open(pdf_path)
        
        for page in doc:
            widgets = page.widgets()
            if widgets:
                for widget in widgets:
                    if widget.field_name in values:
                        widget.field_value = str(values[widget.field_name])
                        widget.update()
                        
        output_bytes = doc.tobytes()
        doc.close()
        return output_bytes
    except Exception as e:
        print(f"Error filling PDF: {e}")
        raise
