#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import datetime

def extract_refuge_names_from_file(file_path):
    """
    Extreu els noms dels refugis d'un fitxer de text
    """
    refuge_names = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Buscar patrons com "1. Nom del refugi" o "21. Nom del refugi"
        pattern = r'^\s*\d+\.\s+(.+?)$'
        matches = re.findall(pattern, content, re.MULTILINE)
        
        for match in matches:
            # Netejar el nom del refugi
            refuge_name = match.strip()
            refuge_names.add(refuge_name)
            
    except Exception as e:
        print(f"Error llegint {file_path}: {e}")
        
    return refuge_names

def extract_refuge_data_from_alta_capacitat(file_path):
    """
    Extreu la informació completa dels refugis del fitxer refugis_alta_capacitat.txt
    """
    refuges_data = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Dividir el contingut en blocs per refugi
        # Cada refugi comença amb un número seguit d'un punt
        refuge_blocks = re.split(r'\n\s*\d+\.\s+', content)
        
        # El primer bloc conté la capçalera, l'ignorem
        for i, block in enumerate(refuge_blocks[1:], 1):
            lines = block.strip().split('\n')
            if not lines:
                continue
                
            # La primera línia és el nom del refugi
            refuge_name = lines[0].strip()
            
            # Recollir tota la informació del refugi
            refuge_info = {
                'name': refuge_name,
                'full_block': f"{i}. {block.strip()}"
            }
            
            # Extraure informació específica
            for line in lines[1:]:
                line = line.strip()
                if line.startswith('Capacitat estiu:'):
                    refuge_info['cap_estiu'] = line.replace('Capacitat estiu:', '').strip()
                elif line.startswith('Capacitat hivern:'):
                    refuge_info['cap_hivern'] = line.replace('Capacitat hivern:', '').strip()
                elif line.startswith('Capacitat màxima:'):
                    refuge_info['cap_maxima'] = line.replace('Capacitat màxima:', '').strip()
                elif line.startswith('Regió:'):
                    refuge_info['regio'] = line.replace('Regió:', '').strip()
                elif line.startswith('Altitud:'):
                    refuge_info['altitud'] = line.replace('Altitud:', '').strip()
                elif line.startswith('Tipus:'):
                    refuge_info['tipus'] = line.replace('Tipus:', '').strip()
                elif line.startswith('URL:'):
                    refuge_info['url'] = line.replace('URL:', '').strip()
            
            refuges_data[refuge_name] = refuge_info
            
    except Exception as e:
        print(f"Error llegint {file_path}: {e}")
        
    return refuges_data

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Fitxers d'entrada
    refugis_alta_capacitat_file = os.path.join(script_dir, "refugis_alta_capacitat.txt")
    refugis_guardats_file = os.path.join(script_dir, "refugisPyrinees_refus_guardats.txt")
    
    # Fitxer de sortida
    output_file = os.path.join(script_dir, "refugis_alta_capacitat_comparats.txt")
    
    print("Comparant fitxers de refugis...")
    print("=" * 60)
    print(f"Fitxer 1 (alta capacitat): {refugis_alta_capacitat_file}")
    print(f"Fitxer 2 (guardats): {refugis_guardats_file}")
    print(f"Fitxer de sortida: {output_file}")
    print("=" * 60)
    
    # Extreure dades dels refugis d'alta capacitat
    refuges_alta_capacitat = extract_refuge_data_from_alta_capacitat(refugis_alta_capacitat_file)
    
    # Extreure noms dels refugis guardats
    refuges_guardats = extract_refuge_names_from_file(refugis_guardats_file)
    
    print(f"Refugis amb alta capacitat: {len(refuges_alta_capacitat)}")
    print(f"Refugis guardats: {len(refuges_guardats)}")
    
    # Trobar refugis que estan en alta capacitat però no en guardats
    refuges_no_guardats = []
    
    for refuge_name in refuges_alta_capacitat:
        if refuge_name not in refuges_guardats:
            refuges_no_guardats.append(refuges_alta_capacitat[refuge_name])
    
    print(f"Refugis no guardats (filtrats): {len(refuges_no_guardats)}")
    
    if not refuges_no_guardats:
        print("Tots els refugis d'alta capacitat ja estan en la llista de guardats.")
        return
    
    # Ordenar per capacitat màxima
    refuges_no_guardats.sort(key=lambda x: int(re.findall(r'\d+', x.get('cap_maxima', '0'))[0]) if re.findall(r'\d+', x.get('cap_maxima', '0')) else 0, reverse=True)
    
    # Crear el contingut per escriure al fitxer
    content_lines = []
    content_lines.append("REFUGIS AMB CAPACITAT SUPERIOR A 15 PERSONES QUE NO ESTAN GUARDATS")
    content_lines.append("=" * 70)
    content_lines.append(f"Data d'anàlisi: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    content_lines.append(f"Total de refugis no guardats: {len(refuges_no_guardats)}")
    content_lines.append("")
    content_lines.append("Ordenats per capacitat màxima (de major a menor)")
    content_lines.append("=" * 70)
    content_lines.append("")
    
    for i, refuge in enumerate(refuges_no_guardats, 1):
        content_lines.append(f"{i:2}. {refuge['name']}")
        content_lines.append(f"    Capacitat estiu: {refuge.get('cap_estiu', 'No especificada')}")
        content_lines.append(f"    Capacitat hivern: {refuge.get('cap_hivern', 'No especificada')}")
        content_lines.append(f"    Capacitat màxima: {refuge.get('cap_maxima', 'No especificada')}")
        content_lines.append(f"    Regió: {refuge.get('regio', 'No especificada')}")
        content_lines.append(f"    Altitud: {refuge.get('altitud', 'No especificada')}")
        content_lines.append(f"    Tipus: {refuge.get('tipus', 'No especificat')}")
        content_lines.append(f"    URL: {refuge.get('url', 'No especificada')}")
        content_lines.append("")
    
    # Estadístiques
    content_lines.append("=" * 70)
    content_lines.append("ESTADÍSTIQUES:")
    content_lines.append("=" * 70)
    
    # Distribució per rangs de capacitat
    ranges = {
        '16-30': 0,
        '31-50': 0,
        '51-100': 0,
        '101+': 0
    }
    
    for refuge in refuges_no_guardats:
        cap_str = refuge.get('cap_maxima', '0')
        cap_nums = re.findall(r'\d+', cap_str)
        cap = int(cap_nums[0]) if cap_nums else 0
        
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
    content_lines.append("TOP 5 refugis no guardats amb més capacitat:")
    for i, refuge in enumerate(refuges_no_guardats[:5], 1):
        content_lines.append(f"  {i}. {refuge['name']} - {refuge.get('cap_maxima', 'No especificada')}")
    
    # Escriure el contingut al fitxer
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(content_lines))
        print(f"\nResultats guardats a: {output_file}")
    except Exception as e:
        print(f"Error en escriure el fitxer: {e}")
    
    # Mostrar per pantalla
    print(f"\nRefugis NO GUARDATS amb capacitat superior a 15:")
    print()
    
    for i, refuge in enumerate(refuges_no_guardats[:10], 1):
        print(f"{i:2}. {refuge['name']}")
        print(f"    Capacitat màxima: {refuge.get('cap_maxima', 'No especificada')}")
        print(f"    Regió: {refuge.get('regio', 'No especificada')}")
        print(f"    URL: {refuge.get('url', 'No especificada')}")
        print()
    
    if len(refuges_no_guardats) > 10:
        print(f"... i {len(refuges_no_guardats) - 10} refugis més (vegeu el fitxer complet)")
    
    print(f"\nRESUM:")
    print(f"Total de refugis no guardats: {len(refuges_no_guardats)}")
    if refuges_no_guardats:
        first_refuge = refuges_no_guardats[0]
        print(f"Capacitat més alta (no guardat): {first_refuge.get('cap_maxima', 'No especificada')} ({first_refuge['name']})")

if __name__ == "__main__":
    main()