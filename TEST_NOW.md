# 🎯 EXACT STEPS TO TEST RIGHT NOW

## ✅ Good News: You Already Have a Template!

Template ID: **1** exists in your database.

---

## 📋 TEST EACH ENDPOINT (Copy & Paste These)

### **1. View Template Fields**

**Endpoint**: `GET /templates/1/fields`

Just click Execute - no body needed!

---

### **2. Open Form (Auto-fill)**

**Endpoint**: `POST /forms/open`

**Copy this JSON** into the request body:

```json
{
  "template_id": 1,
  "graph_keys": {
    "person_id": "P123"
  },
  "existing_manual_values": {}
}
```

**Expected Response**:
```json
{
  "template_id": 1,
  "template_name": "...",
  "auto_filled_values": {
    "id_number": "P123456789",
    "first_name": "John",
    "email": "john.doe@example.com"
  },
  "manual_fields": [...],
  "unlocked_graph_fields": [...]
}
```

---

### **3. Submit Form (Get Filled PDF)**

**Endpoint**: `POST /forms/submit`

**Copy this JSON** into the request body:

```json
{
  "template_id": 1,
  "graph_keys": {
    "person_id": "P123"
  },
  "final_values": {
    "id_number": "P123456789",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0123",
    "address": "123 Main Street",
    "comments": "Test submission"
  }
}
```

**Expected Response**: PDF file download

---

## 🚨 IMPORTANT: Change template_id from 0 to 1

You keep using:
```json
{
  "template_id": 0,  ❌ WRONG - This doesn't exist!
```

You should use:
```json
{
  "template_id": 1,  ✅ CORRECT - This exists!
```

---

## 🔍 If You Want to Upload a NEW Template

**Endpoint**: `POST /templates`

1. Click "Try it out"
2. **file**: Choose `Patient Registration Form Template-1.pdf`
3. **template_name**: "Patient Form"
4. **tenant_id**: "tenant_001"
5. Click Execute

This will create template ID 2 (or higher).

---

## 📊 Quick Database Check

Current templates in database:
- **ID: 1** - Already exists ✅

Use this ID in all your tests!

---

## ✅ DO THIS NOW:

1. Go to **POST /forms/open**
2. Click "Try it out"
3. **Replace the entire request body** with:
   ```json
   {
     "template_id": 1,
     "graph_keys": {
       "person_id": "P123"
     },
     "existing_manual_values": {}
   }
   ```
4. Click **Execute**
5. You should see auto-filled values! 🎉

---

**The key is: Use template_id = 1, not 0!**
