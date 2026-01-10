#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per seleccionar 100 refugis variats del dataset.
Selecciona refugis amb varietat en: places, type, info_comp, links, altitude, region, departement.
"""

import json
import random
from typing import List, Dict, Any
from collections import defaultdict


def load_refuges(filepath: str) -> List[Dict[str, Any]]:
    """Carrega els refugis del fitxer JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def categorize_refuges(refuges: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Categoritza els refugis per diferents criteris per assegurar varietat."""
    
    categories = {
        'by_type': defaultdict(list),
        'by_altitude': defaultdict(list),
        'by_places': defaultdict(list),
        'by_info_comp': defaultdict(list),
        'by_links': defaultdict(list),
        'by_region': defaultdict(list),
        'by_departement': defaultdict(list)
    }
    
    for refuge in refuges:
        # Per tipus
        refuge_type = refuge.get('type', 'unknown')
        categories['by_type'][refuge_type].append(refuge)
        
        # Per altitud (en rangs)
        altitude = refuge.get('altitude')
        if altitude:
            if altitude < 1000:
                alt_range = 'baixa'
            elif altitude < 1500:
                alt_range = 'mitjana-baixa'
            elif altitude < 2000:
                alt_range = 'mitjana'
            elif altitude < 2500:
                alt_range = 'mitjana-alta'
            else:
                alt_range = 'alta'
            categories['by_altitude'][alt_range].append(refuge)
        else:
            categories['by_altitude']['null'].append(refuge)
        
        # Per places
        places = refuge.get('places')
        if places is None:
            categories['by_places']['null'].append(refuge)
        elif places == 0:
            categories['by_places']['0'].append(refuge)
        elif places <= 5:
            categories['by_places']['1-5'].append(refuge)
        elif places <= 10:
            categories['by_places']['6-10'].append(refuge)
        elif places <= 20:
            categories['by_places']['11-20'].append(refuge)
        else:
            categories['by_places']['20+'].append(refuge)
        
        # Per info_comp (per diversitat de camps)
        info_comp = refuge.get('info_comp')
        if info_comp:
            num_features = sum(1 for v in info_comp.values() if v == 1)
            if num_features == 0:
                categories['by_info_comp']['0'].append(refuge)
            elif num_features <= 2:
                categories['by_info_comp']['1-2'].append(refuge)
            elif num_features <= 4:
                categories['by_info_comp']['3-4'].append(refuge)
            else:
                categories['by_info_comp']['5+'].append(refuge)
        else:
            categories['by_info_comp']['null'].append(refuge)
        
        # Per links
        links = refuge.get('links', [])
        if not links:
            categories['by_links']['0'].append(refuge)
        elif len(links) == 1:
            categories['by_links']['1'].append(refuge)
        elif len(links) == 2:
            categories['by_links']['2'].append(refuge)
        else:
            categories['by_links']['3+'].append(refuge)
        
        # Per regió
        region = refuge.get('region')
        if region:
            categories['by_region'][region].append(refuge)
        else:
            categories['by_region']['null'].append(refuge)
        
        # Per departament
        dept = refuge.get('departement')
        if dept:
            categories['by_departement'][dept].append(refuge)
        else:
            categories['by_departement']['null'].append(refuge)
    
    return categories


def select_varied_refuges(refuges: List[Dict[str, Any]], n: int = 100) -> List[Dict[str, Any]]:
    """
    Selecciona n refugis variats basant-se en múltiples criteris.
    Prioritza la diversitat en tipus i altres atributs.
    """
    
    categories = categorize_refuges(refuges)
    selected = []
    selected_ids = set()
    
    # Primer, assegurem que tenim els 4 tipus principals
    required_types = [
        'non gardé',
        'fermée',
        'cabane ouverte mais ocupee par le berger l ete',
        'orri'
    ]
    
    # Seleccionem refugis de cada tipus
    refuges_per_type = n // len(required_types)
    
    for refuge_type in required_types:
        type_refuges = categories['by_type'].get(refuge_type, [])
        
        if not type_refuges:
            print(f"Advertència: No s'han trobat refugis del tipus '{refuge_type}'")
            continue
        
        # Dins de cada tipus, seleccionem amb varietat
        type_selected = select_varied_from_list(
            type_refuges, 
            refuges_per_type,
            selected_ids
        )
        selected.extend(type_selected)
        selected_ids.update(id(r) for r in type_selected)
    
    # Si no arribem a n refugis, omplim amb refugis variats dels restants
    if len(selected) < n:
        remaining = [r for r in refuges if id(r) not in selected_ids]
        additional_needed = n - len(selected)
        
        additional = select_varied_from_list(
            remaining,
            additional_needed,
            selected_ids
        )
        selected.extend(additional)
    
    # Si encara tenim més de n (per arrodoniments), retornem només n
    return selected[:n]


def select_varied_from_list(
    refuges: List[Dict[str, Any]], 
    n: int,
    exclude_ids: set
) -> List[Dict[str, Any]]:
    """
    Selecciona n refugis d'una llista assegurant varietat en altitud, places, etc.
    """
    # Filtrem refugis ja seleccionats
    available = [r for r in refuges if id(r) not in exclude_ids]
    
    if len(available) <= n:
        return available
    
    # Estratègia: seleccionem proporcionalment de diferents categories
    selected = []
    
    # Barrejem per tenir aleatorietat
    random.shuffle(available)
    
    # Intentem tenir varietat d'altituds, places, etc.
    altitude_groups = defaultdict(list)
    for refuge in available:
        alt = refuge.get('altitude', 0)
        if alt < 1500:
            group = 'baixa'
        elif alt < 2000:
            group = 'mitjana'
        else:
            group = 'alta'
        altitude_groups[group].append(refuge)
    
    # Seleccionem proporcionalment
    per_group = n // len(altitude_groups)
    remainder = n % len(altitude_groups)
    
    for i, (group, group_refuges) in enumerate(altitude_groups.items()):
        count = per_group + (1 if i < remainder else 0)
        selected.extend(random.sample(group_refuges, min(count, len(group_refuges))))
    
    # Si no en tenim prou, omplim amb els restants
    if len(selected) < n:
        remaining = [r for r in available if r not in selected]
        selected.extend(random.sample(remaining, min(n - len(selected), len(remaining))))
    
    return selected[:n]


def process_refuge(refuge: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processa un refugi:
    - Elimina el camp 'remarque'
    - Converteix 'description' d'array a string (primer element)
    """
    processed = refuge.copy()
    
    # Eliminar remarque
    if 'remarque' in processed:
        del processed['remarque']
    
    # Convertir description d'array a string
    if 'description' in processed and isinstance(processed['description'], list):
        if processed['description']:
            processed['description'] = processed['description'][0]
        else:
            processed['description'] = None
    
    return processed


def print_selection_statistics(selected_refuges: List[Dict[str, Any]]):
    """Imprimeix estadístiques de la selecció."""
    print("\n" + "="*60)
    print("ESTADÍSTIQUES DE LA SELECCIÓ")
    print("="*60)
    
    # Comptar per tipus
    type_counts = defaultdict(int)
    for r in selected_refuges:
        type_counts[r.get('type', 'unknown')] += 1
    
    print("\nDistribució per tipus:")
    for type_name, count in sorted(type_counts.items()):
        print(f"  {type_name}: {count}")
    
    # Places
    places_values = [r.get('places') for r in selected_refuges if r.get('places') is not None]
    print(f"\nPlaces:")
    print(f"  Refugis amb places definits: {len(places_values)}")
    print(f"  Refugis amb places = null: {100 - len(places_values)}")
    if places_values:
        print(f"  Min places: {min(places_values)}")
        print(f"  Max places: {max(places_values)}")
        print(f"  Mitjana places: {sum(places_values) / len(places_values):.1f}")
    
    # Altitud
    altitude_values = [r.get('altitude') for r in selected_refuges if r.get('altitude') is not None]
    print(f"\nAltitud:")
    print(f"  Refugis amb altitud definida: {len(altitude_values)}")
    if altitude_values:
        print(f"  Min altitud: {min(altitude_values)} m")
        print(f"  Max altitud: {max(altitude_values)} m")
        print(f"  Mitjana altitud: {sum(altitude_values) / len(altitude_values):.0f} m")
    
    # Links
    links_counts = defaultdict(int)
    for r in selected_refuges:
        num_links = len(r.get('links', []))
        links_counts[num_links] += 1
    
    print(f"\nLinks:")
    for num, count in sorted(links_counts.items()):
        print(f"  {num} links: {count} refugis")
    
    # Info_comp
    info_comp_counts = []
    for r in selected_refuges:
        info = r.get('info_comp')
        if info:
            count = sum(1 for v in info.values() if v == 1)
            info_comp_counts.append(count)
    
    print(f"\nInfo_comp:")
    print(f"  Refugis amb info_comp: {len(info_comp_counts)}")
    if info_comp_counts:
        print(f"  Min característiques: {min(info_comp_counts)}")
        print(f"  Max característiques: {max(info_comp_counts)}")
        print(f"  Mitjana característiques: {sum(info_comp_counts) / len(info_comp_counts):.1f}")
    
    # Regions
    regions = defaultdict(int)
    for r in selected_refuges:
        region = r.get('region', 'null')
        regions[region if region else 'null'] += 1
    
    print(f"\nRegions:")
    for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {region}: {count}")
    
    # Departaments
    depts = defaultdict(int)
    for r in selected_refuges:
        dept = r.get('departement', 'null')
        depts[dept if dept else 'null'] += 1
    
    print(f"\nDepartaments:")
    for dept, count in sorted(depts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {dept}: {count}")
    
    print("\n" + "="*60)


def main():
    """Funció principal."""
    # Establim una llavor per reproducibilitat (opcional)
    random.seed(42)
    
    input_file = 'data_refugis_sense_repetits.json'
    output_file = 'data_demo.json'
    
    print(f"Carregant refugis de {input_file}...")
    refuges = load_refuges(input_file)
    print(f"Total refugis carregats: {len(refuges)}")
    
    print("\nSeleccionant 100 refugis variats...")
    selected = select_varied_refuges(refuges, n=100)
    print(f"Refugis seleccionats: {len(selected)}")
    
    print("\nProcessant refugis (eliminant remarque i convertint description)...")
    processed = [process_refuge(r) for r in selected]
    
    # Mostrar estadístiques
    print_selection_statistics(processed)
    
    print(f"\nGuardant refugis processats a {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Procés completat!")
    print(f"  - {len(processed)} refugis guardats a {output_file}")


if __name__ == '__main__':
    main()
