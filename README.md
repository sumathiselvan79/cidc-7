# 📄 PDF Template Service

A comprehensive backend service for managing PDF templates with intelligent field mapping to GraphDB (Neo4j) and automated form filling.

## 🚀 Quick Start

### 1. Start the Server

```bash
.\run.bat
```

Or manually:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Access the API

- **Swagger UI**: http://127.0.0.1:8000/docs
- **API Root**: http://127.0.0.1:8000

## 📋 Complete Testing Workflow

### Step 1: Upload a PDF Template

**Endpoint**: `POST /templates`

1. Open http://127.0.0.1:8000/docs
2. Click on **POST /templates**
3. Click **"Try it out"**
4. Fill in:
   - `file`: Upload a fillable PDF
   - `template_name`: "Registration Form"
   - `tenant_id`: "tenant_001"
5. Click **Execute**

**Response Example**:
```json
{
  "id": 1,
  "tenant_id": "tenant_001",
  "template_hash": "abc123...",
  "template_name": "Registration Form",
  "confirm_threshold": 2,
  "fields": [
    {
      "id": 1,
      "template_id": 1,
      "field_name": "id_number",
      "label_text": "ID NUMBER",
      "source": "graphdb",
      "entity_type": "Person",
      "property_name": "id_number",
      "confirm_count": 0,
      "is_locked": false
    }
  ]
}
```

### Step 2: View Field Mappings

**Endpoint**: `GET /templates/{template_id}/fields`

1. Click on **GET /templates/{template_id}/fields**
2. Enter `template_id`: `1`
3. Click **Execute**

This shows all extracted fields and their auto-suggested mappings.

### Step 3: Update Mappings (Optional)

**Endpoint**: `POST /templates/{template_id}/fields/mapping`

If you want to change field mappings:

```json
{
  "fields": [
    {"field_name": "id_number", "source": "graphdb"},
    {"field_name": "comments", "source": "manual"}
  ]
}
```

### Step 4: Open a Form

**Endpoint**: `POST /forms/open`

```json
{
  "template_id": 1,
  "graph_keys": {
    "person_id": "P123"
  },
  "existing_manual_values": {}
}
```

**Response**:
```json
{
  "template_id": 1,
  "template_name": "Registration Form",
  "auto_filled_values": {
    "id_number": "P123456789",
    "first_name": "John",
    "email": "john.doe@example.com"
  },
  "manual_fields": [
    {
      "field_name": "comments",
      "label_text": "COMMENTS"
    }
  ],
  "unlocked_graph_fields": []
}
```

### Step 5: Submit Form

**Endpoint**: `POST /forms/submit`

```json
{
  "template_id": 1,
  "graph_keys": {
    "person_id": "P123"
  },
  "final_values": {
    "id_number": "P123456789",
    "first_name": "John",
    "email": "john.doe@example.com",
    "comments": "Test submission"
  }
}
```

**Response**: Downloads the filled PDF file

## 🎯 Features

### Automatic Field Detection
- Extracts AcroForm fields from PDFs
- Intelligently detects field labels using spatial analysis
- Supports various PDF form formats

### Smart Mapping Engine
Auto-suggests GraphDB mappings based on field labels:

| Label Pattern | Entity | Property |
|--------------|--------|----------|
| ID NUMBER | Person | id_number |
| FIRST NAME | Person | first_name |
| EMAIL | Person | email |
| PHONE | Person | phone |
| PARENT ADDRESS | Parent | address |
| EMPLOYEE ID | Employee | employee_id |

### Confirmation & Locking System
- **Threshold-based locking**: Fields lock after N successful uses
- **Auto-fill locked fields**: Locked fields automatically fetch from GraphDB
- **Manual override**: Admin can always change mappings

### GraphDB Integration
- **Neo4j support**: Full integration with Neo4j graph database
- **Mock data fallback**: Works without Neo4j for testing
- **Flexible queries**: Supports multiple entity types

## 📁 Project Structure

```
pdfproject/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── routers/
│   │   ├── templates.py     # Template endpoints
│   │   └── forms.py         # Form endpoints
│   └── services/
│       ├── pdf_service.py   # PDF operations
│       ├── graph_service.py # Neo4j integration
│       └── mapping_service.py # Mapping rules
├── uploaded_pdfs/           # PDF storage
├── requirements.txt         # Dependencies
├── run.bat                  # Quick start script
└── README.md               # This file
```

## ⚙️ Configuration

### Environment Variables (Optional)

Create a `.env` file:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

### Database

- **Type**: SQLite (auto-created as `sql_app.db`)
- **Tables**: `templates`, `field_mappings`
- **Auto-migration**: Tables created on startup

## 🔧 API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/templates` | Upload PDF template |
| GET | `/templates/{id}/fields` | View field mappings |
| POST | `/templates/{id}/fields/mapping` | Update mappings |
| POST | `/forms/open` | Open form (auto-fill) |
| POST | `/forms/submit` | Submit form (get PDF) |
| GET | `/` | API information |
| GET | `/health` | Health check |

## 🧪 Testing Without a Real PDF

If you don't have a fillable PDF, you can create one using:
- Adobe Acrobat Pro
- LibreOffice Writer (Export as PDF with form fields)
- Online PDF form creators

Or use the mock data mode which works with any PDF structure.

## 📊 How It Works

### 1. Template Upload Flow
```
Upload PDF → Calculate Hash → Check Duplicates → Extract Fields → 
Auto-Suggest Mappings → Store in Database
```

### 2. Form Open Flow
```
Load Template → Partition Fields (Locked/Unlocked/Manual) → 
Fetch Locked Fields from GraphDB → Return Auto-filled Data
```

### 3. Form Submit Flow
```
Receive Values → Update Confirmation Counts → Lock Fields if Threshold Met → 
Fill PDF → Return Filled Document
```

### 4. Locking Mechanism
```
Field Used → confirm_count++ → 
If confirm_count >= threshold → is_locked = TRUE → 
Future Opens Auto-fill from GraphDB
```

## 🐛 Troubleshooting

### Server won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### PDF fields not detected
- Ensure PDF has AcroForm fields (not XFA or static text)
- Test with Adobe Acrobat fillable forms
- Check terminal logs for extraction errors

### Neo4j connection fails
- Service automatically falls back to mock data
- Check Neo4j is running: `neo4j status`
- Verify credentials in environment variables

### 500 Internal Server Error
- Check terminal logs for detailed error messages
- Ensure uploaded file is a valid PDF
- Verify database file permissions

## 📝 Example Use Cases

### 1. School Registration Forms
- Auto-fill student ID, name, parent details from database
- Manual fields: Emergency contact, special requirements
- Lock common fields after 2 successful submissions

### 2. Employee Onboarding
- Auto-fill employee ID, department, manager from HR system
- Manual fields: Bank details, emergency contacts
- Progressive locking as forms are verified

### 3. Medical Forms
- Auto-fill patient ID, demographics from EHR
- Manual fields: Current symptoms, medications
- Ensure data consistency across visits

## 🎓 Advanced Features

### Custom Mapping Rules

Edit `app/services/mapping_service.py` to add custom rules:

```python
rules = {
    "STUDENT ID": ("Student", "student_id"),
    "GRADE": ("Student", "grade_level"),
    # Add your custom mappings
}
```

### Adjust Confirmation Threshold

Default is 2. Change in database or via API:

```python
# In models.py
confirm_threshold = Column(Integer, default=3)  # Change to 3
```

### Add More Entity Types

Extend `graph_service.py` mock data:

```python
elif entity_type == 'Student':
    if prop_name == 'student_id':
        results[field_name] = 'STU-2024-001'
```

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Support

- **Documentation**: http://127.0.0.1:8000/docs
- **Issues**: Check terminal logs for detailed error messages
- **Questions**: Review code comments in `app/` directory

---

**Made with ❤️ using FastAPI, SQLAlchemy, PyMuPDF, and Neo4j**
