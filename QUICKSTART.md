# 🚀 QUICK START GUIDE

## Start the Server

```bash
uvicorn app.main:app --reload
```

Server runs at: **http://127.0.0.1:8000**

## Access API Documentation

Open in browser: **http://127.0.0.1:8000/docs**

---

## 📝 5-Step Testing Workflow

### STEP 1: Upload PDF Template
**POST /templates**

- Click "Try it out"
- Upload a fillable PDF
- `template_name`: "Test Form"
- `tenant_id`: "tenant_001"
- Click "Execute"
- **Note the `id` from response** (e.g., 1)

---

### STEP 2: View Fields
**GET /templates/{template_id}/fields**

- Enter `template_id`: 1
- Click "Execute"
- See all extracted fields and their mappings

---

### STEP 3: Update Mappings (Optional)
**POST /templates/{template_id}/fields/mapping**

Request body:
```json
{
  "fields": [
    {"field_name": "id_number", "source": "graphdb"},
    {"field_name": "comments", "source": "manual"}
  ]
}
```

---

### STEP 4: Open Form (Auto-fill)
**POST /forms/open**

Request body:
```json
{
  "template_id": 1,
  "graph_keys": {
    "person_id": "P123"
  },
  "existing_manual_values": {}
}
```

Response shows:
- `auto_filled_values`: Data from GraphDB (or mock)
- `manual_fields`: Fields user must fill
- `unlocked_graph_fields`: Fields not yet locked

---

### STEP 5: Submit Form (Get PDF)
**POST /forms/submit**

Request body:
```json
{
  "template_id": 1,
  "graph_keys": {
    "person_id": "P123"
  },
  "final_values": {
    "id_number": "P123456789",
    "first_name": "John",
    "email": "john@example.com",
    "comments": "Test submission"
  }
}
```

Click "Download file" to get the filled PDF!

---

## 🎯 Key Features

### Auto-Mapping Rules
| Label Contains | Maps To |
|----------------|---------|
| ID NUMBER | Person.id_number |
| FIRST NAME | Person.first_name |
| EMAIL | Person.email |
| PHONE | Person.phone |
| PARENT ADDRESS | Parent.address |

### Locking System
- Default threshold: **2 submissions**
- After threshold: Field auto-fills from GraphDB
- Admin can always override mappings

### Mock Data (No Neo4j needed)
The system works without Neo4j using mock data:
- Person.id_number → "P123456789"
- Person.first_name → "John"
- Person.email → "john.doe@example.com"

---

## 🔍 Terminal Logs

Watch the terminal for detailed logs:
- ✓ Success messages
- ⚠ Warnings
- ✗ Errors
- 📊 Mock data usage
- 🔒 Field locking events

---

## 📁 Files Created

- `sql_app.db` - SQLite database
- `uploaded_pdfs/` - PDF storage
- Server logs in terminal

---

## 🐛 Common Issues

**500 Error on upload:**
- Check PDF is a valid fillable form
- See terminal for detailed error

**No fields extracted:**
- PDF must have AcroForm fields
- Try a different PDF

**Neo4j warning:**
- Normal! System uses mock data
- To use real Neo4j, set environment variables

---

## 📚 Full Documentation

See `README.md` for complete documentation.

---

**Ready to test!** Open http://127.0.0.1:8000/docs and follow Step 1!
