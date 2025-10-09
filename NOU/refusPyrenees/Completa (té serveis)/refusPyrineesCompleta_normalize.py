import json

# Read the original JSON file
input_file = r"c:\Users\jordi\Desktop\UNI\TFG\INFO\NOU\refusPyrenees\Completa (té serveis)\refusPyrineesCompleta.json"
output_file = r"c:\Users\jordi\Desktop\UNI\TFG\INFO\NOU\refusPyrenees\Completa (té serveis)\refusPyrineesComp_norm.json"

# Load the data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total d'elements originals: {len(data)}")

# Filter out elements with type "Ruine" or "Refuge gardé toute l'année"
# Also remove the "ideerando" field from all elements
filtered_data = []
removed_count = 0

for item in data:
    if isinstance(item, dict):
        item_type = item.get('type', '')
        if item_type not in ["Ruine", "Refuge gardé toute l'année"]:
            # Create a copy of the item without the "ideerando" field
            filtered_item = {key: value for key, value in item.items() if key != 'ideerando'}
            filtered_data.append(filtered_item)
        else:
            removed_count += 1
            print(f"Eliminat: {item.get('name', 'sense nom')} - Tipus: {item_type}")
    else:
        # Keep non-dictionary items (shouldn't happen in this case)
        filtered_data.append(item)

print(f"\nElements eliminats: {removed_count}")
print(f"Elements restants: {len(filtered_data)}")

# Save the filtered data to the new file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)

print(f"\nFitxer creat: {output_file}")

# Verify the transformations
print("\nVerificació de les transformacions:")
print(f"1. Eliminació d'elements amb type='Ruine' o 'Refuge gardé toute l'année': {removed_count} eliminats ✓")
print(f"2. Eliminació del camp 'ideerando': ✓")

# Check if ideerando was successfully removed
has_ideerando = any('ideerando' in item for item in filtered_data if isinstance(item, dict))
print(f"3. Camp 'ideerando' completament eliminat: {'✗' if has_ideerando else '✓'}")

# Verify the filtering by counting types in the new file
from collections import Counter
types = [item.get('type', '') for item in filtered_data if isinstance(item, dict)]
type_counts = Counter(types)

print("\nTipus restants:")
for type_name, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
    if type_name.strip():
        print(f"  {type_name}: {count}")
    else:
        print(f"  [Buit/Null]: {count}")

# Show sample of first transformed element
if filtered_data:
    print(f"\nMostra del primer element transformat:")
    sample_keys = list(filtered_data[0].keys()) if isinstance(filtered_data[0], dict) else []
    print(f"- Camps disponibles: {', '.join(sample_keys[:10])}{'...' if len(sample_keys) > 10 else ''}")
    print(f"- NO té 'ideerando': {'ideerando' not in sample_keys}")
    print(f"- Valor de 'type': {filtered_data[0].get('type', 'N/A') if isinstance(filtered_data[0], dict) else 'N/A'}")