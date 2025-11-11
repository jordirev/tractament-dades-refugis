#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per fer el merge de refugis duplicats identificats a noms_parelles_semblants.txt
Segueix les normes especificades per combinar la informació de dos refugis en un sol.
"""

import json
import re
from typing import Dict, List, Any, Optional


def parse_pairs_file(filepath: str) -> List[tuple]:
    """
    Parseja el fitxer de parelles de refugis amb noms semblants.
    
    Returns:
        List de tuples (nom1, nom2, num_parella)
    """
    pairs = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar totes les parelles
    pattern = r'PARELLA #(\d+)\n={80,}\n(.+?)\n(.+?)\n(?:(.+?)\n)?(?:={80,}|$)'
    matches = re.finditer(pattern, content, re.MULTILINE)
    
    for match in matches:
        num = int(match.group(1))
        names = []
        # Recollir tots els noms de la parella
        for i in range(2, 5):
            name = match.group(i)
            if name and name.strip() and not name.startswith('='):
                names.append(name.strip())
        
        # Si hi ha 2 noms, és una parella simple
        if len(names) == 2:
            pairs.append((names[0], names[1], num))
        # Si hi ha 3 noms, pot ser que el tercer sigui un altre nom alternatiu
        elif len(names) == 3:
            # Afegir les dues primeres com a parella principal
            pairs.append((names[0], names[1], num))
    
    return pairs


def find_refuge_by_name(refuges: List[Dict], name: str) -> Optional[int]:
    """
    Troba l'índex d'un refugi pel seu nom o surname.
    
    Returns:
        Índex del refugi o None si no es troba
    """
    for i, refuge in enumerate(refuges):
        refuge_name = refuge.get('name', '')
        refuge_surname = refuge.get('surname', '')
        
        if refuge_name == name or refuge_surname == name:
            return i
    
    return None


def merge_altitude(alt1: Any, alt2: Any) -> Any:
    """
    Escull l'altitud més precisa (valor més numèric no 0).
    """
    if alt1 is None:
        return alt2
    if alt2 is None:
        return alt1
    
    # Si ambdós són valors, escollir el més precís (més gran en precisió)
    try:
        val1 = float(alt1) if alt1 else 0
        val2 = float(alt2) if alt2 else 0
        
        # Si un és 0, escollir l'altre
        if val1 == 0:
            return alt2
        if val2 == 0:
            return alt1
        
        # Escollir el valor més precís (més dígits o més gran)
        if val1 != val2:
            return alt2 if val2 > val1 else alt1
        return alt1
    except:
        return alt1 if alt1 else alt2


def merge_info_comp(info1: Optional[Dict], info2: Optional[Dict]) -> Dict:
    """
    Unió OR dels atributs d'info_comp.
    Si qualsevol dels refugis té un atribut a 1, el resultat és 1.
    """
    if not info1:
        return info2 if info2 else {}
    if not info2:
        return info1
    
    result = {}
    all_keys = set(info1.keys()) | set(info2.keys())
    
    for key in all_keys:
        val1 = info1.get(key, 0)
        val2 = info2.get(key, 0)
        # Unió OR: si qualsevol és 1, el resultat és 1
        result[key] = 1 if (val1 == 1 or val2 == 1) else 0
    
    return result


def merge_type(type1: Optional[str], type2: Optional[str]) -> Optional[str]:
    """
    Regles per TYPE:
    - Si qualsevol == "fermée", resultat = "fermée"
    - Si un == "non gardé", escollir l'altre
    - Prioritza informació més específica
    """
    if not type1:
        return type2
    if not type2:
        return type1
    
    # Si qualsevol és "fermée"
    if type1 == "fermée" or type2 == "fermée":
        return "fermée"
    
    # Si un és "non gardé", escollir l'altre
    if type1 == "non gardé" and type2 != "non gardé":
        return type2
    if type2 == "non gardé" and type1 != "non gardé":
        return type1
    
    # Prioritzar el primer si són iguals o no hi ha cap regla especial
    return type1


def merge_places(places1: Any, places2: Any) -> Any:
    """
    Escull el valor més gran (capacitat màxima).
    Si un és null, escull el valor no null.
    """
    if places1 is None:
        return places2
    if places2 is None:
        return places1
    
    try:
        val1 = int(places1) if places1 else 0
        val2 = int(places2) if places2 else 0
        return max(val1, val2)
    except:
        return places1 if places1 else places2


def merge_lists(list1: Optional[List], list2: Optional[List]) -> List:
    """
    Unió de dues llistes sense duplicats.
    Ordre: primer list1, després list2.
    """
    if not list1:
        return list2 if list2 else []
    if not list2:
        return list1
    
    result = list(list1)
    for item in list2:
        if item not in result:
            result.append(item)
    
    return result


def merge_descriptions(desc1: Optional[List], desc2: Optional[List]) -> List:
    """
    Unió de descriptions mantenint l'ordre:
    primer description de refuges.info, després de pyrenees-refuges
    """
    result = []
    if desc1:
        result.extend(desc1)
    if desc2:
        result.extend(desc2)
    return result


def choose_non_null(val1: Any, val2: Any) -> Any:
    """
    Escull el valor no null. Si ambdós són null, retorna None.
    """
    if val1 is not None:
        return val1
    return val2


def merge_refuges(refuge1: Dict, refuge2: Dict, from_refuges_info: bool = True) -> Dict:
    """
    Fa el merge de dos refugis segons les normes especificades.
    
    Args:
        refuge1: Primer refugi (generalment de refuges.info)
        refuge2: Segon refugi (generalment de pyrenees-refuges)
        from_refuges_info: True si refuge1 és de refuges.info
    
    Returns:
        Refugi resultant del merge
    """
    merged = {}
    
    # 1. COORDENADES - Utilitzar les de refuges.info (refuge1 si from_refuges_info)
    if from_refuges_info:
        merged['coord'] = refuge1.get('coord')
    else:
        merged['coord'] = refuge2.get('coord')
    
    # 2. ALTITUD - Escollir la més precisa
    merged['altitude'] = merge_altitude(
        refuge1.get('altitude'),
        refuge2.get('altitude')
    )
    
    # 4. NAME I SURNAME
    if from_refuges_info:
        merged['name'] = refuge1.get('name')
        merged['surname'] = refuge2.get('name') or refuge2.get('surname')
    else:
        merged['name'] = refuge2.get('name')
        merged['surname'] = refuge1.get('name') or refuge1.get('surname')
    
    # 8. LINKS - Unió de tots els links
    merged['links'] = merge_lists(
        refuge1.get('links'),
        refuge2.get('links')
    )
    
    # 6. TYPE
    merged['type'] = merge_type(
        refuge1.get('type'),
        refuge2.get('type')
    )
    
    # 9. DESCRIPTION - Unió en ordre
    merged['description'] = merge_descriptions(
        refuge1.get('description'),
        refuge2.get('description')
    )
    
    # 10. REMARQUE - Unió en ordre
    merged['remarque'] = merge_descriptions(
        refuge1.get('remarque'),
        refuge2.get('remarque')
    )
    
    # 7. PLACES - Escollir el valor més gran
    merged['places'] = merge_places(
        refuge1.get('places'),
        refuge2.get('places')
    )
    
    # 3. INFO_COMP - Unió OR
    merged['info_comp'] = merge_info_comp(
        refuge1.get('info_comp'),
        refuge2.get('info_comp')
    )
    
    # 11. MODIFIED_AT - Escollir el no null
    merged['modified_at'] = choose_non_null(
        refuge1.get('modified_at'),
        refuge2.get('modified_at')
    )
    
    # 5. REGION - Escollir el no null
    merged['region'] = choose_non_null(
        refuge1.get('region'),
        refuge2.get('region')
    )
    
    # 5. DEPARTEMENT - Escollir el no null
    merged['departement'] = choose_non_null(
        refuge1.get('departement'),
        refuge2.get('departement')
    )
    
    # 12. INFO_COUCHAGE - Escollir el no null
    merged['info_couchage'] = choose_non_null(
        refuge1.get('info_couchage'),
        refuge2.get('info_couchage')
    )
    
    # 12. INFO_EAU - Escollir el no null
    merged['info_eau'] = choose_non_null(
        refuge1.get('info_eau'),
        refuge2.get('info_eau')
    )
    
    # Copiar qualsevol altre camp que pugui existir
    for key in refuge1.keys():
        if key not in merged:
            merged[key] = choose_non_null(refuge1.get(key), refuge2.get(key))
    
    for key in refuge2.keys():
        if key not in merged:
            merged[key] = refuge2[key]
    
    return merged


def main():
    """
    Funció principal que executa el merge de refugis duplicats.
    """
    print("=== MERGE DE REFUGIS DUPLICATS ===\n")
    
    # Llegir el fitxer de parelles
    print("1. Llegint parelles de refugis duplicats...")
    pairs = parse_pairs_file('noms_parelles_semblants.txt')
    print(f"   Trobades {len(pairs)} parelles\n")
    
    # Llegir el fitxer de dades
    print("2. Llegint dades de refugis...")
    with open('data_refugis_updated_types.json', 'r', encoding='utf-8') as f:
        refuges = json.load(f)
    print(f"   Carregats {len(refuges)} refugis\n")
    
    # Processar cada parella
    print("3. Processant parelles i fent merge...")
    merged_count = 0
    not_found = []
    indices_to_remove = set()
    merged_refuges = []
    
    for name1, name2, pair_num in pairs:
        idx1 = find_refuge_by_name(refuges, name1)
        idx2 = find_refuge_by_name(refuges, name2)
        
        if idx1 is None or idx2 is None:
            not_found.append((pair_num, name1, name2, idx1, idx2))
            print(f"   ⚠ Parella #{pair_num}: No trobat - '{name1}' (idx:{idx1}) / '{name2}' (idx:{idx2})")
            continue
        
        # Determinar quin és de refuges.info (té link de refuges.info)
        refuge1 = refuges[idx1]
        refuge2 = refuges[idx2]
        
        from_refuges_info = True
        if refuge1.get('links'):
            if any('refuges.info' in link for link in refuge1['links']):
                from_refuges_info = True
            elif refuge2.get('links') and any('refuges.info' in link for link in refuge2['links']):
                from_refuges_info = False
        
        # Fer el merge
        merged = merge_refuges(refuge1, refuge2, from_refuges_info)
        merged_refuges.append(merged)
        
        # Marcar per eliminar
        indices_to_remove.add(idx1)
        indices_to_remove.add(idx2)
        
        merged_count += 1
        if merged_count % 10 == 0:
            print(f"   Processades {merged_count} parelles...")
    
    print(f"\n   ✓ Merge completat: {merged_count} parelles")
    print(f"   ⚠ No trobades: {len(not_found)} parelles\n")
    
    # Crear la llista final
    print("4. Creant llista final de refugis...")
    final_refuges = []
    
    # Afegir refugis que no s'han fusionat
    for i, refuge in enumerate(refuges):
        if i not in indices_to_remove:
            final_refuges.append(refuge)
    
    # Afegir refugis fusionats
    final_refuges.extend(merged_refuges)
    
    print(f"   Total refugis originals: {len(refuges)}")
    print(f"   Total refugis eliminats (fusionats): {len(indices_to_remove)}")
    print(f"   Total refugis resultants: {len(final_refuges)}")
    print(f"   (Esperats: {len(refuges)} - {len(indices_to_remove)} + {merged_count} = {len(refuges) - len(indices_to_remove) + merged_count})\n")
    
    # Guardar resultats
    print("5. Guardant resultats...")
    with open('data_refugis_sense_repetits.json', 'w', encoding='utf-8') as f:
        json.dump(final_refuges, f, ensure_ascii=False, indent=2)
    print("   ✓ Guardat a data_refugis_sense_repetits.json\n")
    
    # Guardar informe de parelles no trobades
    if not_found:
        print("6. Guardant informe de parelles no trobades...")
        with open('parelles_no_trobades.txt', 'w', encoding='utf-8') as f:
            f.write("PARELLES NO TROBADES\n")
            f.write("=" * 80 + "\n\n")
            for pair_num, name1, name2, idx1, idx2 in not_found:
                f.write(f"Parella #{pair_num}\n")
                f.write(f"  Nom 1: {name1} (índex: {idx1})\n")
                f.write(f"  Nom 2: {name2} (índex: {idx2})\n\n")
        print(f"   ✓ Informe guardat a parelles_no_trobades.txt\n")
    
    print("=== PROCÉS COMPLETAT ===")
    print(f"\nResum:")
    print(f"  - Parelles processades: {merged_count}/{len(pairs)}")
    print(f"  - Refugis resultants: {len(final_refuges)}")
    print(f"  - Reducció: {len(refuges)} → {len(final_refuges)} ({len(indices_to_remove)} eliminats)")


if __name__ == '__main__':
    main()
