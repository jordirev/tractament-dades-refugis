#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per normalitzar els camps de 'info_comp' en el fitxer JSON dels refugis.

Transformacions aplicades:
- manque_un_mur: "Sans" → 0
- cheminee: "Sans" → 0, 2 o altres números → 1  
- poele: "Sans" → 0, 2 o altres números → 1
- couvertures: "Sans" → 0, 2 o altres números → 1
- latrines: tot valor que no sigui 0 o 1 → 0
- bois: tot valor que no sigui 0 o 1 → 0
- eau: tot valor que no sigui 0 o 1 → 0
- places_matelas: si no és 0, places_matelas → 1 i afegir info a description
"""

import json

def normalize_info_comp(data):
    """
    Normalitza els camps de info_comp segons les regles especificades.
    """
    refugis_processats = 0
    
    for refugi in data.get("nodes", []):
        if "info_comp" not in refugi:
            continue
            
        info_comp = refugi["info_comp"]
        refugis_processats += 1
        
        # Normalitzar manque_un_mur: "Sans" → 0
        if info_comp.get("manque_un_mur") == "Sans":
            info_comp["manque_un_mur"] = 0
            
        # Normalitzar cheminee: "Sans" → 0, números > 1 → 1
        cheminee_val = info_comp.get("cheminee")
        if cheminee_val == "Sans":
            info_comp["cheminee"] = 0
        elif isinstance(cheminee_val, (int, float)) and cheminee_val >= 2:
            info_comp["cheminee"] = 1
        elif isinstance(cheminee_val, str) and cheminee_val.isdigit() and int(cheminee_val) >= 2:
            info_comp["cheminee"] = 1
            
        # Normalitzar poele: "Sans" → 0, números > 1 → 1
        poele_val = info_comp.get("poele")
        if poele_val == "Sans":
            info_comp["poele"] = 0
        elif isinstance(poele_val, (int, float)) and poele_val >= 2:
            info_comp["poele"] = 1
        elif isinstance(poele_val, str) and poele_val.isdigit() and int(poele_val) >= 2:
            info_comp["poele"] = 1
            
        # Normalitzar couvertures: "Sans" → 0, números > 1 → 1
        couvertures_val = info_comp.get("couvertures")
        if couvertures_val == "Sans":
            info_comp["couvertures"] = 0
        elif isinstance(couvertures_val, (int, float)) and couvertures_val >= 2:
            info_comp["couvertures"] = 1
        elif isinstance(couvertures_val, str) and couvertures_val.isdigit() and int(couvertures_val) >= 2:
            info_comp["couvertures"] = 1
            
        # Normalitzar latrines: tot valor que no sigui 0 o 1 → 0
        latrines_val = info_comp.get("latrines")
        if latrines_val not in [0, 1]:
            info_comp["latrines"] = 0
            
        # Normalitzar bois: tot valor que no sigui 0 o 1 → 0
        bois_val = info_comp.get("bois")
        if bois_val not in [0, 1]:
            info_comp["bois"] = 0
            
        # Normalitzar eau: tot valor que no sigui 0 o 1 → 0
        eau_val = info_comp.get("eau")
        if eau_val not in [0, 1]:
            info_comp["eau"] = 0
            
        # Tractar places_matelas: si no és 0, convertir a 1 i afegir info a description
        places_matelas_val = info_comp.get("places_matelas", 0)
        if places_matelas_val != 0:
            # Convertir el valor a número si és string
            if isinstance(places_matelas_val, str):
                try:
                    places_matelas_num = int(places_matelas_val)
                except ValueError:
                    places_matelas_num = 0
            else:
                places_matelas_num = places_matelas_val
                
            if places_matelas_num > 0:
                # Canviar places_matelas a 1
                info_comp["places_matelas"] = 1
                
                # Afegir informació del nombre de matalassos a la descripció només si no existeix ja
                description = refugi.get("description", "")
                matelas_info = f" Il y a {places_matelas_num} matelas."
                
                # Comprovar si ja hi ha informació sobre matalassos per evitar duplicats
                import re
                # Buscar patrons com "Places sur Matelas: X" o "Il y a X matelas"
                if (f"Il y a {places_matelas_num} matelas" not in description and 
                    not re.search(rf"Places sur Matelas:\s*{places_matelas_num}", description)):
                    refugi["description"] = description + matelas_info
    
    print(f"S'han processat {refugis_processats} refugis.")
    return data

def main():
    """Funció principal."""
    input_file = "refusInfo_normalized_with_types.json"
    output_file = "refusInfo_normalized_types_services.json"
    
    print(f"Carregant dades de {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: No s'ha trobat el fitxer {input_file}")
        return
    except json.JSONDecodeError as e:
        print(f"Error al llegir el JSON: {e}")
        return
    
    print("Normalitzant camps info_comp...")
    normalized_data = normalize_info_comp(data)
    
    print(f"Guardant dades normalitzades a {output_file}...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(normalized_data, f, ensure_ascii=False, indent=2)
        print(f"Fitxer {output_file} creat correctament!")
    except Exception as e:
        print(f"Error al guardar el fitxer: {e}")

if __name__ == "__main__":
    main()