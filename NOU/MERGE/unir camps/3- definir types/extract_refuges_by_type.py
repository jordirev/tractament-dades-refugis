import json

def extract_refuges_by_type(json_file_path, target_types):
    """
    Extract refuge names that have specific type values
    """
    results = {type_val: [] for type_val in target_types}
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        for item in data:
            if 'type' in item and 'name' in item:
                type_value = item['type']
                name = item['name']
                
                # Handle different type formats
                if isinstance(type_value, list):
                    for t in type_value:
                        if t in target_types:
                            results[t].append(name)
                elif isinstance(type_value, str):
                    if type_value in target_types:
                        results[type_value].append(name)
                elif type_value is None or type_value == "":
                    if "" in target_types:
                        results[""].append(name)
    
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return {}
    
    return results

def main():
    json_file = "data_refugis_updated_altitudes.json"
    output_file = "refugis_tipus_especifics.txt"
    
    # Target types to search for
    target_types = ["cabane fermee", "Fermée", "Détruite", ""]
    
    print("Extracting refuges with specific type values...")
    results = extract_refuges_by_type(json_file, target_types)
    
    # Count total refuges found
    total_count = sum(len(refuges) for refuges in results.values())
    
    print(f"Found {total_count} refuges with the specified type values")
    
    # Write to text file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("NOMS DELS REFUGIS AMB TIPUS ESPECÍFICS\n")
        file.write("=" * 50 + "\n\n")
        file.write(f"Total refugis trobats: {total_count}\n\n")
        
        for type_value in target_types:
            refuges = results[type_value]
            type_display = type_value if type_value else "(buit)"
            
            file.write(f"TIPUS: '{type_display}' ({len(refuges)} refugis)\n")
            file.write("-" * 40 + "\n")
            
            if refuges:
                for i, name in enumerate(sorted(refuges), 1):
                    file.write(f"{i:3d}. {name}\n")
            else:
                file.write("Cap refugi trobat amb aquest tipus.\n")
            
            file.write("\n")
    
    print(f"Results saved to {output_file}")
    
    # Also print to console
    print("\nRefuges found by type:")
    for type_value in target_types:
        refuges = results[type_value]
        type_display = type_value if type_value else "(buit)"
        print(f"\n'{type_display}' ({len(refuges)} refugis):")
        
        if refuges:
            for i, name in enumerate(sorted(refuges), 1):
                print(f"  {i:3d}. {name}")
        else:
            print("  Cap refugi trobat amb aquest tipus.")

if __name__ == "__main__":
    main()