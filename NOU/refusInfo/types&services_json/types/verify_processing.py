import json

# Cargar el archivo procesado
with open('refusInfo_normalized_with_types.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Buscar ejemplos donde remarque fue eliminado
examples_no_remarque = [n for n in data['nodes'] if 'description' in n and 'remarque' not in n]

print(f"Ejemplos de nodos SIN remarque (eliminado por ser igual a description):")
for i, ex in enumerate(examples_no_remarque[:5], 1):
    print(f"{i}. ID: {ex['id']}, Nombre: {ex['nom']}")
    print(f"   Type: {ex['type']}")
    print(f"   Description: {ex['description'][:100]}...")
    print()

# Verificar tipos
type_counts = {}
for node in data['nodes']:
    node_type = node.get('type', 'Sin type')
    type_counts[node_type] = type_counts.get(node_type, 0) + 1

print("Distribución de tipos:")
for tipo, count in type_counts.items():
    print(f"- {tipo}: {count}")