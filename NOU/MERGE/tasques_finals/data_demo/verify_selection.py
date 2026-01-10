#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per verificar que la selecció i processament de refugis s'ha fet correctament.
"""

import json
from collections import defaultdict
from typing import List, Dict, Any


def load_json(filepath: str) -> List[Dict[str, Any]]:
    """Carrega dades d'un fitxer JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def verify_data_transformations(refuges: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Verifica que les transformacions de dades s'han aplicat correctament."""
    
    results = {
        'total_refuges': len(refuges),
        'errors': [],
        'warnings': [],
        'checks': {}
    }
    
    # 1. Verificar que no hi ha camp 'remarque'
    refuges_amb_remarque = []
    for i, refuge in enumerate(refuges):
        if 'remarque' in refuge:
            refuges_amb_remarque.append({
                'index': i,
                'name': refuge.get('name', 'unknown')
            })
    
    results['checks']['remarque_eliminat'] = {
        'passed': len(refuges_amb_remarque) == 0,
        'refuges_amb_remarque': len(refuges_amb_remarque),
        'detalls': refuges_amb_remarque[:5]  # Mostrem només els primers 5
    }
    
    if refuges_amb_remarque:
        results['errors'].append(
            f"ERROR: {len(refuges_amb_remarque)} refugis encara tenen el camp 'remarque'"
        )
    
    # 2. Verificar que 'description' no és un array
    descriptions_array = []
    descriptions_none = 0
    descriptions_string = 0
    
    for i, refuge in enumerate(refuges):
        desc = refuge.get('description')
        if isinstance(desc, list):
            descriptions_array.append({
                'index': i,
                'name': refuge.get('name', 'unknown'),
                'description': desc
            })
        elif desc is None:
            descriptions_none += 1
        elif isinstance(desc, str):
            descriptions_string += 1
    
    results['checks']['description_format'] = {
        'passed': len(descriptions_array) == 0,
        'descriptions_string': descriptions_string,
        'descriptions_none': descriptions_none,
        'descriptions_array': len(descriptions_array),
        'detalls': descriptions_array[:5]
    }
    
    if descriptions_array:
        results['errors'].append(
            f"ERROR: {len(descriptions_array)} refugis encara tenen 'description' com a array"
        )
    
    return results


def verify_variety(refuges: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Verifica que hi ha varietat en els diferents camps."""
    
    results = {
        'type': defaultdict(int),
        'altitude_ranges': defaultdict(int),
        'places_ranges': defaultdict(int),
        'links_count': defaultdict(int),
        'info_comp_features': defaultdict(int),
        'regions': defaultdict(int),
        'departements': defaultdict(int)
    }
    
    required_types = [
        'non gardé',
        'fermée',
        'cabane ouverte mais ocupee par le berger l ete',
        'orri'
    ]
    
    for refuge in refuges:
        # Tipus
        refuge_type = refuge.get('type', 'unknown')
        results['type'][refuge_type] += 1
        
        # Altitud
        altitude = refuge.get('altitude')
        if altitude is None:
            results['altitude_ranges']['null'] += 1
        elif altitude < 1500:
            results['altitude_ranges']['<1500'] += 1
        elif altitude < 2000:
            results['altitude_ranges']['1500-2000'] += 1
        elif altitude < 2500:
            results['altitude_ranges']['2000-2500'] += 1
        else:
            results['altitude_ranges']['>=2500'] += 1
        
        # Places
        places = refuge.get('places')
        if places is None:
            results['places_ranges']['null'] += 1
        elif places == 0:
            results['places_ranges']['0'] += 1
        elif places <= 5:
            results['places_ranges']['1-5'] += 1
        elif places <= 10:
            results['places_ranges']['6-10'] += 1
        elif places <= 20:
            results['places_ranges']['11-20'] += 1
        else:
            results['places_ranges']['>20'] += 1
        
        # Links
        num_links = len(refuge.get('links', []))
        results['links_count'][num_links] += 1
        
        # Info_comp
        info_comp = refuge.get('info_comp')
        if info_comp:
            num_features = sum(1 for v in info_comp.values() if v == 1)
            if num_features == 0:
                results['info_comp_features']['0'] += 1
            elif num_features <= 2:
                results['info_comp_features']['1-2'] += 1
            elif num_features <= 4:
                results['info_comp_features']['3-4'] += 1
            else:
                results['info_comp_features']['5+'] += 1
        else:
            results['info_comp_features']['null'] += 1
        
        # Region
        region = refuge.get('region')
        results['regions'][region if region else 'null'] += 1
        
        # Departement
        dept = refuge.get('departement')
        results['departements'][dept if dept else 'null'] += 1
    
    # Verificar que tenim els 4 tipus requerits
    missing_types = [t for t in required_types if results['type'][t] == 0]
    
    return results, missing_types


def generate_report(
    transformations: Dict[str, Any],
    variety: Dict[str, Any],
    missing_types: List[str],
    output_file: str
):
    """Genera un informe de verificació."""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("INFORME DE VERIFICACIÓ - data_demo.json\n")
        f.write("="*70 + "\n\n")
        
        # 1. TRANSFORMACIONS DE DADES
        f.write("1. VERIFICACIÓ DE TRANSFORMACIONS\n")
        f.write("-"*70 + "\n\n")
        
        f.write(f"Total refugis: {transformations['total_refuges']}\n\n")
        
        # Remarque
        check = transformations['checks']['remarque_eliminat']
        status = "✓ PASS" if check['passed'] else "✗ FAIL"
        f.write(f"Eliminació del camp 'remarque': {status}\n")
        f.write(f"  - Refugis amb 'remarque': {check['refuges_amb_remarque']}\n")
        if check['detalls']:
            f.write(f"  - Exemples: {check['detalls']}\n")
        f.write("\n")
        
        # Description
        check = transformations['checks']['description_format']
        status = "✓ PASS" if check['passed'] else "✗ FAIL"
        f.write(f"Conversió de 'description' a string: {status}\n")
        f.write(f"  - Descriptions com a string: {check['descriptions_string']}\n")
        f.write(f"  - Descriptions null: {check['descriptions_none']}\n")
        f.write(f"  - Descriptions com a array: {check['descriptions_array']}\n")
        if check['detalls']:
            f.write(f"  - Exemples d'arrays: {check['detalls']}\n")
        f.write("\n")
        
        # Errors i warnings
        if transformations['errors']:
            f.write("ERRORS TROBATS:\n")
            for error in transformations['errors']:
                f.write(f"  - {error}\n")
            f.write("\n")
        else:
            f.write("✓ Cap error de transformació trobat\n\n")
        
        if transformations['warnings']:
            f.write("ADVERTÈNCIES:\n")
            for warning in transformations['warnings']:
                f.write(f"  - {warning}\n")
            f.write("\n")
        
        # 2. VARIETAT DE DADES
        f.write("\n" + "="*70 + "\n")
        f.write("2. VERIFICACIÓ DE VARIETAT\n")
        f.write("-"*70 + "\n\n")
        
        # Tipus
        f.write("TIPUS DE REFUGIS:\n")
        for type_name, count in sorted(variety['type'].items()):
            f.write(f"  - {type_name}: {count}\n")
        
        if missing_types:
            f.write(f"\n✗ ATENCIÓ: Falten els següents tipus:\n")
            for t in missing_types:
                f.write(f"    - {t}\n")
        else:
            f.write(f"\n✓ Tots els 4 tipus requerits estan presents\n")
        f.write("\n")
        
        # Altitud
        f.write("DISTRIBUCIÓ PER ALTITUD:\n")
        for range_name, count in sorted(variety['altitude_ranges'].items()):
            f.write(f"  - {range_name}: {count}\n")
        f.write("\n")
        
        # Places
        f.write("DISTRIBUCIÓ PER PLACES:\n")
        for range_name, count in sorted(variety['places_ranges'].items()):
            f.write(f"  - {range_name}: {count}\n")
        f.write("\n")
        
        # Links
        f.write("DISTRIBUCIÓ PER NOMBRE DE LINKS:\n")
        for num_links, count in sorted(variety['links_count'].items()):
            f.write(f"  - {num_links} links: {count}\n")
        f.write("\n")
        
        # Info_comp
        f.write("DISTRIBUCIÓ PER CARACTERÍSTIQUES (info_comp):\n")
        for features, count in sorted(variety['info_comp_features'].items()):
            f.write(f"  - {features} característiques: {count}\n")
        f.write("\n")
        
        # Regions
        f.write("DISTRIBUCIÓ PER REGIONS (top 10):\n")
        top_regions = sorted(variety['regions'].items(), key=lambda x: x[1], reverse=True)[:10]
        for region, count in top_regions:
            f.write(f"  - {region}: {count}\n")
        f.write(f"  Total regions diferents: {len(variety['regions'])}\n\n")
        
        # Departaments
        f.write("DISTRIBUCIÓ PER DEPARTAMENTS (top 10):\n")
        top_depts = sorted(variety['departements'].items(), key=lambda x: x[1], reverse=True)[:10]
        for dept, count in top_depts:
            f.write(f"  - {dept}: {count}\n")
        f.write(f"  Total departaments diferents: {len(variety['departements'])}\n\n")
        
        # 3. CONCLUSIÓ
        f.write("\n" + "="*70 + "\n")
        f.write("3. CONCLUSIÓ\n")
        f.write("-"*70 + "\n\n")
        
        all_passed = (
            transformations['checks']['remarque_eliminat']['passed'] and
            transformations['checks']['description_format']['passed'] and
            len(missing_types) == 0
        )
        
        if all_passed:
            f.write("✓ VERIFICACIÓ COMPLETADA AMB ÈXIT\n")
            f.write("  Totes les transformacions s'han aplicat correctament\n")
            f.write("  i hi ha una bona varietat de refugis seleccionats.\n")
        else:
            f.write("✗ VERIFICACIÓ AMB PROBLEMES\n")
            f.write("  Revisa els errors i advertències anteriors.\n")
        
        f.write("\n" + "="*70 + "\n")


def main():
    """Funció principal."""
    input_file = 'data_demo.json'
    output_file = 'verificacio_data_demo.txt'
    
    print(f"Carregant dades de {input_file}...")
    try:
        refuges = load_json(input_file)
    except FileNotFoundError:
        print(f"ERROR: No s'ha trobat el fitxer {input_file}")
        print("Assegura't d'executar primer select_varied_refuges.py")
        return
    
    print(f"Total refugis: {len(refuges)}")
    
    print("\nVerificant transformacions de dades...")
    transformations = verify_data_transformations(refuges)
    
    print("Verificant varietat de dades...")
    variety, missing_types = verify_variety(refuges)
    
    print(f"\nGenerant informe a {output_file}...")
    generate_report(transformations, variety, missing_types, output_file)
    
    # Resum per consola
    print("\n" + "="*70)
    print("RESUM DE LA VERIFICACIÓ")
    print("="*70)
    
    print(f"\nTotal refugis: {transformations['total_refuges']}")
    
    print("\nTransformacions:")
    print(f"  - Remarque eliminat: {'✓' if transformations['checks']['remarque_eliminat']['passed'] else '✗'}")
    print(f"  - Description convertit a string: {'✓' if transformations['checks']['description_format']['passed'] else '✗'}")
    
    print("\nVarietat:")
    print(f"  - Tipus diferents: {len(variety['type'])}")
    print(f"  - Tipus requerits presents: {'✓' if len(missing_types) == 0 else '✗'}")
    if missing_types:
        print(f"    Falten: {', '.join(missing_types)}")
    print(f"  - Regions diferents: {len(variety['regions'])}")
    print(f"  - Departaments diferents: {len(variety['departements'])}")
    
    if transformations['errors']:
        print(f"\n✗ {len(transformations['errors'])} errors trobats")
    else:
        print("\n✓ Cap error trobat")
    
    print(f"\n✓ Informe complet guardat a {output_file}")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
