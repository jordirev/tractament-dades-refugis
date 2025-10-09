import json
import os

# Rutas de archivos
input_json_path = "refusInfo_normalized.json"
output_json_path = "refusInfo_normalized_with_types.json"

# Leer el archivo JSON normalizado
with open(input_json_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Contadores para estadísticas
stats = {
    'total_nodes': len(data['nodes']),
    'type_fermee': 0,
    'type_detruite': 0,
    'type_cabane_ouverte': 0,
    'etat_removed_equal_remarque': 0,
    'remarque_removed_equal_description': 0
}

# Procesar cada nodo
for node in data['nodes']:
    # 1. Manejar el campo "etat" y crear "type"
    if 'etat' in node:
        if node['etat'] == "Fermée":
            node['type'] = "Fermée"
            del node['etat']
            stats['type_fermee'] += 1
        elif node['etat'] == "Détruite":
            node['type'] = "Détruite"
            del node['etat']
            stats['type_detruite'] += 1
        else:
            # Si etat no es Fermée ni Détruite
            node['type'] = "cabane ouverte"
            
            # Eliminar etat si es igual que remarque
            if 'remarque' in node and node['etat'] == node['remarque']:
                del node['etat']
                stats['etat_removed_equal_remarque'] += 1
            else:
                # Si etat es diferente de remarque, mantener ambos y agregar type
                pass
            stats['type_cabane_ouverte'] += 1
    else:
        # Si no hay campo etat, establecer type por defecto
        node['type'] = "cabane ouverte"
        stats['type_cabane_ouverte'] += 1
    
    # 2. Eliminar remarque si es igual que description
    if 'remarque' in node and 'description' in node:
        if node['remarque'] == node['description']:
            del node['remarque']
            stats['remarque_removed_equal_description'] += 1

# Escribir el resultado al archivo de salida
with open(output_json_path, 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=2)

# Mostrar estadísticas
print("Procesamiento completado!")
print(f"Archivo de salida: {output_json_path}")
print("\nEstadísticas:")
print(f"- Total de nodos procesados: {stats['total_nodes']}")
print(f"- Nodos con type 'Fermée': {stats['type_fermee']}")
print(f"- Nodos con type 'Détruite': {stats['type_detruite']}")
print(f"- Nodos con type 'cabane ouverte': {stats['type_cabane_ouverte']}")
print(f"- Campos 'etat' eliminados (igual a remarque): {stats['etat_removed_equal_remarque']}")
print(f"- Campos 'remarque' eliminados (igual a description): {stats['remarque_removed_equal_description']}")

# Mostrar un ejemplo del primer nodo procesado
print(f"\nEjemplo del primer nodo procesado:")
first_node = data['nodes'][0]
print(f"ID: {first_node['id']}")
print(f"Nombre: {first_node['nom']}")
print(f"Type: {first_node['type']}")
print(f"Tiene 'etat': {'etat' in first_node}")
print(f"Tiene 'remarque': {'remarque' in first_node}")
print(f"Tiene 'description': {'description' in first_node}")