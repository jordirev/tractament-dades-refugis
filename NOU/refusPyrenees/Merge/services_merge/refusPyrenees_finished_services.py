#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

def parse_classification_file(classification_file):
    """
    Parseja el fitxer de classificació dels valors de couchage
    i retorna un diccionari amb els noms dels refugis agrupats per categoria
    """
    groups = {
        'MATELAS': set(),
        'BAS FLANCS': set(),
        'SOL/TERRE': set(),
        'LITS': set(),
        'MEZZANINE/ÉTAGE': set(),
        'NÉGATIF': set(),
        'NUMÉRIC': set(),
        'NUMÉRIC_0': set()  # Grup especial per als valors numèrics "0"
    }
    
    try:
        with open(classification_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        current_group = None
        current_valor = None
        in_refugis_section = False
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            
            # Detectar grup actual
            if line.startswith('GRUP: '):
                current_group = line.replace('GRUP: ', '').strip()
                in_refugis_section = False
                continue
            
            # Detectar valor actual
            if line.startswith('VALOR: '):
                current_valor = line.split("'")[1] if "'" in line else ""
                in_refugis_section = False
                continue
            
            # Detectar inici de secció de refugis
            if line == 'Refugis:':
                in_refugis_section = True
                continue
            
            # Processar noms de refugis
            if in_refugis_section and line.startswith('- '):
                refuge_name = line[2:].strip()  # Eliminar "- "
                if current_group and refuge_name:
                    groups[current_group].add(refuge_name)
                    
                    # Afegir també al grup especial NUMÉRIC_0 si correspon
                    if current_group == 'NUMÉRIC' and current_valor == '0':
                        groups['NUMÉRIC_0'].add(refuge_name)
            
            # Finalitzar secció de refugis si trobem línies que no són refugis
            elif in_refugis_section and line and not line.startswith('- ') and not line.startswith('      '):
                # Línies com "... i 14 refugis més" ens fan sortir de la secció de refugis
                in_refugis_section = False
        
        # Convertir sets a llistes per facilitar la depuració
        for group in groups:
            groups[group] = list(groups[group])
        
        print(f"Grups processats des del fitxer de classificació:")
        for group, refuges in groups.items():
            print(f"- {group}: {len(refuges)} refugis")
        
        return groups
        
    except FileNotFoundError:
        print(f"Error: No s'ha trobat el fitxer {classification_file}")
        return {}
    except Exception as e:
        print(f"Error processant el fitxer de classificació: {e}")
        return {}

def process_services(input_file, output_file):
    """
    Processa els serveis dels refugis segons les especificacions:
    - Normalitza els valors de cheminee, bois i eau a 0 o 1
    - Afegeix info_eau quan sigui necessari
    - Mou tots els camps de serveis a "info_comp"
    - Elimina els camps originals del nivell principal
    """
    
    # Valors que han de ser 0 per cada camp
    cheminee_zero_values = ["", "Non", "non"]
    bois_zero_values = ["", "Non", "non", "?", "à apporter", "Pas de bois à proximité"]
    eau_zero_values = ["", "Non", "non", "?", "Pas de source ", "Pas à proximité immédiate", "Non. "]
    
    # Valors d'eau que necessiten info_eau
    eau_info_values = [
        "A la source distante de 100 m ",
        "abreuvoir (eau captée) en contrebas",
        "Source sous la cabane près du ",
        "ruisseau à proximité ",
        "Oui + source à proximité",
        "source en amont",
        "Source à 5min difficilement tr",
        "Torrent à proximité",
        "15min",
        "Source à environ 500m au sud sur le GR",
        "sí, a 160m",
        "Ruisseau proche",
        "A proximité ",
        "pas en hiver. ",
        "Source captée à 5mn vers l'Est",
        "Oui mais le robinet à l'intéri",
        "Torrent"
    ]
    
    try:
        # Llegir el fitxer JSON d'entrada
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        processed_count = 0
        info_eau_count = 0
        
        # Processar cada refugi
        for refuge in data:
            # Obtenir els valors originals
            cheminee_original = refuge.get("cheminee", "")
            bois_original = refuge.get("bois", "")
            eau_original = refuge.get("eau", "")
            couchage_original = refuge.get("couchage", "")
            
            # Processar cheminee
            if cheminee_original in cheminee_zero_values:
                cheminee_processed = 0
            else:
                cheminee_processed = 1
            
            # Processar bois
            if bois_original in bois_zero_values:
                bois_processed = 0
            else:
                bois_processed = 1
            
            # Processar eau
            if eau_original in eau_zero_values:
                eau_processed = 0
            else:
                eau_processed = 1
                # Afegir info_eau si el valor està en la llista específica
                if eau_original in eau_info_values:
                    refuge["info_eau"] = eau_original
                    info_eau_count += 1
            
            # Crear el camp info_comp amb els valors processats
            refuge["info_comp"] = {
                "cheminee": cheminee_processed,
                "bois": bois_processed,
                "eau": eau_processed,
                "couchage": couchage_original  # No es toca
            }
            
            # Eliminar els camps originals del nivell principal
            if "cheminee" in refuge:
                del refuge["cheminee"]
            if "bois" in refuge:
                del refuge["bois"]
            if "eau" in refuge:
                del refuge["eau"]
            if "couchage" in refuge:
                del refuge["couchage"]
            
            processed_count += 1
        
        # Guardar el resultat
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Processament completat!")
        print(f"- Refugis processats: {processed_count}")
        print(f"- Refugis amb info_eau: {info_eau_count}")
        print(f"- Fitxer guardat com: {output_file}")
        
        # Estadístiques dels valors normalitzats
        cheminee_1 = sum(1 for r in data if r.get("info_comp", {}).get("cheminee") == 1)
        cheminee_0 = sum(1 for r in data if r.get("info_comp", {}).get("cheminee") == 0)
        bois_1 = sum(1 for r in data if r.get("info_comp", {}).get("bois") == 1)
        bois_0 = sum(1 for r in data if r.get("info_comp", {}).get("bois") == 0)
        eau_1 = sum(1 for r in data if r.get("info_comp", {}).get("eau") == 1)
        eau_0 = sum(1 for r in data if r.get("info_comp", {}).get("eau") == 0)
        
        print("\nEstadístiques:")
        print(f"- Cheminee: {cheminee_1} (Sí), {cheminee_0} (No)")
        print(f"- Bois: {bois_1} (Sí), {bois_0} (No)")
        print(f"- Eau: {eau_1} (Sí), {eau_0} (No)")
        print(f"- Tots els camps de serveis moguts a 'info_comp'")
        
    except FileNotFoundError:
        print(f"Error: No s'ha trobat el fitxer {input_file}")
    except json.JSONDecodeError:
        print(f"Error: El fitxer {input_file} no és un JSON vàlid")
    except Exception as e:
        print(f"Error inesperat: {e}")

def classify_couchage_value(couchage_value):
    """
    Classifica un valor de couchage segons les paraules clau i patrons
    Retorna una tupla (couchage_binary, matelas, bas_flancs, lits, mezzanine, group)
    """
    if not couchage_value or couchage_value.strip() == "":
        return 0, 0, 0, 0, 0, "EMPTY"
    
    value_lower = couchage_value.lower().strip()
    
    # Patrons per identificar cada grup
    matelas_patterns = ['matelas', 'mousse']
    bas_flancs_patterns = ['bas flanc', 'bat-flanc', 'bat flanc', 'bas-flanc']
    lits_patterns = ['lit', 'sommier', 'couchette', 'superpos']
    mezzanine_patterns = ['mezzanine', 'étage', 'etage', 'plancher']
    
    # Patrons negatius
    negatif_patterns = ['non', 'rien', 'néant', 'neant', 'pas de', 'aucun', 'négatif']
    sol_terre_patterns = ['sol', 'terre', 'béton', 'beton', 'par terre', 'plancher', 'dalle']
    
    # Verificar si és numèric
    try:
        num_value = int(value_lower)
        if num_value == 0:
            return 0, 0, 0, 0, 0, "NUMÉRIC_0"
        else:
            return 1, 0, 0, 0, 0, "NUMÉRIC"
    except ValueError:
        pass
    
    # Verificar patrons negatius primer
    if any(pattern in value_lower for pattern in negatif_patterns):
        # Verificar si no és una excepció com "non mais..."
        if not ('mais' in value_lower or 'but' in value_lower):
            return 0, 0, 0, 0, 0, "NÉGATIF"
    
    # Inicialitzar camps binaris
    matelas = 0
    bas_flancs = 0
    lits = 0
    mezzanine = 0
    
    # Verificar cada tipus d'equipament
    if any(pattern in value_lower for pattern in matelas_patterns):
        # Assegurar-se que no és "sans matelas"
        if not ('sans' in value_lower and 'matelas' in value_lower):
            matelas = 1
    
    if any(pattern in value_lower for pattern in bas_flancs_patterns):
        # Assegurar-se que no és "pas de bat-flanc"
        if not ('pas de' in value_lower or 'sans' in value_lower):
            bas_flancs = 1
    
    if any(pattern in value_lower for pattern in lits_patterns):
        lits = 1
    
    if any(pattern in value_lower for pattern in mezzanine_patterns):
        mezzanine = 1
    
    # Determinar el valor binari de couchage
    if matelas or bas_flancs or lits or mezzanine:
        couchage_binary = 1
        group = "CLASSIFIED"
    elif any(pattern in value_lower for pattern in sol_terre_patterns):
        couchage_binary = 0
        group = "SOL/TERRE"
    else:
        # Valors no classificats - assumir que hi ha algún tipus de couchage
        couchage_binary = 1
        group = "OTHER"
    
    return couchage_binary, matelas, bas_flancs, lits, mezzanine, group

def process_couchage_classification(data, classification_groups):
    """
    Processa els camps de couchage segons la classificació:
    - Crea camps nous: matelas, bas_flancs, lits, mezzanine/etage
    - Modifica el valor de couchage segons els grups
    - Crea info_couchage quan correspon
    """
    
    processed_count = 0
    info_couchage_count = 0
    
    # Crear mapes de noms de refugis per a cada grup (dels que tenim)
    matelas_refuges = set(classification_groups.get('MATELAS', []))
    bas_flancs_refuges = set(classification_groups.get('BAS FLANCS', []))
    lits_refuges = set(classification_groups.get('LITS', []))
    mezzanine_refuges = set(classification_groups.get('MEZZANINE/ÉTAGE', []))
    sol_terre_refuges = set(classification_groups.get('SOL/TERRE', []))
    negatif_refuges = set(classification_groups.get('NÉGATIF', []))
    
    # Estadístiques per grup
    stats = {
        'couchage_0': 0,
        'couchage_1': 0,
        'matelas_1': 0,
        'bas_flancs_1': 0,
        'lits_1': 0,
        'mezzanine_1': 0,
        'info_couchage': 0,
        'classified_by_name': 0,
        'classified_by_value': 0
    }
    
    print(f"\nProcessant classificació de couchage:")
    print(f"- Refugis coneguts amb matelas: {len(matelas_refuges)}")
    print(f"- Refugis coneguts amb bas_flancs: {len(bas_flancs_refuges)}")
    print(f"- Refugis coneguts amb lits: {len(lits_refuges)}")
    print(f"- Refugis coneguts amb mezzanine: {len(mezzanine_refuges)}")
    
    for refuge in data:
        refuge_name = refuge.get("name", "").strip()
        
        # Obtenir el valor actual de couchage
        current_couchage = refuge.get("info_comp", {}).get("couchage", "")
        
        # Estratègia híbrida: primer per nom, després per valor
        classified_by_name = False
        
        # Inicialitzar camps
        new_fields = {
            "matelas": 0,
            "bas_flancs": 0,
            "lits": 0,
            "mezzanine/etage": 0
        }
        
        # 1. Classificació per nom del refugi (prioritària)
        new_couchage_value = None
        
        if refuge_name in sol_terre_refuges or refuge_name in negatif_refuges:
            new_couchage_value = 0
            classified_by_name = True
            stats['classified_by_name'] += 1
        elif refuge_name in (matelas_refuges | bas_flancs_refuges | lits_refuges | mezzanine_refuges):
            new_couchage_value = 1
            classified_by_name = True
            stats['classified_by_name'] += 1
            if current_couchage:
                refuge["info_couchage"] = current_couchage
                info_couchage_count += 1
                stats['info_couchage'] += 1
        
        # Assignar camps específics per nom
        if refuge_name in matelas_refuges:
            new_fields["matelas"] = 1
        if refuge_name in bas_flancs_refuges:
            new_fields["bas_flancs"] = 1
        if refuge_name in lits_refuges:
            new_fields["lits"] = 1
        if refuge_name in mezzanine_refuges:
            new_fields["mezzanine/etage"] = 1
        
        # 2. Si no s'ha classificat per nom, usar classificació per valor
        if not classified_by_name and current_couchage:
            couchage_bin, matelas_val, bas_flancs_val, lits_val, mezzanine_val, group = classify_couchage_value(current_couchage)
            
            new_couchage_value = couchage_bin
            new_fields["matelas"] = matelas_val
            new_fields["bas_flancs"] = bas_flancs_val
            new_fields["lits"] = lits_val
            new_fields["mezzanine/etage"] = mezzanine_val
            
            stats['classified_by_value'] += 1
            
            if couchage_bin == 1 and current_couchage.strip():
                refuge["info_couchage"] = current_couchage
                info_couchage_count += 1
                stats['info_couchage'] += 1
        
        # 3. Si no hi ha valor de couchage, mantenir valor original o assignar 0
        if new_couchage_value is None:
            new_couchage_value = current_couchage if current_couchage else 0
        
        # Actualitzar estadístiques
        if new_couchage_value == 0:
            stats['couchage_0'] += 1
        else:
            stats['couchage_1'] += 1
        
        if new_fields["matelas"]:
            stats['matelas_1'] += 1
        if new_fields["bas_flancs"]:
            stats['bas_flancs_1'] += 1
        if new_fields["lits"]:
            stats['lits_1'] += 1
        if new_fields["mezzanine/etage"]:
            stats['mezzanine_1'] += 1
        
        # Actualitzar info_comp amb els nous camps i el nou valor de couchage
        if "info_comp" not in refuge:
            refuge["info_comp"] = {}
        
        refuge["info_comp"]["couchage"] = new_couchage_value
        refuge["info_comp"].update(new_fields)
        
        processed_count += 1
    
    print(f"\nResultats del processament de couchage:")
    print(f"- Refugis processats: {processed_count}")
    print(f"- Classificats per nom: {stats['classified_by_name']}")
    print(f"- Classificats per valor: {stats['classified_by_value']}")
    print(f"- Refugis amb couchage = 0: {stats['couchage_0']}")
    print(f"- Refugis amb couchage = 1: {stats['couchage_1']}")
    print(f"- Refugis amb matelas = 1: {stats['matelas_1']}")
    print(f"- Refugis amb bas_flancs = 1: {stats['bas_flancs_1']}")
    print(f"- Refugis amb lits = 1: {stats['lits_1']}")
    print(f"- Refugis amb mezzanine/etage = 1: {stats['mezzanine_1']}")
    print(f"- Refugis amb info_couchage: {stats['info_couchage']}")
    
    return processed_count, info_couchage_count

if __name__ == "__main__":
    input_file = "refusPyrenees_finished.json"
    output_file = "refusPyrenees_finished_services.json"
    classification_file = "classificacio_couchage.txt"
    
    # Processar serveis bàsics
    process_services(input_file, output_file)
    
    # Carregar dades per processar couchage
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Carregar grups de classificació
        classification_groups = parse_classification_file(classification_file)
        
        if classification_groups:
            # Processar classificació de couchage
            process_couchage_classification(data, classification_groups)
            
            # Guardar el resultat final
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"\nFitxer final guardat com: {output_file}")
        else:
            print("No s'ha pogut carregar la classificació. Es manté el processament bàsic.")
            
    except Exception as e:
        print(f"Error processant la classificació de couchage: {e}")
