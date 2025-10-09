import json

def verify_results():
    """Verifica els resultats de la normalització"""
    
    # Llegir el fitxer normalitzat
    with open('refusPyrenees_finished.json', 'r', encoding='utf-8') as f:
        refuges = json.load(f)

    print('VERIFICACIÓ DE CASOS ESPECÍFICS:')
    print('=' * 50)

    # Cercar refugis amb casos especials coneguts
    casos_test = [
        'Cabane Areng',  # '4 a 5' → 5
        'Cabane de l\'Artigue (col d\'Esponne)',  # '6 3' → 6
        'Cabane Benaques',  # cap_ete: '0', cap_hiver: '5 6' → 6
        'Cabane de Beziaou',  # '3 4' → 4
        'Cabane du Bouchidet',  # '6 8' → 8
    ]

    for nom_cas in casos_test:
        refugi_trobat = None
        for refugi in refuges:
            if refugi['name'] == nom_cas:
                refugi_trobat = refugi
                break
        
        if refugi_trobat:
            print(f'{nom_cas}:')
            print(f'  - Altitude: {refugi_trobat.get("altitude")}')
            print(f'  - Places: {refugi_trobat.get("places")}')
        else:
            print(f'{nom_cas}: NO TROBAT')
        print()

    # Estadístiques generals
    total_refuges = len(refuges)
    refuges_amb_places = sum(1 for r in refuges if r.get('places') is not None)
    refuges_sense_places = total_refuges - refuges_amb_places
    refuges_amb_altitude = sum(1 for r in refuges if r.get('altitude') is not None)
    refuges_sense_altitude = total_refuges - refuges_amb_altitude

    print('ESTADÍSTIQUES FINALS:')
    print('=' * 30)
    print(f'Total refugis: {total_refuges}')
    print(f'Refugis amb places: {refuges_amb_places}')
    print(f'Refugis sense places (null): {refuges_sense_places}')
    print(f'Refugis amb altitude: {refuges_amb_altitude}')
    print(f'Refugis sense altitude (null): {refuges_sense_altitude}')

    # Verificar que no hi ha camps cap_ete o cap_hiver
    camps_antics = 0
    for refugi in refuges:
        if 'cap_ete' in refugi or 'cap_hiver' in refugi:
            camps_antics += 1

    print(f'Refugis amb camps antics (cap_ete/cap_hiver): {camps_antics}')
    
    # Mostrar alguns exemples de places calculades
    print('\nEXEMPLES DE PLACES CALCULADES:')
    print('=' * 35)
    
    exemples_mostrats = 0
    for refugi in refuges:
        places = refugi.get('places')
        if places is not None and places > 0 and exemples_mostrats < 5:
            print(f'{refugi["name"]}: {places} places')
            exemples_mostrats += 1

if __name__ == "__main__":
    verify_results()