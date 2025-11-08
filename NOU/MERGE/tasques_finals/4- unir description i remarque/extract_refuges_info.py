import json

def extract_refuges_info(input_file, output_file):
    """
    Extrae solo los campos 'name', 'description' y 'remarque' de cada refugio
    """
    
    # Cargar el archivo JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        refuges = json.load(f)
    
    # Extraer solo los campos requeridos
    extracted_refuges = []
    
    for refuge in refuges:
        extracted_refuge = {}
        
        # Nombre del refugio (campo obligatorio)
        if 'name' in refuge:
            extracted_refuge['name'] = refuge['name']
        
        # Description (puede ser lista o string)
        if 'description' in refuge:
            extracted_refuge['description'] = refuge['description']
        
        # Remarque (puede ser lista o string) 
        if 'remarque' in refuge:
            extracted_refuge['remarque'] = refuge['remarque']
        
        extracted_refuges.append(extracted_refuge)
    
    # Guardar el resultado en un nuevo archivo JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(extracted_refuges, f, ensure_ascii=False, indent=2)
    
    print(f"Procesados {len(extracted_refuges)} refugios")
    print(f"Resultado guardado en: {output_file}")
    
    # Mostrar estadísticas
    with_description = sum(1 for r in extracted_refuges if 'description' in r and r['description'])
    with_remarque = sum(1 for r in extracted_refuges if 'remarque' in r and r['remarque'])
    
    print(f"Refugios con descripción: {with_description}")
    print(f"Refugios con remarque: {with_remarque}")

if __name__ == "__main__":
    input_file = "data_refugis_updated_altitudes.json"
    output_file = "refuges_name_description_remarque.json"
    
    extract_refuges_info(input_file, output_file)