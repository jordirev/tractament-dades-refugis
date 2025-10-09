#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import datetime
import os

def find_high_capacity_refuges(json_file_path):
    """
    Troba tots els refugis amb capacitat superior a 15 (estiu o hivern)
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        high_capacity_refuges = []
        
        for item in data:
            cap_ete = item.get('cap_ete', '')
            cap_hiver = item.get('cap_hiver', '')
            
            # Convertir a números per comparar
            cap_ete_num = 0
            cap_hiver_num = 0
            
            # Intentar convertir cap_ete a número
            if cap_ete and str(cap_ete).strip():
                try:
                    # Extraure només números (en cas que hi hagi text addicional)
                    cap_ete_str = str(cap_ete).strip()
                    # Buscar el primer número en la cadena
                    import re
                    numbers = re.findall(r'\d+', cap_ete_str)
                    if numbers:
                        cap_ete_num = int(numbers[0])
                except:
                    cap_ete_num = 0
            
            # Intentar convertir cap_hiver a número
            if cap_hiver and str(cap_hiver).strip():
                try:
                    cap_hiver_str = str(cap_hiver).strip()
                    import re
                    numbers = re.findall(r'\d+', cap_hiver_str)
                    if numbers:
                        cap_hiver_num = int(numbers[0])
                except:
                    cap_hiver_num = 0
            
            # Comprovar si alguna capacitat és superior a 15
            if cap_ete_num > 15 or cap_hiver_num > 15:
                high_capacity_refuges.append({
                    'nom': item.get('name', 'Sense nom'),
                    'cap_ete': str(cap_ete).strip() if cap_ete else '',
                    'cap_hiver': str(cap_hiver).strip() if cap_hiver else '',
                    'cap_ete_num': cap_ete_num,
                    'cap_hiver_num': cap_hiver_num,
                    'max_capacity': max(cap_ete_num, cap_hiver_num),
                    'url': item.get('url', ''),
                    'region': item.get('region', ''),
                    'altitude': item.get('altitude', ''),
                    'type': item.get('type', '')
                })
        
        return high_capacity_refuges
    
    except FileNotFoundError:
        print(f"Error: No s'ha pogut trobar el fitxer {json_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: El fitxer {json_file_path} no és un JSON vàlid")
        return []
    except Exception as e:
        print(f"Error inesperat: {e}")
        return []

def main():
    # Obtenir el directori actual de l'script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Camí relatiu al fitxer JSON (dins de la carpeta merge)
    json_file = os.path.join(script_dir, "..", "merge (Completa + Normal)", "refusPyrinees_merged.json")
    
    # Fitxer de sortida en el mateix directori que l'script
    output_file = os.path.join(script_dir, "refugis_alta_capacitat.txt")
    
    print("Cercant refugis amb capacitat superior a 15...")
    print("=" * 60)
    print(f"Fitxer d'entrada: {json_file}")
    print(f"Fitxer de sortida: {output_file}")
    print("=" * 60)
    
    high_capacity_refuges = find_high_capacity_refuges(json_file)
    
    if not high_capacity_refuges:
        print("No s'han trobat refugis amb capacitat superior a 15.")
        return
    
    # Ordenar per capacitat màxima (de major a menor)
    high_capacity_refuges.sort(key=lambda x: x['max_capacity'], reverse=True)
    
    # Crear el contingut per escriure al fitxer
    content_lines = []
    content_lines.append("REFUGIS AMB CAPACITAT SUPERIOR A 15 PERSONES")
    content_lines.append("=" * 60)
    content_lines.append(f"Data d'anàlisi: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    content_lines.append(f"Fitxer analitzat: {os.path.basename(json_file)}")
    content_lines.append(f"Total de refugis trobats: {len(high_capacity_refuges)}")
    content_lines.append("")
    content_lines.append("Ordenats per capacitat màxima (de major a menor)")
    content_lines.append("=" * 60)
    content_lines.append("")
    
    for i, refuge in enumerate(high_capacity_refuges, 1):
        content_lines.append(f"{i:2}. {refuge['nom']}")
        content_lines.append(f"    Capacitat estiu: {refuge['cap_ete'] if refuge['cap_ete'] else 'No especificada'}")
        content_lines.append(f"    Capacitat hivern: {refuge['cap_hiver'] if refuge['cap_hiver'] else 'No especificada'}")
        content_lines.append(f"    Capacitat màxima: {refuge['max_capacity']} persones")
        content_lines.append(f"    Regió: {refuge['region']}")
        content_lines.append(f"    Altitud: {refuge['altitude']}")
        content_lines.append(f"    Tipus: {refuge['type']}")
        content_lines.append(f"    URL: {refuge['url']}")
        content_lines.append("")
    
    # Estadístiques addicionals
    content_lines.append("=" * 60)
    content_lines.append("ESTADÍSTIQUES:")
    content_lines.append("=" * 60)
    
    # Estadístiques per capacitat
    ranges = {
        '16-30': 0,
        '31-50': 0,
        '51-100': 0,
        '101+': 0
    }
    
    for refuge in high_capacity_refuges:
        cap = refuge['max_capacity']
        if 16 <= cap <= 30:
            ranges['16-30'] += 1
        elif 31 <= cap <= 50:
            ranges['31-50'] += 1
        elif 51 <= cap <= 100:
            ranges['51-100'] += 1
        else:
            ranges['101+'] += 1
    
    content_lines.append("Distribució per rangs de capacitat:")
    for range_name, count in ranges.items():
        content_lines.append(f"  - {range_name} persones: {count} refugis")
    
    # Top 5 refugis amb més capacitat
    content_lines.append("")
    content_lines.append("TOP 5 refugis amb més capacitat:")
    for i, refuge in enumerate(high_capacity_refuges[:5], 1):
        content_lines.append(f"  {i}. {refuge['nom']} - {refuge['max_capacity']} persones")
    
    # Refugis només d'estiu vs només d'hivern vs ambdues temporades
    summer_only = [r for r in high_capacity_refuges if r['cap_ete_num'] > 15 and r['cap_hiver_num'] <= 15]
    winter_only = [r for r in high_capacity_refuges if r['cap_hiver_num'] > 15 and r['cap_ete_num'] <= 15]
    both_seasons = [r for r in high_capacity_refuges if r['cap_ete_num'] > 15 and r['cap_hiver_num'] > 15]
    
    content_lines.append("")
    content_lines.append("Distribució per temporada:")
    content_lines.append(f"  - Només estiu (>15): {len(summer_only)} refugis")
    content_lines.append(f"  - Només hivern (>15): {len(winter_only)} refugis")
    content_lines.append(f"  - Ambdues temporades (>15): {len(both_seasons)} refugis")
    
    # Escriure el contingut al fitxer
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(content_lines))
        print(f"\nResultats guardats a: {output_file}")
    except Exception as e:
        print(f"Error en escriure el fitxer: {e}")
    
    # També mostrar per pantalla
    print(f"S'han trobat {len(high_capacity_refuges)} refugis amb capacitat superior a 15:")
    print()
    
    for i, refuge in enumerate(high_capacity_refuges[:10], 1):  # Mostrar només els primers 10
        print(f"{i:2}. {refuge['nom']}")
        print(f"    Capacitat: Estiu={refuge['cap_ete'] if refuge['cap_ete'] else 'N/A'}, Hivern={refuge['cap_hiver'] if refuge['cap_hiver'] else 'N/A'}")
        print(f"    Màxima: {refuge['max_capacity']} persones")
        print(f"    URL: {refuge['url']}")
        print()
    
    if len(high_capacity_refuges) > 10:
        print(f"... i {len(high_capacity_refuges) - 10} refugis més (vegeu el fitxer complet)")
    
    print(f"\nRESUM:")
    print(f"Total de refugis: {len(high_capacity_refuges)}")
    print(f"Capacitat més alta: {high_capacity_refuges[0]['max_capacity']} persones ({high_capacity_refuges[0]['nom']})")

if __name__ == "__main__":
    main()