#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificació del merge de refugis duplicats.
Comprova que el merge s'ha fet correctament segons les normes especificades.
"""

import json
from typing import Dict, List, Any


def load_json(filepath: str) -> List[Dict]:
    """Carrega un fitxer JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def check_basic_structure(refuges: List[Dict]) -> Dict:
    """
    Verifica l'estructura bàsica dels refugis.
    """
    results = {
        'total': len(refuges),
        'with_coord': 0,
        'with_name': 0,
        'with_surname': 0,
        'with_altitude': 0,
        'with_type': 0,
        'with_links': 0,
        'with_description': 0,
        'with_remarque': 0,
        'with_places': 0,
        'with_info_comp': 0,
        'with_departement': 0,
        'with_region': 0,
    }
    
    for refuge in refuges:
        if refuge.get('coord'):
            results['with_coord'] += 1
        if refuge.get('name'):
            results['with_name'] += 1
        if refuge.get('surname'):
            results['with_surname'] += 1
        if refuge.get('altitude') is not None:
            results['with_altitude'] += 1
        if refuge.get('type'):
            results['with_type'] += 1
        if refuge.get('links') and len(refuge['links']) > 0:
            results['with_links'] += 1
        if refuge.get('description') and len(refuge['description']) > 0:
            results['with_description'] += 1
        if refuge.get('remarque') and len(refuge['remarque']) > 0:
            results['with_remarque'] += 1
        if refuge.get('places') is not None:
            results['with_places'] += 1
        if refuge.get('info_comp'):
            results['with_info_comp'] += 1
        if refuge.get('departement'):
            results['with_departement'] += 1
        if refuge.get('region'):
            results['with_region'] += 1
    
    return results


def check_merged_refuges(refuges: List[Dict]) -> Dict:
    """
    Verifica característiques específiques dels refugis fusionats.
    """
    results = {
        'with_both_names': 0,  # Tenen name i surname
        'with_multiple_links': 0,  # Més d'un link
        'with_refuges_info_link': 0,
        'with_pyrenees_refuges_link': 0,
        'with_both_links': 0,
        'with_multiple_descriptions': 0,
        'with_multiple_remarques': 0,
    }
    
    for refuge in refuges:
        # Name i surname
        if refuge.get('name') and refuge.get('surname'):
            results['with_both_names'] += 1
        
        # Links
        links = refuge.get('links', [])
        if len(links) > 1:
            results['with_multiple_links'] += 1
        
        has_refuges_info = any('refuges.info' in link for link in links)
        has_pyrenees_refuges = any('pyrenees-refuges.com' in link for link in links)
        
        if has_refuges_info:
            results['with_refuges_info_link'] += 1
        if has_pyrenees_refuges:
            results['with_pyrenees_refuges_link'] += 1
        if has_refuges_info and has_pyrenees_refuges:
            results['with_both_links'] += 1
        
        # Descriptions i remarques
        if len(refuge.get('description', [])) > 1:
            results['with_multiple_descriptions'] += 1
        if len(refuge.get('remarque', [])) > 1:
            results['with_multiple_remarques'] += 1
    
    return results


def check_data_quality(refuges: List[Dict]) -> Dict:
    """
    Verifica la qualitat de les dades després del merge.
    """
    results = {
        'null_coords': [],
        'null_altitude': [],
        'null_type': [],
        'null_departement': [],
        'no_links': [],
        'no_description': [],
        'type_fermee': 0,
        'type_non_garde': 0,
        'type_garde': 0,
        'type_other': [],
    }
    
    for i, refuge in enumerate(refuges):
        name = refuge.get('name', f'Refugi #{i}')
        
        if not refuge.get('coord'):
            results['null_coords'].append(name)
        
        if refuge.get('altitude') is None:
            results['null_altitude'].append(name)
        
        if not refuge.get('type'):
            results['null_type'].append(name)
        else:
            refuge_type = refuge['type']
            if refuge_type == 'fermée':
                results['type_fermee'] += 1
            elif refuge_type == 'non gardé':
                results['type_non_garde'] += 1
            elif refuge_type == 'gardé':
                results['type_garde'] += 1
            else:
                results['type_other'].append((name, refuge_type))
        
        if not refuge.get('departement'):
            results['null_departement'].append(name)
        
        if not refuge.get('links') or len(refuge['links']) == 0:
            results['no_links'].append(name)
        
        if not refuge.get('description') or len(refuge['description']) == 0:
            results['no_description'].append(name)
    
    return results


def compare_counts(original_count: int, final_count: int, merged_pairs: int) -> Dict:
    """
    Compara els números esperats amb els obtinguts.
    """
    expected_count = original_count - merged_pairs
    difference = final_count - expected_count
    
    return {
        'original_count': original_count,
        'merged_pairs': merged_pairs,
        'expected_count': expected_count,
        'final_count': final_count,
        'difference': difference,
        'is_correct': abs(difference) <= 2  # Tolerància de 2
    }


def print_report(original_file: str, merged_file: str):
    """
    Genera i imprimeix un informe complet de verificació.
    """
    print("=" * 80)
    print("INFORME DE VERIFICACIÓ DEL MERGE DE REFUGIS DUPLICATS")
    print("=" * 80)
    print()
    
    # Carregar dades
    print("Carregant dades...")
    original_refuges = load_json(original_file)
    merged_refuges = load_json(merged_file)
    print(f"  ✓ Refugis originals: {len(original_refuges)}")
    print(f"  ✓ Refugis després del merge: {len(merged_refuges)}")
    print()
    
    # Comparació de números
    print("-" * 80)
    print("1. COMPARACIÓ DE NÚMEROS")
    print("-" * 80)
    
    # Assumim que s'han processat aproximadament 123 parelles
    expected_pairs = 123
    counts = compare_counts(len(original_refuges), len(merged_refuges), expected_pairs)
    
    print(f"Refugis originals:        {counts['original_count']}")
    print(f"Parelles esperades:       ~{counts['merged_pairs']}")
    print(f"Refugis esperats:         ~{counts['expected_count']}")
    print(f"Refugis obtinguts:        {counts['final_count']}")
    print(f"Diferència:               {counts['difference']}")
    
    if counts['is_correct']:
        print("✓ La reducció està dins de la tolerància esperada (±2)")
    else:
        print(f"⚠ La reducció no està dins de la tolerància! Diferència: {counts['difference']}")
    
    reduction = len(original_refuges) - len(merged_refuges)
    print(f"\nReducció total:           {reduction} refugis eliminats")
    print()
    
    # Estructura bàsica
    print("-" * 80)
    print("2. ESTRUCTURA BÀSICA")
    print("-" * 80)
    
    structure = check_basic_structure(merged_refuges)
    total = structure['total']
    
    print(f"Total de refugis:         {total}")
    print(f"Amb coordenades:          {structure['with_coord']} ({structure['with_coord']/total*100:.1f}%)")
    print(f"Amb nom (name):           {structure['with_name']} ({structure['with_name']/total*100:.1f}%)")
    print(f"Amb sobrenom (surname):   {structure['with_surname']} ({structure['with_surname']/total*100:.1f}%)")
    print(f"Amb altitud:              {structure['with_altitude']} ({structure['with_altitude']/total*100:.1f}%)")
    print(f"Amb tipus:                {structure['with_type']} ({structure['with_type']/total*100:.1f}%)")
    print(f"Amb links:                {structure['with_links']} ({structure['with_links']/total*100:.1f}%)")
    print(f"Amb description:          {structure['with_description']} ({structure['with_description']/total*100:.1f}%)")
    print(f"Amb remarque:             {structure['with_remarque']} ({structure['with_remarque']/total*100:.1f}%)")
    print(f"Amb places:               {structure['with_places']} ({structure['with_places']/total*100:.1f}%)")
    print(f"Amb info_comp:            {structure['with_info_comp']} ({structure['with_info_comp']/total*100:.1f}%)")
    print(f"Amb departement:          {structure['with_departement']} ({structure['with_departement']/total*100:.1f}%)")
    print(f"Amb region:               {structure['with_region']} ({structure['with_region']/total*100:.1f}%)")
    print()
    
    # Característiques de refugis fusionats
    print("-" * 80)
    print("3. CARACTERÍSTIQUES DELS REFUGIS FUSIONATS")
    print("-" * 80)
    
    merged = check_merged_refuges(merged_refuges)
    
    print(f"Amb name i surname:       {merged['with_both_names']}")
    print(f"  (Indica refugis que probablement han estat fusionats)")
    print()
    print(f"Amb múltiples links:      {merged['with_multiple_links']}")
    print(f"Amb link refuges.info:    {merged['with_refuges_info_link']}")
    print(f"Amb link pyrenees-ref.:   {merged['with_pyrenees_refuges_link']}")
    print(f"Amb ambdós links:         {merged['with_both_links']}")
    print(f"  (Els refugis fusionats haurien de tenir ambdós links)")
    print()
    print(f"Amb múltiples descrip.:   {merged['with_multiple_descriptions']}")
    print(f"Amb múltiples remarques:  {merged['with_multiple_remarques']}")
    print()
    
    # Qualitat de les dades
    print("-" * 80)
    print("4. QUALITAT DE LES DADES")
    print("-" * 80)
    
    quality = check_data_quality(merged_refuges)
    
    print(f"Refugis sense coordenades:  {len(quality['null_coords'])}")
    print(f"Refugis sense altitud:      {len(quality['null_altitude'])}")
    print(f"Refugis sense tipus:        {len(quality['null_type'])}")
    print(f"Refugis sense departement:  {len(quality['null_departement'])}")
    print(f"Refugis sense links:        {len(quality['no_links'])}")
    print(f"Refugis sense description:  {len(quality['no_description'])}")
    print()
    
    print("Distribució de tipus:")
    print(f"  - fermée:                 {quality['type_fermee']}")
    print(f"  - non gardé:              {quality['type_non_garde']}")
    print(f"  - gardé:                  {quality['type_garde']}")
    print(f"  - altres:                 {len(quality['type_other'])}")
    print()
    
    # Mostrar exemples de refugis fusionats
    print("-" * 80)
    print("5. EXEMPLES DE REFUGIS FUSIONATS")
    print("-" * 80)
    
    examples_shown = 0
    for refuge in merged_refuges:
        if refuge.get('name') and refuge.get('surname'):
            links = refuge.get('links', [])
            has_both_links = (
                any('refuges.info' in link for link in links) and
                any('pyrenees-refuges.com' in link for link in links)
            )
            
            if has_both_links and examples_shown < 5:
                print(f"\nRefugi: {refuge['name']}")
                print(f"  Surname: {refuge.get('surname')}")
                print(f"  Altitud: {refuge.get('altitude')}")
                print(f"  Tipus: {refuge.get('type')}")
                print(f"  Places: {refuge.get('places')}")
                print(f"  Descriptions: {len(refuge.get('description', []))}")
                print(f"  Remarques: {len(refuge.get('remarque', []))}")
                print(f"  Links: {len(links)}")
                examples_shown += 1
    
    print()
    print("=" * 80)
    print("FI DE L'INFORME")
    print("=" * 80)
    
    # Guardar informe en fitxer
    with open('informe_verificacio_merge.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("INFORME DE VERIFICACIÓ DEL MERGE DE REFUGIS DUPLICATS\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Refugis originals: {len(original_refuges)}\n")
        f.write(f"Refugis després del merge: {len(merged_refuges)}\n")
        f.write(f"Reducció: {len(original_refuges) - len(merged_refuges)} refugis\n\n")
        
        f.write("ESTRUCTURA:\n")
        for key, value in structure.items():
            if key != 'total':
                f.write(f"  {key}: {value} ({value/total*100:.1f}%)\n")
        
        f.write("\nREFUGIS FUSIONATS:\n")
        for key, value in merged.items():
            f.write(f"  {key}: {value}\n")
        
        f.write("\nQUALITAT:\n")
        f.write(f"  Sense coordenades: {len(quality['null_coords'])}\n")
        f.write(f"  Sense altitud: {len(quality['null_altitude'])}\n")
        f.write(f"  Sense tipus: {len(quality['null_type'])}\n")
        f.write(f"  Sense departement: {len(quality['null_departement'])}\n")
        
        if quality['null_coords']:
            f.write("\n\nREFUGIS SENSE COORDENADES:\n")
            for name in quality['null_coords'][:20]:
                f.write(f"  - {name}\n")
        
        if quality['null_altitude']:
            f.write("\n\nREFUGIS SENSE ALTITUD:\n")
            for name in quality['null_altitude'][:20]:
                f.write(f"  - {name}\n")
    
    print("\n✓ Informe guardat a informe_verificacio_merge.txt")


def main():
    """Funció principal."""
    print_report(
        'data_refugis_updated_types.json',
        'data_refugis_sense_repetits.json'
    )


if __name__ == '__main__':
    main()
