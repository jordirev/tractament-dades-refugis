#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per unir dos fitxers JSON de refugis de manera intel·ligent
Versió actualitzada amb description i remarque com a arrays
"""

import json
import math
import re
from typing import Dict, List, Tuple, Any, Optional

def normalize_name(name: str) -> str:
    """Normalitza un nom per comparacions més flexibles"""
    # Convertir a minúscules
    normalized = name.lower()
    # Eliminar accents i caràcters especials comuns
    replacements = {
        'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
        'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
        'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
        'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
        'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
        'ñ': 'n', 'ç': 'c'
    }
    
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    
    # Eliminar articles i paraules comunes
    words_to_remove = ['cabane', 'refuge', 'abri', 'refugi', 'refugio', 'cayolar', 'orri', 'orry']
    for word in words_to_remove:
        normalized = re.sub(rf'\b{word}\b', '', normalized)
    
    # Eliminar espais extra i caràcters especials
    normalized = re.sub(r'[^a-z0-9\s]', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized

def calculate_distance(coord1: Dict, coord2: Dict) -> float:
    """Calcula la distància entre dues coordenades en km"""
    lat1, lon1 = math.radians(coord1['lat']), math.radians(coord1['long'])
    lat2, lon2 = math.radians(coord2['lat']), math.radians(coord2['long'])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radi de la Terra en km
    
    return c * r

def are_names_similar(name1: str, name2: str) -> float:
    """Calcula la similitud entre dos noms (0-1)"""
    norm1 = normalize_name(name1)
    norm2 = normalize_name(name2)
    
    # Si són exactament iguals després de normalitzar
    if norm1 == norm2:
        return 1.0
    
    # Si un està contingut dins l'altre
    if norm1 in norm2 or norm2 in norm1:
        return 0.8
    
    # Comparar paraules en comú
    words1 = set(norm1.split())
    words2 = set(norm2.split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def find_potential_matches(refugi1: Dict, refuges2: List[Dict], max_distance_km: float = 2.0) -> List[Tuple[int, float, float]]:
    """Troba possibles coincidències per a un refugi"""
    matches = []
    
    for i, refugi2 in enumerate(refuges2):
        # Calcular similitud de nom
        name_similarity = are_names_similar(refugi1['name'], refugi2['name'])
        
        # Calcular distància geogràfica
        try:
            distance = calculate_distance(refugi1['coord'], refugi2['coord'])
        except (KeyError, TypeError):
            distance = float('inf')
        
        # Si hi ha una similitud mínima de nom o la distància és petita
        if name_similarity > 0.6 or distance < max_distance_km:
            matches.append((i, name_similarity, distance))
    
    # Ordenar per similitud de nom i distància
    matches.sort(key=lambda x: (-x[1], x[2]))
    return matches

def merge_info_comp(info1: Dict, info2: Dict) -> Dict:
    """Uneix dos diccionaris info_comp aplicant OR lògic als camps compartits"""
    # Camps que necessiten OR lògic
    or_fields = ['cheminee', 'bois', 'eau', 'matelas']
    
    # Camps comuns en ambdós documents
    all_fields = set(info1.keys()) | set(info2.keys())
    
    result = {}
    
    for field in all_fields:
        val1 = info1.get(field, 0)
        val2 = info2.get(field, 0)
        
        if field in or_fields:
            # OR lògic: 1 si algun és 1, sinó 0
            result[field] = 1 if (val1 == 1 or val2 == 1) else 0
        else:
            # Per altres camps, prioritzar el valor no zero
            result[field] = val1 if val1 != 0 else val2
    
    return result

def merge_refuges(refugi1: Dict, refugi2: Dict) -> Dict:
    """Uneix dos refugis en un de sol"""
    merged = {}
    
    # Determinar quines coordenades són més precises (més decimals)
    coord1_precision = len(str(refugi1['coord']['lat']).split('.')[-1]) + len(str(refugi1['coord']['long']).split('.')[-1])
    coord2_precision = len(str(refugi2['coord']['lat']).split('.')[-1]) + len(str(refugi2['coord']['long']).split('.')[-1])
    
    if coord1_precision >= coord2_precision:
        merged['coord'] = refugi1['coord']
    else:
        merged['coord'] = refugi2['coord']
    
    # Altitud més alta
    alt1 = refugi1.get('altitude', 0)
    alt2 = refugi2.get('altitude', 0)
    
    # Convertir a int/float si és possible
    try:
        alt1 = float(alt1) if alt1 is not None else 0
    except (ValueError, TypeError):
        alt1 = 0
        
    try:
        alt2 = float(alt2) if alt2 is not None else 0
    except (ValueError, TypeError):
        alt2 = 0
    
    merged['altitude'] = max(alt1, alt2) if alt1 and alt2 else (alt1 or alt2 or 0)
    
    # Noms: refugi1 com surname, refugi2 com name
    merged['name'] = refugi2['name']
    merged['surname'] = refugi1['name']
    
    # Unir llistes
    for list_field in ['links', 'type']:
        list1 = refugi1.get(list_field, [])
        list2 = refugi2.get(list_field, [])
        
        # Convertir a llista si és string
        if isinstance(list1, str):
            list1 = [list1]
        if isinstance(list2, str):
            list2 = [list2]
        
        # Unir eliminant duplicats
        merged[list_field] = list(set(list1 + list2))
    
    # Unir camps de text com a arrays
    for text_field in ['description', 'remarque']:
        text1 = refugi1.get(text_field, '')
        text2 = refugi2.get(text_field, '')
        
        # Crear array amb els texts no buits
        texts = []
        if text1:
            texts.append(text1)
        if text2:
            texts.append(text2)
        
        merged[text_field] = texts
    
    # Places: el més gran
    places1 = refugi1.get('places', 0)
    places2 = refugi2.get('places', 0)
    
    # Convertir a int si és possible
    try:
        places1 = int(places1) if places1 is not None else 0
    except (ValueError, TypeError):
        places1 = 0
        
    try:
        places2 = int(places2) if places2 is not None else 0
    except (ValueError, TypeError):
        places2 = 0
    
    merged['places'] = max(places1, places2)
    
    # info_comp: unió intel·ligent
    info1 = refugi1.get('info_comp', {})
    info2 = refugi2.get('info_comp', {})
    merged['info_comp'] = merge_info_comp(info1, info2)
    
    # Camps que només estan en un dels documents
    all_fields = set(refugi1.keys()) | set(refugi2.keys())
    processed_fields = {'coord', 'altitude', 'name', 'links', 'type', 'description', 'remarque', 'places', 'info_comp'}
    
    for field in all_fields - processed_fields:
        val1 = refugi1.get(field)
        val2 = refugi2.get(field)
        merged[field] = val1 if val1 is not None else val2
    
    return merged

def complete_refuge_fields(refugi: Dict, from_which_source: str) -> Dict:
    """Completa els camps que falten en un refugi"""
    # Camps obligatoris de info_comp
    required_info_comp = {
        'cheminee': 0,
        'bois': 0,
        'eau': 0,
        'matelas': 0,
        'couchage': 0,
        'bas_flancs': 0,
        'lits': 0,
        'mezzanine/etage': 0
    }
    
    # Si no té info_comp, crear-lo buit
    if 'info_comp' not in refugi:
        refugi['info_comp'] = {}
    
    # Completar camps que falten
    for field, default_value in required_info_comp.items():
        if field not in refugi['info_comp']:
            refugi['info_comp'][field] = default_value
    
    # Camps opcionals
    if 'region' not in refugi:
        refugi['region'] = None
    if 'departement' not in refugi:
        refugi['departement'] = None
    if 'modified_at' not in refugi:
        refugi['modified_at'] = None
    
    # Convertir description i remarque a arrays si són strings
    for field in ['description', 'remarque']:
        if field in refugi:
            if isinstance(refugi[field], str):
                refugi[field] = [refugi[field]] if refugi[field] else []
        else:
            refugi[field] = []
    
    return refugi

def main():
    print("Carregant fitxers JSON...")
    
    # Carregar els dos fitxers
    with open('refusInfo_normalized_types_services.json', 'r', encoding='utf-8') as f:
        data1 = json.load(f)
        refuges1 = data1['nodes']
    
    with open('refusPyrenees_definitiu.json', 'r', encoding='utf-8') as f:
        refuges2 = json.load(f)
    
    print(f"Refugis en refusInfo: {len(refuges1)}")
    print(f"Refugis en refusPyrenees: {len(refuges2)}")
    
    merged_refuges = []
    used_indices_2 = set()
    uncertain_matches = []
    
    print("\nBuscant parelles de refugis...")
    
    for i, refugi1 in enumerate(refuges1):
        if i % 100 == 0:
            print(f"Processant refugi {i+1}/{len(refuges1)}")
        
        # Buscar possibles coincidències
        matches = find_potential_matches(refugi1, refuges2)
        
        best_match = None
        for j, name_sim, distance in matches:
            if j in used_indices_2:
                continue
            
            refugi2 = refuges2[j]
            
            # Criteris per acceptar una coincidència
            if name_sim > 0.8 or (name_sim > 0.6 and distance < 1.0):
                best_match = j
                break
            elif name_sim > 0.5 and distance < 0.5:
                # Coincidència incerta
                uncertain_matches.append({
                    'refugi1': refugi1['name'],
                    'refugi2': refugi2['name'],
                    'name_similarity': name_sim,
                    'distance_km': distance,
                    'coord1': refugi1['coord'],
                    'coord2': refugi2['coord'],
                    'altitude1': refugi1.get('altitude'),
                    'altitude2': refugi2.get('altitude')
                })
                best_match = j
                break
        
        if best_match is not None:
            # Unir els refugis
            refugi2 = refuges2[best_match]
            merged_refugi = merge_refuges(refugi1, refugi2)
            merged_refuges.append(merged_refugi)
            used_indices_2.add(best_match)
        else:
            # Refugi només en document 1
            refugi1_completed = complete_refuge_fields(refugi1.copy(), 'refusInfo')
            merged_refuges.append(refugi1_completed)
    
    # Afegir refugis que només estan en document 2
    for i, refugi2 in enumerate(refuges2):
        if i not in used_indices_2:
            refugi2_completed = complete_refuge_fields(refugi2.copy(), 'refusPyrenees')
            merged_refuges.append(refugi2_completed)
    
    print(f"\nResultats:")
    print(f"Total refugis en el resultat: {len(merged_refuges)}")
    print(f"Refugis només de refusInfo: {len(refuges1) - len([r for r in merged_refuges if 'surname' in r])}")
    print(f"Refugis només de refusPyrenees: {len(refuges2) - len(used_indices_2)}")
    print(f"Refugis units: {len(used_indices_2)}")
    
    # Mostrar coincidències incertes
    if uncertain_matches:
        print(f"\nCoincidències incertes ({len(uncertain_matches)}):")
        for match in uncertain_matches[:10]:  # Mostrar només les primeres 10
            print(f"- '{match['refugi1']}' ↔ '{match['refugi2']}'")
            print(f"  Similitud: {match['name_similarity']:.2f}, Distància: {match['distance_km']:.2f}km")
            print(f"  Alt1: {match['altitude1']}, Alt2: {match['altitude2']}")
            print()
    
    # Guardar el resultat
    output_file = 'data_refugis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_refuges, f, ensure_ascii=False, indent=2)
    
    print(f"\nResultat guardat a: {output_file}")
    
    return uncertain_matches

if __name__ == "__main__":
    uncertain = main()