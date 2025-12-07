# 🧪 Quick Test - Copy & Paste This JSON

## For POST /forms/submit

Copy this JSON and paste it into the Swagger UI:

```json
{
  "template_id": 1,
  "graph_keys": {
    "person_id": "P123"
  },
  "final_values": {
    "Email": "test@example.com",
    "Address": "456 Oak Avenue",
    "City": "Boston",
    "State": "MA",
    "Apt": "Suite 100",
    "s Home Phone Number": "555-0123",
    "Alternate Phone Number": "555-0456"
  }
}
```

## Expected Result

✅ Download a PDF file
✅ Open the PDF
✅ See all the filled values clearly visible in the form fields

## Server Log Output You Should See

```
📝 Submitting form for template: Patient Registration Form Template-1
  ⚠ Fixed font size from 0 to 11 for 'Email'
✓ Page 1: Filled 'Email' = 'test@example.com' (fontsize: 11)
  ⚠ Fixed font size from 0 to 11 for 'Address'
✓ Page 1: Filled 'Address' = '456 Oak Avenue' (fontsize: 11)
  ⚠ Fixed font size from 0 to 11 for 'City'
✓ Page 1: Filled 'City' = 'Boston' (fontsize: 11)
  ⚠ Fixed font size from 0 to 11 for 'State'
✓ Page 1: Filled 'State' = 'MA' (fontsize: 11)
  ⚠ Fixed font size from 0 to 11 for 'Apt'
✓ Page 1: Filled 'Apt' = 'Suite 100' (fontsize: 11)
  ⚠ Fixed font size from 0 to 11 for 's Home Phone Number'
✓ Page 1: Filled 's Home Phone Number' = '555-0123' (fontsize: 11)
  ⚠ Fixed font size from 0 to 11 for 'Alternate Phone Number'
✓ Page 1: Filled 'Alternate Phone Number' = '555-0456' (fontsize: 11)
✓ Total fields filled: 7/7
✓ PDF filled successfully with 7 values
```

The `⚠ Fixed font size from 0 to 11` messages confirm the fix is working!

---

**Go to http://127.0.0.1:8000/docs and test it now!** 🚀
