import json

# Llegir el fitxer JSON
with open('data_refugis_updated_altitudes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Comptadors per fer seguiment dels canvis
stats = {
    'total_refugis': len(data),
    'types_modificats': 0,
    'conversions': {
        'fermée + cabane fermee -> fermée': 0,
        'cabane ouverte + cabane ouverte mais ocupee par le berger l ete -> cabane ouverte mais ocupee par le berger l ete': 0,
        'cabane ouverte + orri toue abri en pierre -> orri': 0,
        'cabane ouverte -> non gardé': 0,
        'orri toue abri en pierre -> orri': 0,
        'Fermée -> fermée': 0,
        'cabane fermee -> fermée': 0
    }
}

# Processar cada refugi
for refugi in data:
    type_field = refugi.get('type')
    original_type = type_field
    
    # Si type és un array (llista)
    if isinstance(type_field, list):
        # Si l'array només té un element, convertir-lo a string
        if len(type_field) == 1:
            type_field = type_field[0]
            refugi['type'] = type_field
            # Ara processar com si fos un string
        else:
            # Arrays amb múltiples elements
            type_set = set(type_field)
            
            # Fermée + cabane fermee -> fermée
            if type_set == {'Fermée', 'cabane fermee'}:
                refugi['type'] = 'fermée'
                stats['conversions']['fermée + cabane fermee -> fermée'] += 1
                stats['types_modificats'] += 1
                continue
            
            # cabane ouverte + cabane ouverte mais ocupee par le berger l ete -> cabane ouverte mais ocupee par le berger l ete
            elif type_set == {'cabane ouverte', 'cabane ouverte mais ocupee par le berger l ete'}:
                refugi['type'] = 'cabane ouverte mais ocupee par le berger l ete'
                stats['conversions']['cabane ouverte + cabane ouverte mais ocupee par le berger l ete -> cabane ouverte mais ocupee par le berger l ete'] += 1
                stats['types_modificats'] += 1
                continue
            
            # cabane ouverte + orri toue abri en pierre -> orri
            elif type_set == {'cabane ouverte', 'orri toue abri en pierre'}:
                refugi['type'] = 'orri'
                stats['conversions']['cabane ouverte + orri toue abri en pierre -> orri'] += 1
                stats['types_modificats'] += 1
                continue
            else:
                # Si hi ha un array amb múltiples elements que no coincideix amb cap patró
                continue
    
    # Ara processar strings (tant originals com convertits d'arrays d'un element)
    if isinstance(refugi['type'], str):
        type_field = refugi['type']
        
        # cabane ouverte -> non gardé
        if type_field == 'cabane ouverte':
            refugi['type'] = 'non gardé'
            stats['conversions']['cabane ouverte -> non gardé'] += 1
            stats['types_modificats'] += 1
        
        # orri toue abri en pierre -> orri
        elif type_field == 'orri toue abri en pierre':
            refugi['type'] = 'orri'
            stats['conversions']['orri toue abri en pierre -> orri'] += 1
            stats['types_modificats'] += 1
        
        # Fermée -> fermée (normalitzar majúscules)
        elif type_field == 'Fermée':
            refugi['type'] = 'fermée'
            stats['conversions']['Fermée -> fermée'] += 1
            stats['types_modificats'] += 1
        
        # cabane fermee -> fermée
        elif type_field == 'cabane fermee':
            refugi['type'] = 'fermée'
            stats['conversions']['cabane fermee -> fermée'] += 1
            stats['types_modificats'] += 1

# Comptadors per a les noves transformacions
transformations = {
    'altitude_arrodonida': 0,
    'places_a_null': 0,
    'coordenades_arrodonides': 0
}

# Aplicar les noves transformacions
for refugi in data:
    # 1. Altitude sense decimals (número enter)
    if 'altitude' in refugi and refugi['altitude'] is not None:
        if isinstance(refugi['altitude'], (int, float)):
            refugi['altitude'] = int(round(refugi['altitude']))
            transformations['altitude_arrodonida'] += 1
    
    # 2. Si places==0 i type!=fermée, llavors places = null
    if refugi.get('places') == 0 and refugi.get('type') != 'fermée':
        refugi['places'] = None
        transformations['places_a_null'] += 1
    
    # 3. Reduir coordenades lat i long a 6 decimals com a molt
    if 'coord' in refugi and refugi['coord'] is not None:
        if 'lat' in refugi['coord'] and refugi['coord']['lat'] is not None:
            refugi['coord']['lat'] = round(refugi['coord']['lat'], 6)
        if 'long' in refugi['coord'] and refugi['coord']['long'] is not None:
            refugi['coord']['long'] = round(refugi['coord']['long'], 6)
        transformations['coordenades_arrodonides'] += 1

# Guardar el fitxer actualitzat
with open('data_refugis_updated_types.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Mostrar estadístiques
print("ACTUALITZACIÓ DE DADES COMPLETADA")
print("=" * 60)
print(f"Total de refugis processats: {stats['total_refugis']}")
print(f"Total de refugis amb tipus modificat: {stats['types_modificats']}")
print("\nDETALL DE CONVERSIONS DE TIPUS:")
print("-" * 60)
for conversion, count in stats['conversions'].items():
    if count > 0:
        print(f"  {conversion}: {count}")

print("\nTRANSFORMACIONS ADDICIONALS:")
print("-" * 60)
print(f"  Altituds arrodonides a enter: {transformations['altitude_arrodonida']}")
print(f"  Places=0 canviades a null (type!=fermée): {transformations['places_a_null']}")
print(f"  Coordenades arrodonides a 6 decimals: {transformations['coordenades_arrodonides']}")

print(f"\nFitxer generat: data_refugis_updated_types.json")
