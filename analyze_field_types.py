#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import datetime
from collections import Counter

def analyze_field_types(json_file_path):
    """
    Analitza els diferents tipus/valors dels camps cheminee, bois, eau, couchage
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Inicialitzar contadors per cada camp
        cheminee_values = []
        bois_values = []
        eau_values = []
        couchage_values = []
        
        # Recórrer tots els elements
        for item in data:
            # Obtenir els valors dels camps (convertir a string i netejar)
            cheminee = str(item.get('cheminee', '')).strip()
            bois = str(item.get('bois', '')).strip()
            eau = str(item.get('eau', '')).strip()
            couchage = str(item.get('couchage', '')).strip()
            
            # Afegir als arrays (incloent valors buits)
            cheminee_values.append(cheminee)
            bois_values.append(bois)
            eau_values.append(eau)
            couchage_values.append(couchage)
        
        # Comptar occurrències
        cheminee_counts = Counter(cheminee_values)
        bois_counts = Counter(bois_values)
        eau_counts = Counter(eau_values)
        couchage_counts = Counter(couchage_values)
        
        return {
            'total_refugis': len(data),
            'cheminee': cheminee_counts,
            'bois': bois_counts,
            'eau': eau_counts,
            'couchage': couchage_counts
        }
    
    except FileNotFoundError:
        print(f"Error: No s'ha pogut trobar el fitxer {json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: El fitxer {json_file_path} no és un JSON vàlid")
        return None
    except Exception as e:
        print(f"Error inesperat: {e}")
        return None

def format_field_analysis(field_name, field_counts):
    """
    Formata l'anàlisi d'un camp específic
    """
    lines = []
    lines.append(f"\n=== CAMP: {field_name.upper()} ===")
    lines.append(f"Total de valors diferents: {len(field_counts)}")
    lines.append("")
    
    # Ordenar per freqüència (més freqüent primer)
    sorted_counts = sorted(field_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (value, count) in enumerate(sorted_counts, 1):
        # Mostrar valor buit com a "(buit)"
        display_value = "(buit)" if value == "" else value
        percentage = (count / sum(field_counts.values())) * 100
        lines.append(f"{i:2}. '{display_value}' - {count} refugis ({percentage:.1f}%)")
    
    return lines

def main():
    json_file = r"c:\Users\jordi\Desktop\UNI\TFG\INFO\NOU\refusPyrenees\Merge\Filtrar merge refus guardats per capacitat\refusPyrinees_merged_filtered.json"
    output_file = r"c:\Users\jordi\Desktop\UNI\TFG\INFO\analisi_camps_refugis_filtrats.txt"
    
    print("Analitzant tipus de valors dels camps cheminee, bois, eau, couchage...")
    print("=" * 70)
    
    results = analyze_field_types(json_file)
    
    if not results:
        print("No s'han pogut analitzar les dades.")
        return
    
    # Crear el contingut per escriure al fitxer
    content_lines = []
    content_lines.append("ANÀLISI DELS TIPUS DE VALORS DELS CAMPS DELS REFUGIS")
    content_lines.append("=" * 70)
    content_lines.append(f"Data d'anàlisi: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    content_lines.append(f"Total de refugis analitzats: {results['total_refugis']}")
    content_lines.append("")
    content_lines.append("Camps analitzats: cheminee, bois, eau, couchage")
    content_lines.append("=" * 70)
    
    # Anàlisi de cada camp
    for field_name in ['cheminee', 'bois', 'eau', 'couchage']:
        field_analysis = format_field_analysis(field_name, results[field_name])
        content_lines.extend(field_analysis)
    
    # Resum final
    content_lines.append("\n" + "=" * 70)
    content_lines.append("RESUM EXECUTIU:")
    content_lines.append("=" * 70)
    
    for field_name in ['cheminee', 'bois', 'eau', 'couchage']:
        field_counts = results[field_name]
        total_values = len(field_counts)
        empty_count = field_counts.get('', 0)
        filled_count = sum(field_counts.values()) - empty_count
        
        content_lines.append(f"\n{field_name.upper()}:")
        content_lines.append(f"  - Valors diferents: {total_values}")
        content_lines.append(f"  - Refugis amb dades: {filled_count}")
        content_lines.append(f"  - Refugis sense dades: {empty_count}")
        content_lines.append(f"  - Percentatge cobertura: {(filled_count/results['total_refugis']*100):.1f}%")
    
    # Escriure el contingut al fitxer
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(content_lines))
        print(f"\nResultats guardats a: {output_file}")
    except Exception as e:
        print(f"Error en escriure el fitxer: {e}")
    
    # També mostrar per pantalla un resum
    print(f"\nRESUM DE L'ANÀLISI:")
    print(f"Total de refugis: {results['total_refugis']}")
    
    for field_name in ['cheminee', 'bois', 'eau', 'couchage']:
        field_counts = results[field_name]
        total_values = len(field_counts)
        print(f"\nCamp '{field_name}':")
        print(f"  - Valors diferents: {total_values}")
        print(f"  - Valors més freqüents:")
        
        # Mostrar els 3 valors més freqüents
        sorted_counts = sorted(field_counts.items(), key=lambda x: x[1], reverse=True)
        for i, (value, count) in enumerate(sorted_counts[:3], 1):
            display_value = "(buit)" if value == "" else value
            percentage = (count / sum(field_counts.values())) * 100
            print(f"    {i}. '{display_value}': {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    main()