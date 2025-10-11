#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from collections import defaultdict

def classify_couchage_values(json_file, output_file):
    """
    Classifica els valors del camp COUCHAGE en grups i troba els refugis
    que contenen cada valor.
    """
    
    try:
        # Llegir el fitxer JSON original
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Diccionari per emmagatzemar els valors i els refugis que els contenen
        couchage_values = defaultdict(list)
        
        # Recopilar tots els valors de couchage amb els noms dels refugis
        for refuge in data:
            couchage_value = refuge.get("couchage", "")
            if couchage_value is None:
                couchage_value = ""
            refuge_name = refuge.get("name", "Nom desconegut")
            couchage_values[str(couchage_value)].append(refuge_name)
        
        # Definir grups de classificació
        groups = {
            "MATELAS": {
                "keywords": ["matelas", "matelas", "mousse"],
                "exclude_keywords": ["sans matelas", "sans matela", "pas de matelas"],
                "description": "Valors que contenen informació sobre matalassos"
            },
            "BAS FLANCS": {
                "keywords": ["bas flanc", "bas-flanc", "bat-flanc", "bas flancs", "bat flancs", "bat-flancs"],
                "exclude_keywords": ["sans bas flanc", "pas de bas flanc"],
                "description": "Valors que contenen informació sobre bat-flancs o bas-flancs"
            },
            "SOL/TERRE": {
                "keywords": ["sol", "terre", "béton", "beton", "par terre", "au sol", "dalles", "plancher"],
                "exclude_keywords": [],
                "description": "Valors relacionats amb dormir al terra, sol o superfícies dures"
            },
            "LITS": {
                "keywords": ["lit", "lits", "superposé", "superpose", "couchette", "sommier"],
                "exclude_keywords": [],
                "description": "Valors relacionats amb llits i estructures de dormir"
            },
            "MEZZANINE/ÉTAGE": {
                "keywords": ["mezzanine", "étage", "etage", "grenier", "plancher", "en haut"],
                "exclude_keywords": [],
                "description": "Valors relacionats amb dormir en alçada o mezzanines"
            },
            "NÉGATIF": {
                "keywords": ["non", "néant", "neant", "rien", "aucun", "négatif", "nada", "pas de"],
                "exclude_keywords": [],
                "description": "Valors que indiquen absència de couchage"
            },
            "NUMÉRIC": {
                "keywords": [],
                "exclude_keywords": [],
                "description": "Valors purament numèrics",
                "special": "numeric"
            }
        }
        
        # Classificar cada valor en grups
        classified_groups = {group_name: defaultdict(list) for group_name in groups.keys()}
        
        for couchage_value, refuge_names in couchage_values.items():
            value_lower = couchage_value.lower()
            
            for group_name, group_info in groups.items():
                if group_name == "NUMÉRIC":
                    # Classificació especial per valors numèrics
                    if couchage_value.strip().isdigit() or re.match(r'^\d+$', couchage_value.strip()):
                        classified_groups[group_name][couchage_value].extend(refuge_names)
                    continue
                
                # Comprovar paraules excloses
                excluded = False
                for exclude_word in group_info["exclude_keywords"]:
                    if exclude_word.lower() in value_lower:
                        excluded = True
                        break
                
                if not excluded:
                    # Comprovar paraules incloses
                    for keyword in group_info["keywords"]:
                        if keyword.lower() in value_lower:
                            classified_groups[group_name][couchage_value].extend(refuge_names)
                            break
        
        # Escriure els resultats
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("CLASSIFICACIÓ DELS VALORS DEL CAMP COUCHAGE\n")
            f.write("=" * 60 + "\n\n")
            
            for group_name, group_data in classified_groups.items():
                if group_data:  # Només mostrar grups que tenen valors
                    f.write(f"GRUP: {group_name}\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"Descripció: {groups[group_name]['description']}\n")
                    f.write(f"Total de valors diferents: {len(group_data)}\n\n")
                    
                    for i, (couchage_value, refuge_names) in enumerate(sorted(group_data.items()), 1):
                        display_value = couchage_value if couchage_value != "" else "[BUIT]"
                        f.write(f"{i:2d}. VALOR: '{display_value}'\n")
                        f.write(f"    Nombre de refugis: {len(refuge_names)}\n")
                        f.write(f"    Refugis:\n")
                        
                        # Mostrar fins a 10 refugis per valor, ordenats alfabèticament
                        sorted_refuges = sorted(set(refuge_names))
                        for j, refuge_name in enumerate(sorted_refuges[:10]):
                            f.write(f"      - {refuge_name}\n")
                        
                        if len(sorted_refuges) > 10:
                            f.write(f"      ... i {len(sorted_refuges) - 10} refugis més\n")
                        
                        f.write("\n")
                    
                    f.write("=" * 60 + "\n\n")
        
        # Estadístiques generals
        total_values = len(couchage_values)
        total_refuges = sum(len(refuges) for refuges in couchage_values.values())
        
        print(f"Classificació completada!")
        print(f"- Total de valors únics de couchage: {total_values}")
        print(f"- Total de refugis analitzats: {total_refuges}")
        print(f"- Grups creats: {len([g for g in classified_groups if classified_groups[g]])}")
        print(f"- Fitxer guardat com: {output_file}")
        
        # Resum de grups
        print("\nResum per grups:")
        for group_name, group_data in classified_groups.items():
            if group_data:
                total_refuges_group = sum(len(refuges) for refuges in group_data.values())
                print(f"- {group_name}: {len(group_data)} valors únics, {total_refuges_group} refugis")
        
    except FileNotFoundError:
        print(f"Error: No s'ha trobat el fitxer {json_file}")
    except json.JSONDecodeError:
        print(f"Error: El fitxer {json_file} no és un JSON vàlid")
    except Exception as e:
        print(f"Error inesperat: {e}")

if __name__ == "__main__":
    input_file = "refusPyrenees_finished.json"
    output_file = "classificacio_couchage.txt"
    
    classify_couchage_values(input_file, output_file)