import json

def process_refugis(input_file, output_file):
    """
    Processa el fitxer de refugis:
    1. Converteix info_comp de "mezzanine/etage" a "mezzanine_etage"
    2. "Processa la descripció per unir llistes en un únic string"
    """
    
    # Carregar el fitxer JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        refuges = json.load(f)
    
    print(f"Total de refugis a processar: {len(refuges)}")
    
    processed_refuges = []
    
    for i, refuge in enumerate(refuges, 1):
        # Crear una còpia del refugi sense remarque
        processed_refuge = {k: v for k, v in refuge.items() if k != 'remarque'}
        
        # 1. Convertir info_comp: clau "mezzanine/etage" -> "mezzanine_etage"
        if 'info_comp' in processed_refuge and processed_refuge['info_comp']:
            if isinstance(processed_refuge['info_comp'], dict):
                # Si la clau "mezzanine/etage" existeix, canviar-la per "mezzanine_etage"
                if 'mezzanine/etage' in processed_refuge['info_comp']:
                    processed_refuge['info_comp']['mezzanine_etage'] = processed_refuge['info_comp'].pop('mezzanine/etage')
        
        # 2. Convertir description de llista a valor únic
        if 'description' in processed_refuge:
            description = processed_refuge['description']
            
            # Si és una llista
            if isinstance(description, list):
                # Filtrar elements buits i convertir a strings
                valid_descriptions = [str(d).strip() for d in description if d and str(d).strip()]
                
                if valid_descriptions:
                    # Agafar la descripció més llarga
                    longest_description = max(valid_descriptions, key=len)
                    processed_refuge['description'] = longest_description
                else:
                    # Si no hi ha cap descripció vàlida, deixar string buit
                    processed_refuge['description'] = ''
            
            # Si ja és un string, deixar-lo tal qual
            elif isinstance(description, str):
                processed_refuge['description'] = description.strip()
            
            # Si és None o altre tipus, convertir a string buit
            else:
                processed_refuge['description'] = ''
        else:
            # Si no té camp description, afegir-lo buit
            processed_refuge['description'] = ''
        
        processed_refuges.append(processed_refuge)
        
        if (i % 100 == 0) or (i == len(refuges)):
            print(f"Processat {i}/{len(refuges)} refugis...")
    
    # Guardar el resultat
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_refuges, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Processament completat!")
    print(f"✓ Resultat guardat a: {output_file}")
    print(f"✓ Total refugis processats: {len(processed_refuges)}")
    
    # Estadístiques
    refuges_amb_description = sum(1 for r in processed_refuges if r.get('description'))
    refuges_sense_description = len(processed_refuges) - refuges_amb_description
    print(f"\nEstadístiques:")
    print(f"  - Refugis amb descripció: {refuges_amb_description}")
    print(f"  - Refugis sense descripció: {refuges_sense_description}")

if __name__ == "__main__":
    input_file = "data_refugis_sense_repetits.json"
    output_file = "data_refuges_description_merged.json"
    
    process_refugis(input_file, output_file)
