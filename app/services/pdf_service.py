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
    Fills the PDF with the provided values using a hybrid approach:
    1. Sets widget field values (for form functionality)
    2. Draws text directly on the page (for guaranteed visibility)
    Returns PDF bytes
    """
    try:
        doc = fitz.open(pdf_path)
        filled_count = 0
        
        for page_num, page in enumerate(doc):
            widgets = page.widgets()
            if widgets:
                for widget in widgets:
                    field_name = widget.field_name
                    if field_name in values:
                        value = str(values[field_name])
                        
                        # Get widget properties
                        rect = widget.rect
                        current_fontsize = widget.text_fontsize
                        
                        # Method 1: Set the field value (standard approach)
                        widget.field_value = value
                        
                        # Fix font size if needed
                        if not current_fontsize or current_fontsize == 0:
                            widget.text_fontsize = 10  # Default readable size
                            fontsize_to_use = 10
                            print(f"  ⚠ Fixed font size from {current_fontsize} to 10 for '{field_name}'")
                        else:
                            widget.text_fontsize = current_fontsize
                            fontsize_to_use = current_fontsize
                        
                        # Ensure text is visible
                        widget.text_color = (0, 0, 0)  # Black text
                        
                        # Update the widget
                        widget.update()
                        
                        # Method 2: ALSO draw text directly on the page (guaranteed visibility)
                        # This ensures the text is visible even if widget appearance fails
                        # Add small padding to position text nicely in the field
                        text_x = rect.x0 + 2
                        text_y = rect.y0 + (rect.height / 2) + (fontsize_to_use / 3)
                        
                        # Draw the text directly on the page
                        page.insert_text(
                            (text_x, text_y),
                            value,
                            fontsize=fontsize_to_use,
                            color=(0, 0, 0),  # Black
                            fontname="helv",  # Helvetica (built-in font)
                        )
                        
                        filled_count += 1
                        print(f"✓ Page {page_num + 1}: Filled '{field_name}' = '{value}' (fontsize: {fontsize_to_use}, drawn at {text_x:.1f}, {text_y:.1f})")
        
        if filled_count == 0:
            print(f"⚠ Warning: No fields were filled. Check if field names match.")
            print(f"  Expected fields: {list(values.keys())}")
        
        # Save with proper settings
        output_bytes = doc.tobytes(
            garbage=4,  # Maximum garbage collection
            deflate=True,  # Compress
            clean=True  # Clean up unused objects
        )
        doc.close()
        
        print(f"✓ Total fields filled: {filled_count}/{len(values)}")
        print(f"✓ Text drawn directly on PDF for guaranteed visibility")
        return output_bytes
        
    except Exception as e:
        print(f"✗ Error filling PDF: {e}")
        import traceback
        print(traceback.format_exc())
        raise




