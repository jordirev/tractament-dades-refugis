import json
from collections import Counter

# Llegir el fitxer actualitzat
with open('data_refugis_updated_types.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Analitzar els tipus finals
type_counter = Counter()
refugis_amb_array = []
refugis_amb_string = []
refugis_sense_type = []

for refugi in data:
    type_field = refugi.get('type')
    
    if type_field is None or type_field == '':
        refugis_sense_type.append(refugi.get('name', 'Sense nom'))
    elif isinstance(type_field, list):
        refugis_amb_array.append({
            'name': refugi.get('name', 'Sense nom'),
            'types': type_field
        })
        # Comptar els tipus individuals de l'array
        for t in type_field:
            type_counter[f"[ARRAY] {t}"] += 1
    elif isinstance(type_field, str):
        refugis_amb_string.append(refugi.get('name', 'Sense nom'))
        type_counter[type_field] += 1

print("VERIFICACIÓ DEL FITXER data_refugis_updated_types.json")
print("=" * 70)
print(f"\nTotal de refugis: {len(data)}")
print(f"Refugis amb type com a string: {len(refugis_amb_string)}")
print(f"Refugis amb type com a array: {len(refugis_amb_array)}")
print(f"Refugis sense type o type buit: {len(refugis_sense_type)}")

print("\n" + "=" * 70)
print("VALORS ÚNICS DEL CAMP 'TYPE':")
print("-" * 70)
for type_val, count in type_counter.most_common():
    print(f"  {type_val}: {count}")

if refugis_amb_array:
    print("\n" + "=" * 70)
    print("ATENCIÓ! Refugis que encara tenen type com a ARRAY:")
    print("-" * 70)
    for refugi in refugis_amb_array[:10]:  # Mostrar només els primers 10
        print(f"  - {refugi['name']}: {refugi['types']}")
    if len(refugis_amb_array) > 10:
        print(f"  ... i {len(refugis_amb_array) - 10} més")

if refugis_sense_type:
    print("\n" + "=" * 70)
    print("Refugis sense type:")
    print("-" * 70)
    for name in refugis_sense_type[:10]:
        print(f"  - {name}")
    if len(refugis_sense_type) > 10:
        print(f"  ... i {len(refugis_sense_type) - 10} més")

print("\n" + "=" * 70)
print("TIPUS ESPERATS DESPRÉS DE L'ACTUALITZACIÓ:")
print("-" * 70)
expected_types = [
    'fermée',
    'non gardé',
    'orri',
    'cabane ouverte mais ocupee par le berger l ete',
    'Détruite',
    '' # type buit
]
print("Els únics valors que hauria de tenir el camp 'type' són:")
for t in expected_types:
    if t == '':
        print(f"  - (buit)")
    else:
        print(f"  - {t}")

print("\n✓ Verificació completada!")
