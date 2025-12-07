def suggest_mapping(label_text):
    """
    Suggests entity_type and property_name based on label text.
    Returns (source, entity_type, property_name)
    """
    label = label_text.upper().strip()
    
    # Mapping rules
    rules = {
        "ID NUMBER": ("Person", "id_number"),
        "ID NO": ("Person", "id_number"),
        "FIRST NAME": ("Person", "first_name"),
        "LAST NAME": ("Person", "last_name"),
        "SURNAME": ("Person", "last_name"),
        "EMAIL": ("Person", "email"),
        "EMAIL ADDRESS": ("Person", "email"),
        "PHONE": ("Person", "phone"),
        "PHONE NUMBER": ("Person", "phone"),
        "MOBILE": ("Person", "phone"),
        "ADDRESS": ("Person", "address"),
        "STREET ADDRESS": ("Person", "address"),
        "PARENT ADDRESS": ("Parent", "address"),
        "PARENT NAME": ("Parent", "name"),
        "EMPLOYEE ID": ("Employee", "employee_id"),
        "EMPLOYEE NUMBER": ("Employee", "employee_id"),
    }
    
    # Check for exact matches first
    if label in rules:
        entity, prop = rules[label]
        return "graphdb", entity, prop
    
    # Check for partial matches
    for key, (entity, prop) in rules.items():
        if key in label:
            return "graphdb", entity, prop
            
    return "manual", None, None
