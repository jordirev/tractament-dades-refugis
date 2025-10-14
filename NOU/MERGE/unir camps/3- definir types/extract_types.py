import json
from collections import Counter

def extract_types_from_json(json_file_path):
    """
    Extract all unique values from the 'type' field in the JSON file
    """
    types = []
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        for item in data:
            if 'type' in item:
                type_value = item['type']
                # Handle both string and list types
                if isinstance(type_value, list):
                    types.extend(type_value)
                elif isinstance(type_value, str):
                    types.append(type_value)
                elif type_value is not None:
                    types.append(str(type_value))
    
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return []
    
    return types

def main():
    json_file = "data_refugis_updated_altitudes.json"
    output_file = "valors_camp_type.txt"
    
    print("Extracting types from JSON file...")
    all_types = extract_types_from_json(json_file)
    
    # Get unique types and count occurrences
    unique_types = list(set(all_types))
    type_counts = Counter(all_types)
    
    # Sort alphabetically
    unique_types.sort()
    
    print(f"Found {len(unique_types)} unique type values")
    print(f"Total type entries: {len(all_types)}")
    
    # Write to text file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("VALORS DEL CAMP 'TYPE' EN EL FITXER data_refugis_updated_altitudes.json\n")
        file.write("=" * 60 + "\n\n")
        file.write(f"Total valors únics: {len(unique_types)}\n")
        file.write(f"Total entrades: {len(all_types)}\n\n")
        file.write("LLISTA DE VALORS ÚNICS (ordenats alfabèticament):\n")
        file.write("-" * 50 + "\n")
        
        for i, type_value in enumerate(unique_types, 1):
            count = type_counts[type_value]
            file.write(f"{i:3d}. {type_value} (apareix {count} vegades)\n")
        
        file.write("\n" + "=" * 60 + "\n")
        file.write("RESUM PER FREQÜÈNCIA:\n")
        file.write("-" * 20 + "\n")
        
        # Sort by frequency (most common first)
        for type_value, count in type_counts.most_common():
            file.write(f"{type_value}: {count}\n")
    
    print(f"Results saved to {output_file}")
    
    # Also print the unique types to console
    print("\nUnique type values found:")
    for i, type_value in enumerate(unique_types, 1):
        count = type_counts[type_value]
        print(f"{i:3d}. {type_value} (apareix {count} vegades)")

if __name__ == "__main__":
    main()