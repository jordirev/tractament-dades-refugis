import json
import re
from typing import Union, Optional

def refusPyrenees_merged_filtered_normalized():
    """
    Normalitza el fitxer refusPyrinees_merged_filtered.json:
    - Converteix "altitude" a número. Si no hi ha o és 0, posa null.
    - Converteix "cap_ete" i "cap_hiver" en un sol camp "places" amb el valor més gran.
    - Extreu números de strings complexos i frases.
    - Guarda el resultat com refusPyrenees_finished.json
    """
    
    def extract_max_number_from_string(text: str) -> Optional[int]:
        """
        Extreu el número més gran d'un string que pot contenir múltiples números o text descriptiu.
        Retorna None si no troba cap número vàlid.
        """
        if not text or text.strip() == '':
            return None
            
        # Casos especials coneguts
        text = text.strip().lower()
        
        # Si és exactament "0", retornem 0
        if text == '0':
            return 0
            
        # Si conté "non", "nada", "néant", etc., retornem 0
        negative_words = ['non', 'nada', 'néant', 'rien']
        if any(word in text for word in negative_words):
            return 0
            
        # Buscar tots els números en el text
        numbers = re.findall(r'\d+', text)
        
        if not numbers:
            return None
            
        # Convertir a enters i retornar el màxim
        try:
            int_numbers = [int(num) for num in numbers]
            return max(int_numbers)
        except ValueError:
            return None
    
    def normalize_altitude(altitude_str: str) -> Optional[int]:
        """
        Normalitza el camp altitude.
        Retorna None si no hi ha valor o és 0.
        """
        if not altitude_str or altitude_str.strip() == '':
            return None
            
        try:
            alt = int(float(altitude_str.strip()))
            return alt if alt > 0 else None
        except (ValueError, TypeError):
            # Intentar extreure número del string
            number = extract_max_number_from_string(altitude_str)
            return number if number and number > 0 else None
    
    def calculate_places(cap_ete: str, cap_hiver: str) -> Optional[int]:
        """
        Calcula el camp "places" a partir de cap_ete i cap_hiver.
        Retorna el valor més gran entre els dos, o None si no hi ha cap número vàlid.
        """
        ete_places = extract_max_number_from_string(cap_ete)
        hiver_places = extract_max_number_from_string(cap_hiver)
        
        # Si cap dels dos té valor, retornem None
        if ete_places is None and hiver_places is None:
            return None
            
        # Si només un té valor, retornem aquell
        if ete_places is None:
            return hiver_places
        if hiver_places is None:
            return ete_places
            
        # Si ambdós tenen valor, retornem el màxim
        return max(ete_places, hiver_places)
    
    # Llegir el fitxer original
    input_file = r'refusPyrinees_merged_filtered.json'
    output_file = r'refusPyrenees_finished.json'
    
    print("Llegint el fitxer original...")
    with open(input_file, 'r', encoding='utf-8') as f:
        refuges = json.load(f)
    
    print(f"Processant {len(refuges)} refugis...")
    
    # Estadístiques per fer seguiment
    stats = {
        'total_refuges': len(refuges),
        'altitude_nulls': 0,
        'altitude_converted': 0,
        'places_nulls': 0,
        'places_calculated': 0,
        'casos_especials': []
    }
    
    normalized_refuges = []
    
    for i, refuge in enumerate(refuges):
        # Crear una còpia del refugi
        normalized_refuge = refuge.copy()
        
        # Normalitzar altitude
        original_altitude = refuge.get('altitude', '')
        normalized_altitude = normalize_altitude(original_altitude)
        
        if normalized_altitude is None:
            stats['altitude_nulls'] += 1
        else:
            stats['altitude_converted'] += 1
            
        normalized_refuge['altitude'] = normalized_altitude
        
        # Calcular places
        cap_ete = refuge.get('cap_ete', '')
        cap_hiver = refuge.get('cap_hiver', '')
        places = calculate_places(cap_ete, cap_hiver)
        
        if places is None:
            stats['places_nulls'] += 1
        else:
            stats['places_calculated'] += 1
        
        # Eliminar els camps originals i afegir el nou
        if 'cap_ete' in normalized_refuge:
            del normalized_refuge['cap_ete']
        if 'cap_hiver' in normalized_refuge:
            del normalized_refuge['cap_hiver']
            
        normalized_refuge['places'] = places
        
        # Detectar casos especials per a la verificació
        if (cap_ete and cap_ete not in ['', ' ', '0']) or (cap_hiver and cap_hiver not in ['', ' ', '0']):
            if len(re.findall(r'\d+', cap_ete + ' ' + cap_hiver)) > 2:  # Més de 2 números
                stats['casos_especials'].append({
                    'nom': refuge.get('name', 'Unknown'),
                    'cap_ete': cap_ete,
                    'cap_hiver': cap_hiver,
                    'places_calculat': places
                })
        
        normalized_refuges.append(normalized_refuge)
        
        # Mostrar progrés cada 100 refugis
        if (i + 1) % 100 == 0:
            print(f"Processat {i + 1}/{len(refuges)} refugis...")
    
    # Guardar el resultat
    print(f"Guardant el resultat a {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(normalized_refuges, f, ensure_ascii=False, indent=2)
    
    # Mostrar estadístiques
    print("\n" + "="*60)
    print("ESTADÍSTIQUES DE LA NORMALITZACIÓ")
    print("="*60)
    print(f"Total de refugis processats: {stats['total_refuges']}")
    print(f"Altituds convertides a número: {stats['altitude_converted']}")
    print(f"Altituds posades a null: {stats['altitude_nulls']}")
    print(f"Places calculades: {stats['places_calculated']}")
    print(f"Places posades a null: {stats['places_nulls']}")
    print(f"Casos especials detectats: {len(stats['casos_especials'])}")
    
    if stats['casos_especials']:
        print("\nCASOS ESPECIALS (primers 10):")
        for i, cas in enumerate(stats['casos_especials'][:10]):
            print(f"{i+1}. {cas['nom']}")
            print(f"   cap_ete: '{cas['cap_ete']}' | cap_hiver: '{cas['cap_hiver']}' → places: {cas['places_calculat']}")
    
    print(f"\nFitxer guardat amb èxit: {output_file}")
    
    # Verificacions adicionals
    verify_normalization(normalized_refuges)

def verify_normalization(refuges):
    """
    Fa verificacions adicionals per assegurar que la normalització s'ha fet correctament.
    """
    print("\n" + "="*60)
    print("VERIFICACIONS DE QUALITAT")
    print("="*60)
    
    altitude_issues = []
    places_issues = []
    
    for refuge in refuges:
        name = refuge.get('name', 'Unknown')
        
        # Verificar altitude
        altitude = refuge.get('altitude')
        if altitude is not None and (not isinstance(altitude, int) or altitude < 0):
            altitude_issues.append(f"{name}: altitude={altitude}")
            
        # Verificar places
        places = refuge.get('places')
        if places is not None and (not isinstance(places, int) or places < 0):
            places_issues.append(f"{name}: places={places}")
    
    print(f"Problemes amb altitude: {len(altitude_issues)}")
    if altitude_issues[:5]:  # Mostrar només els primers 5
        for issue in altitude_issues[:5]:
            print(f"  - {issue}")
    
    print(f"Problemes amb places: {len(places_issues)}")
    if places_issues[:5]:  # Mostrar només els primers 5
        for issue in places_issues[:5]:
            print(f"  - {issue}")
    
    # Mostrar distribució de places
    places_distribution = {}
    null_places = 0
    
    for refuge in refuges:
        places = refuge.get('places')
        if places is None:
            null_places += 1
        else:
            places_distribution[places] = places_distribution.get(places, 0) + 1
    
    print(f"\nDistribució de places:")
    print(f"  Places null: {null_places}")
    print(f"  Places amb valor: {len(refuges) - null_places}")
    
    # Mostrar les places més comunes
    sorted_places = sorted(places_distribution.items(), key=lambda x: x[1], reverse=True)
    print("  Places més comunes:")
    for places, count in sorted_places[:10]:
        print(f"    {places} places: {count} refugis")

def test_edge_cases():
    """
    Testa casos especials per assegurar que la funció funciona correctament.
    """
    print("\n" + "="*60)
    print("TESTANT CASOS ESPECIALS")
    print("="*60)
    
    def extract_max_number_from_string(text: str) -> Optional[int]:
        if not text or text.strip() == '':
            return None
            
        text = text.strip().lower()
        
        if text == '0':
            return 0
            
        negative_words = ['non', 'nada', 'néant', 'rien']
        if any(word in text for word in negative_words):
            return 0
            
        numbers = re.findall(r'\d+', text)
        
        if not numbers:
            return None
            
        try:
            int_numbers = [int(num) for num in numbers]
            return max(int_numbers)
        except ValueError:
            return None
    
    # Casos de test basats en l'anàlisi
    test_cases = [
        ('3 4', 4),
        ('15 20', 20),
        ('6 8', 8),
        ('4 6 ', 6),
        ('2 2x2 serre', 2),
        ('0 2', 2),
        ('2 ou plus ', 2),
        ('15 env ', 15),
        ('12 20', 20),
        ('4 hors periode d', 4),
        ('4 5', 5),
        ('4 5 2 3 ', 5),
        ('4 ou plus ', 4),
        ('0 ou 4', 4),
        ('env 5 6', 6),
        ('2 3 assis ', 3),
        ('4 3', 4),
        ('8 10 sur sol beton', 10),
        ('non', 0),
        ('', None),
        (' ', None),
        ('0', 0),
        ('10', 10)
    ]
    
    errors = 0
    for input_text, expected in test_cases:
        result = extract_max_number_from_string(input_text)
        if result != expected:
            print(f"ERROR: '{input_text}' → {result} (esperat: {expected})")
            errors += 1
        else:
            print(f"OK: '{input_text}' → {result}")
    
    print(f"\nTests completats: {len(test_cases)}")
    print(f"Errors trobats: {errors}")
    
    return errors == 0

if __name__ == "__main__":
    # Primer testem els casos especials
    if test_edge_cases():
        print("\n✅ Tots els tests han passat. Procedint amb la normalització...")
        refusPyrenees_merged_filtered_normalized()
    else:
        print("\n❌ Hi ha errors en els tests. Revisa la implementació.")