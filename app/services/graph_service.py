import os

class GraphService:
    """
    GraphDB service with mock data fallback.
    Connects to Neo4j if available, otherwise uses mock data.
    """
    
    def __init__(self):
        self.driver = None
        # Try to import and connect to Neo4j
        try:
            from neo4j import GraphDatabase
            uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
            user = os.getenv("NEO4J_USER", "neo4j")
            password = os.getenv("NEO4J_PASSWORD", "password")
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            print("✓ Connected to Neo4j")
        except Exception as e:
            print(f"⚠ Neo4j not available, using mock data: {e}")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def fetch_values(self, mappings, graph_keys):
        """
        Fetch values from GraphDB or mock data.
        
        Args:
            mappings: list of dicts with entity_type, property_name, field_name
            graph_keys: dict of {key_name: id_value}
        
        Returns:
            dict of {field_name: value}
        """
        if not self.driver:
            return self._get_mock_data(mappings)

        results = {}
        
        try:
            with self.driver.session() as session:
                for m in mappings:
                    entity_type = m.get('entity_type')
                    prop_name = m.get('property_name')
                    field_name = m.get('field_name')
                    
                    if not entity_type or not prop_name:
                        continue
                    
                    # Determine the key to use from graph_keys
                    key_field = f"{entity_type.lower()}_id"
                    if key_field not in graph_keys:
                        continue
                        
                    id_value = graph_keys[key_field]
                    
                    # Query Neo4j
                    query = f"MATCH (n:{entity_type} {{id: $id}}) RETURN n.{prop_name} as val"
                    result = session.run(query, id=id_value)
                    record = result.single()
                    
                    if record and record["val"]:
                        results[field_name] = record["val"]
        except Exception as e:
            print(f"Error querying Neo4j: {e}")
            return self._get_mock_data(mappings)
                    
        return results

    def _get_mock_data(self, mappings):
        """
        Returns mock data for testing without Neo4j.
        """
        print("📊 Using mock GraphDB data")
        results = {}
        
        for m in mappings:
            entity_type = m.get('entity_type')
            prop_name = m.get('property_name')
            field_name = m.get('field_name')
            
            # Mock data based on entity type and property
            if entity_type == 'Person':
                if prop_name == 'id_number':
                    results[field_name] = 'P123456789'
                elif prop_name == 'first_name':
                    results[field_name] = 'John'
                elif prop_name == 'last_name':
                    results[field_name] = 'Doe'
                elif prop_name == 'email':
                    results[field_name] = 'john.doe@example.com'
                elif prop_name == 'phone':
                    results[field_name] = '+1-555-0123'
                elif prop_name == 'address':
                    results[field_name] = '123 Main Street, City, State 12345'
                    
            elif entity_type == 'Parent':
                if prop_name == 'address':
                    results[field_name] = '456 Oak Avenue, Town, State 67890'
                elif prop_name == 'name':
                    results[field_name] = 'Jane Doe'
                    
            elif entity_type == 'Employee':
                if prop_name == 'employee_id':
                    results[field_name] = 'EMP-2024-001'
                    
        return results
