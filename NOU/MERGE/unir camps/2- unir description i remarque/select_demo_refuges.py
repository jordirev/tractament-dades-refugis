import json
import random

def select_demo_refuges(input_file, output_file):
    """
    Selecciona 100 refugios variados con múltiples parámetros de info_comp a 1,
    variados en type, region, departement y places.
    Convierte arrays a valores únicos.
    """
    
    # Cargar el archivo JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        refuges = json.load(f)
    
    print(f"Total refugios cargados: {len(refuges)}")
    
    # Filtrar refugios con múltiples parámetros info_comp a 1
    filtered_refuges = []
    
    for refuge in refuges:
        if 'info_comp' in refuge and isinstance(refuge['info_comp'], dict):
            # Contar cuántos parámetros están a 1
            ones_count = sum(1 for value in refuge['info_comp'].values() if value == 1)
            
            # Solo refugios con al menos 3 parámetros a 1
            if ones_count >= 3:
                filtered_refuges.append(refuge)
    
    print(f"Refugios con al menos 3 parámetros info_comp a 1: {len(filtered_refuges)}")
    
    # Análisis de diversidad disponible
    types_set = set()
    regions_set = set()
    departments_set = set()
    places_ranges = {'0': [], '1-5': [], '6-15': [], '16+': []}
    
    for refuge in filtered_refuges:
        # Types
        if 'type' in refuge:
            if isinstance(refuge['type'], list):
                types_set.update(refuge['type'])
            else:
                types_set.add(refuge['type'])
        
        # Regions
        if 'region' in refuge and refuge['region']:
            regions_set.add(refuge['region'])
        
        # Departments  
        if 'departement' in refuge and refuge['departement']:
            departments_set.add(refuge['departement'])
        
        # Places
        places = refuge.get('places', 0)
        if places is None:
            places = 0
        
        if places == 0:
            places_ranges['0'].append(refuge)
        elif 1 <= places <= 5:
            places_ranges['1-5'].append(refuge)
        elif 6 <= places <= 15:
            places_ranges['6-15'].append(refuge)
        else:
            places_ranges['16+'].append(refuge)
    
    print(f"Types únicos disponibles: {len(types_set)}")
    print(f"Regions únicas disponibles: {len(regions_set)}")
    print(f"Departamentos únicos disponibles: {len(departments_set)}")
    print(f"Distribución por places: 0={len(places_ranges['0'])}, 1-5={len(places_ranges['1-5'])}, 6-15={len(places_ranges['6-15'])}, 16+={len(places_ranges['16+'])}")
    
    # Selección balanceada
    selected_refuges = []
    
    # Intentar conseguir 25 de cada rango de places
    target_per_range = 25
    
    for range_name, refuges_in_range in places_ranges.items():
        if len(refuges_in_range) >= target_per_range:
            selected_from_range = random.sample(refuges_in_range, target_per_range)
        else:
            selected_from_range = refuges_in_range
        
        selected_refuges.extend(selected_from_range)
        print(f"Seleccionados {len(selected_from_range)} refugios del rango de places '{range_name}'")
    
    # Si no tenemos 100, completar con refugios adicionales
    if len(selected_refuges) < 100:
        remaining_refuges = [r for r in filtered_refuges if r not in selected_refuges]
        additional_needed = min(100 - len(selected_refuges), len(remaining_refuges))
        if additional_needed > 0:
            additional_refuges = random.sample(remaining_refuges, additional_needed)
            selected_refuges.extend(additional_refuges)
    
    # Si tenemos más de 100, recortar aleatoriamente
    if len(selected_refuges) > 100:
        selected_refuges = random.sample(selected_refuges, 100)
    
    print(f"Total refugios seleccionados: {len(selected_refuges)}")
    
    # Procesar refugios para eliminar arrays y convertir a valores únicos
    processed_refuges = []
    
    for refuge in selected_refuges:
        processed_refuge = {}
        
        for key, value in refuge.items():
            if key in ['type', 'description', 'remarque'] and isinstance(value, list) and value:
                # Tomar el primer elemento no vacío
                processed_refuge[key] = next((item for item in value if item), value[0] if value else "")
            else:
                processed_refuge[key] = value
        
        processed_refuges.append(processed_refuge)
    
    # Análisis final de diversidad
    final_types = set()
    final_regions = set()
    final_departments = set()
    final_places_dist = {'0': 0, '1-5': 0, '6-15': 0, '16+': 0}
    
    for refuge in processed_refuges:
        # Types
        if 'type' in refuge and refuge['type']:
            final_types.add(refuge['type'])
        
        # Regions
        if 'region' in refuge and refuge['region']:
            final_regions.add(refuge['region'])
        
        # Departments
        if 'departement' in refuge and refuge['departement']:
            final_departments.add(refuge['departement'])
        
        # Places distribution
        places = refuge.get('places', 0)
        if places is None:
            places = 0
            
        if places == 0:
            final_places_dist['0'] += 1
        elif 1 <= places <= 5:
            final_places_dist['1-5'] += 1
        elif 6 <= places <= 15:
            final_places_dist['6-15'] += 1
        else:
            final_places_dist['16+'] += 1
    
    # Guardar el resultado
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_refuges, f, ensure_ascii=False, indent=2)
    
    print(f"\nResultado guardado en: {output_file}")
    print(f"\nDIVERSIDAD FINAL:")
    print(f"Types únicos: {len(final_types)} - {list(final_types)[:5]}...")
    print(f"Regions únicas: {len(final_regions)}")
    print(f"Departamentos únicos: {len(final_departments)}")
    print(f"Distribución final de places: {final_places_dist}")
    
    # Verificar info_comp
    info_comp_stats = {}
    for refuge in processed_refuges:
        if 'info_comp' in refuge:
            ones_count = sum(1 for value in refuge['info_comp'].values() if value == 1)
            info_comp_stats[ones_count] = info_comp_stats.get(ones_count, 0) + 1
    
    print(f"Distribución de parámetros info_comp a 1: {info_comp_stats}")

if __name__ == "__main__":
    input_file = "data_refugis_updated_altitudes.json"
    output_file = "demo_data_refugis.json"
    
    # Establecer semilla para reproducibilidad
    random.seed(42)
    
    select_demo_refuges(input_file, output_file)