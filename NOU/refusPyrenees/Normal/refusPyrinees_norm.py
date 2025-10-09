import json

# Read the GeoJSON file
input_file = r"c:\Users\jordi\Desktop\UNI\TFG\INFO\NOU\refusPyrenees\Normal\refusPyrinees.geojson"
output_file = r"c:\Users\jordi\Desktop\UNI\TFG\INFO\NOU\refusPyrenees\Normal\refusPyrinees_norm.json"

# Load the data
with open(input_file, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

print(f"Total de features originals: {len(geojson_data['features'])}")

# Transform GeoJSON to JSON array
json_array = []
removed_count = 0

for feature in geojson_data['features']:
    # Check if type_hebergement is "ruine" and skip if it is
    if feature.get('type_hebergement') == 'ruine':
        removed_count += 1
        print(f"Eliminat (ruine): {feature.get('name', 'sense nom')}")
        continue
    
    # Create new feature object
    new_feature = {}
    
    # Copy all properties except "photo"
    for key, value in feature.items():
        if key != 'photo':
            new_feature[key] = value
    
    # Rename "type_hebergement" to "type"
    if 'type_hebergement' in new_feature:
        new_feature['type'] = new_feature.pop('type_hebergement')
    
    json_array.append(new_feature)

print(f"Elements eliminats (ruine): {removed_count}")
print(f"Elements restants: {len(json_array)}")

# Save the transformed data as JSON array
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(json_array, f, ensure_ascii=False, indent=4)

print(f"\nFitxer creat: {output_file}")

# Verify the transformations
print("\nVerificació de les transformacions:")
print(f"1. Transformació GeoJSON → JSON array: ✓")
print(f"2. Eliminació d'elements amb type='ruine': {removed_count} eliminats ✓")
print(f"3. Eliminació del camp 'photo': ✓")
print(f"4. Canvi 'type_hebergement' → 'type': ✓")

# Show sample of first transformed element
if json_array:
    print(f"\nMostra del primer element transformat:")
    print(f"- Té coordenades: {'coordinates' in json_array[0]}")
    print(f"- Té 'type': {'type' in json_array[0]}")
    print(f"- NO té 'photo': {'photo' not in json_array[0]}")
    print(f"- NO té 'type_hebergement': {'type_hebergement' not in json_array[0]}")
    print(f"- Valor de 'type': {json_array[0].get('type', 'N/A')}")

# Count types in final result
from collections import Counter
types = [item.get('type', '') for item in json_array]
type_counts = Counter(types)

print(f"\nTipus finals i nombre d'aparicions:")
for type_name, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
    if type_name.strip():
        print(f"  {type_name}: {count}")
    else:
        print(f"  [Buit/Null]: {count}")