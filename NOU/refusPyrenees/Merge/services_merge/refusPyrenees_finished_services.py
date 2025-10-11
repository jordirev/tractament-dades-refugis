#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

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

if __name__ == "__main__":
    input_file = "refusPyrenees_finished.json"
    output_file = "refusPyrenees_finished_services.json"
    
    process_services(input_file, output_file)
