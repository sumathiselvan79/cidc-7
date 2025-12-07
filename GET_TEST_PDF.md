# 📄 How to Get a Test PDF

## Option 1: Use an Existing PDF
If you have any fillable PDF form (like tax forms, registration forms, etc.), you can use that directly!

## Option 2: Create One Online
Use free online tools:
- **PDFescape**: https://www.pdfescape.com/
- **JotForm PDF Editor**: https://www.jotform.com/pdf-editor/
- **Adobe Acrobat Online**: https://www.adobe.com/acrobat/online/edit-pdf.html

## Option 3: Use LibreOffice
1. Create a document in LibreOffice Writer
2. Insert → Form Controls → Text Box
3. Add multiple form fields
4. File → Export as PDF
5. Check "Create PDF Form"

## Option 4: Download Sample Forms
Search for "fillable PDF form template" online. Many free templates available.

## What the PDF Needs
- **AcroForm fields** (standard PDF form fields)
- Field names (automatically assigned)
- Optional: Field labels nearby for better auto-mapping

## Testing Without a PDF
The API will work with any PDF, but won't extract fields if the PDF doesn't have form fields. You can still test the endpoints with an empty fields array.

---

**Once you have a PDF**, upload it using:
- Swagger UI: http://127.0.0.1:8000/docs
- POST /templates endpoint
