import json
import re

def extract_refuge_names_from_txt(txt_file_path):
    """Extract refuge names from the text file"""
    refuge_names = []
    
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Pattern to match refuge names (lines that start with a number and a dot)
    pattern = r'^\s*\d+\.\s+(.+)$'
    
    for line in content.split('\n'):
        match = re.match(pattern, line)
        if match:
            refuge_name = match.group(1).strip()
            refuge_names.append(refuge_name)
            print(f"Found refuge: {refuge_name}")
    
    return refuge_names

def remove_refuges_from_json(json_file_path, refuge_names_to_remove):
    """Remove refuges from JSON file that match the names in the list"""
    
    # Load the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        refuges = json.load(file)
    
    print(f"Original number of refuges: {len(refuges)}")
    
    # Create a filtered list
    filtered_refuges = []
    removed_count = 0
    
    for refuge in refuges:
        refuge_name = refuge.get('name', '')
        
        # Check if this refuge should be removed
        should_remove = False
        for name_to_remove in refuge_names_to_remove:
            if refuge_name == name_to_remove:
                should_remove = True
                print(f"Removing: {refuge_name}")
                removed_count += 1
                break
        
        if not should_remove:
            filtered_refuges.append(refuge)
    
    print(f"Refuges removed: {removed_count}")
    print(f"Remaining refuges: {len(filtered_refuges)}")
    
    # Save the filtered JSON to a new file
    output_file = json_file_path.replace('.json', '_filtered.json')
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filtered_refuges, file, ensure_ascii=False, indent=2)
    
    print(f"Filtered data saved to: {output_file}")
    return filtered_refuges

def main():
    # File paths
    txt_file = "refugisPyrinees_refus_guardats.txt"
    json_file = "refusPyrinees_merged.json"
    
    # Extract refuge names from the text file
    print("Extracting refuge names from text file...")
    refuge_names_to_remove = extract_refuge_names_from_txt(txt_file)
    
    print(f"\nFound {len(refuge_names_to_remove)} refuges to remove:")
    for name in refuge_names_to_remove:
        print(f"  - {name}")
    
    # Remove these refuges from the JSON file
    print("\nRemoving refuges from JSON file...")
    filtered_refuges = remove_refuges_from_json(json_file, refuge_names_to_remove)

if __name__ == "__main__":
    main()