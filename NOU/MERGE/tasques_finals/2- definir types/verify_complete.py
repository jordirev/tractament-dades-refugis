import json

# Llegir el fitxer actualitzat
with open('data_refugis_updated_types.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 70)
print("VERIFICACIÓ COMPLETA DEL FITXER data_refugis_updated_types.json")
print("=" * 70)

# 1. Verificar tipus
type_errors = []
types_as_arrays = []
for i, refugi in enumerate(data):
    if isinstance(refugi.get('type'), list):
        types_as_arrays.append(refugi.get('name', f'Index {i}'))
    elif not isinstance(refugi.get('type'), (str, type(None))):
        type_errors.append(refugi.get('name', f'Index {i}'))

print("\n1. VERIFICACIÓ CAMP 'TYPE':")
print("-" * 70)
print(f"   Total refugis: {len(data)}")
print(f"   Types com a array: {len(types_as_arrays)}")
print(f"   Errors de tipus: {len(type_errors)}")
if len(types_as_arrays) == 0 and len(type_errors) == 0:
    print("   ✓ CORRECTE: Tots els types són strings o null")
else:
    print("   ✗ ERROR: Hi ha types amb format incorrecte")

# 2. Verificar altituds
altitude_decimals = []
altitude_not_int = []
for i, refugi in enumerate(data):
    alt = refugi.get('altitude')
    if alt is not None:
        if not isinstance(alt, int):
            altitude_not_int.append((refugi.get('name', f'Index {i}'), alt, type(alt).__name__))
        elif isinstance(alt, float) and alt != int(alt):
            altitude_decimals.append((refugi.get('name', f'Index {i}'), alt))

print("\n2. VERIFICACIÓ CAMP 'ALTITUDE':")
print("-" * 70)
print(f"   Altituds amb decimals: {len(altitude_decimals)}")
print(f"   Altituds que no són int: {len(altitude_not_int)}")
if len(altitude_decimals) == 0 and len(altitude_not_int) == 0:
    print("   ✓ CORRECTE: Totes les altituds són enters sense decimals")
else:
    print("   ✗ ERROR: Hi ha altituds amb decimals o tipus incorrecte")
    if altitude_not_int:
        for name, alt, tipo in altitude_not_int[:5]:
            print(f"      - {name}: {alt} (tipus: {tipo})")

# 3. Verificar places
places_zero_not_fermee = []
for i, refugi in enumerate(data):
    places = refugi.get('places')
    type_val = refugi.get('type')
    if places == 0 and type_val != 'fermée':
        places_zero_not_fermee.append((refugi.get('name', f'Index {i}'), type_val))

print("\n3. VERIFICACIÓ CAMP 'PLACES':")
print("-" * 70)
print(f"   Refugis amb places=0 i type!=fermée: {len(places_zero_not_fermee)}")
if len(places_zero_not_fermee) == 0:
    print("   ✓ CORRECTE: No hi ha refugis amb places=0 (excepte fermée)")
else:
    print("   ✗ ERROR: Hi ha refugis amb places=0 que no són fermée")
    for name, type_val in places_zero_not_fermee[:5]:
        print(f"      - {name} (type: {type_val})")

# Comptar places null
places_null = sum(1 for r in data if r.get('places') is None)
print(f"   Refugis amb places=null: {places_null}")

# 4. Verificar coordenades
coord_too_many_decimals = []
for i, refugi in enumerate(data):
    coord = refugi.get('coord')
    if coord:
        lat = coord.get('lat')
        long = coord.get('long')
        if lat is not None:
            lat_str = str(lat)
            if '.' in lat_str and len(lat_str.split('.')[1]) > 6:
                coord_too_many_decimals.append((refugi.get('name', f'Index {i}'), 'lat', lat))
        if long is not None:
            long_str = str(long)
            if '.' in long_str and len(long_str.split('.')[1]) > 6:
                coord_too_many_decimals.append((refugi.get('name', f'Index {i}'), 'long', long))

print("\n4. VERIFICACIÓ COORDENADES:")
print("-" * 70)
print(f"   Coordenades amb més de 6 decimals: {len(coord_too_many_decimals)}")
if len(coord_too_many_decimals) == 0:
    print("   ✓ CORRECTE: Totes les coordenades tenen màxim 6 decimals")
else:
    print("   ✗ ERROR: Hi ha coordenades amb més de 6 decimals")
    for name, field, value in coord_too_many_decimals[:5]:
        print(f"      - {name} ({field}): {value}")

# Resum final
print("\n" + "=" * 70)
print("RESUM FINAL:")
print("-" * 70)
errors_total = len(types_as_arrays) + len(type_errors) + len(altitude_decimals) + len(altitude_not_int) + len(places_zero_not_fermee) + len(coord_too_many_decimals)
if errors_total == 0:
    print("✓✓✓ TOTES LES VERIFICACIONS CORRECTES ✓✓✓")
else:
    print(f"✗ S'han trobat {errors_total} errors/avisos")

print("=" * 70)
