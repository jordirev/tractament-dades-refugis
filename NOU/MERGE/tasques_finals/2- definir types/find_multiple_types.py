import json

def find_refuges_with_multiple_types(json_file_path):
    """
    Find refuges that have multiple type values (when type is a list with more than one element)
    """
    refuges_with_multiple_types = []
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        for item in data:
            if 'type' in item and 'name' in item:
                type_value = item['type']
                name = item['name']
                
                # Check if type is a list with more than one element
                if isinstance(type_value, list) and len(type_value) > 1:
                    refuges_with_multiple_types.append({
                        'name': name,
                        'types': type_value,
                        'type_count': len(type_value)
                    })
    
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return []
    
    return refuges_with_multiple_types

def main():
    json_file = "data_refugis_updated_altitudes.json"
    output_file = "refugis_amb_multiples_tipus.txt"
    
    print("Searching for refuges with multiple types...")
    refuges_with_multiple = find_refuges_with_multiple_types(json_file)
    
    # Sort by name for better readability
    refuges_with_multiple.sort(key=lambda x: x['name'])
    
    print(f"Found {len(refuges_with_multiple)} refuges with multiple types")
    
    # Write to text file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("REFUGIS AMB MÚLTIPLES TIPUS\n")
        file.write("=" * 50 + "\n\n")
        file.write(f"Total refugis amb múltiples tipus: {len(refuges_with_multiple)}\n\n")
        
        if refuges_with_multiple:
            file.write("LLISTA DETALLADA:\n")
            file.write("-" * 40 + "\n")
            
            for i, refuge in enumerate(refuges_with_multiple, 1):
                file.write(f"{i:3d}. {refuge['name']}\n")
                file.write(f"     Nombre de tipus: {refuge['type_count']}\n")
                file.write(f"     Tipus:\n")
                for j, type_val in enumerate(refuge['types'], 1):
                    type_display = type_val if type_val else "(buit)"
                    file.write(f"       {j}. {type_display}\n")
                file.write("\n")
            
            # Summary by number of types
            file.write("\n" + "=" * 50 + "\n")
            file.write("RESUM PER NOMBRE DE TIPUS:\n")
            file.write("-" * 30 + "\n")
            
            type_count_summary = {}
            for refuge in refuges_with_multiple:
                count = refuge['type_count']
                if count not in type_count_summary:
                    type_count_summary[count] = 0
                type_count_summary[count] += 1
            
            for count in sorted(type_count_summary.keys()):
                file.write(f"Refugis amb {count} tipus: {type_count_summary[count]}\n")
            
            # Summary of all unique type combinations
            file.write("\n" + "=" * 50 + "\n")
            file.write("COMBINACIONS DE TIPUS TROBADES:\n")
            file.write("-" * 35 + "\n")
            
            type_combinations = {}
            for refuge in refuges_with_multiple:
                combo = tuple(sorted(refuge['types']))
                if combo not in type_combinations:
                    type_combinations[combo] = []
                type_combinations[combo].append(refuge['name'])
            
            for i, (combo, names) in enumerate(sorted(type_combinations.items()), 1):
                file.write(f"{i}. Combinació: {' + '.join([t if t else '(buit)' for t in combo])}\n")
                file.write(f"   Refugis amb aquesta combinació ({len(names)}):\n")
                for name in sorted(names):
                    file.write(f"   - {name}\n")
                file.write("\n")
        else:
            file.write("No s'han trobat refugis amb múltiples tipus.\n")
            file.write("Tots els refugis tenen un sol tipus o cap tipus assignat.\n")
    
    print(f"Results saved to {output_file}")
    
    # Also print summary to console
    if refuges_with_multiple:
        print(f"\nRefuges with multiple types found:")
        for refuge in refuges_with_multiple:
            print(f"  - {refuge['name']} ({refuge['type_count']} tipus: {', '.join([t if t else '(buit)' for t in refuge['types']])})")
    else:
        print("\nNo refuges with multiple types found.")
        print("All refuges have either a single type or no type assigned.")

if __name__ == "__main__":
    main()