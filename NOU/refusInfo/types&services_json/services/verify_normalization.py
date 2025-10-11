#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificació per comprovar que:
1. Tots els camps info_comp tenen només valors 0 o 1
2. Tots els refugis amb places_matelas=1 tenen el missatge de matalassos en la descripció
"""

import json
import re

def verificar_camps_info_comp():
    """Verifica que tots els camps info_comp siguin 0 o 1."""
    with open('refusInfo_normalized_types_services.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print('VERIFICACIÓ DELS CAMPS INFO_COMP')
    print('=================================')
    
    fields = ['manque_un_mur', 'cheminee', 'poele', 'couvertures', 'latrines', 'bois', 'eau', 'places_matelas']
    invalid_found = False
    
    for field in fields:
        invalid_count = 0
        invalid_examples = []
        
        for node in data['nodes']:
            if 'info_comp' in node:
                val = node['info_comp'].get(field)
                if val is not None and val not in [0, 1]:
                    invalid_count += 1
                    if len(invalid_examples) < 3:  # Guardar només els primers 3 exemples
                        invalid_examples.append({
                            'id': node['id'],
                            'nom': node['nom'],
                            'valor': val
                        })
                    invalid_found = True
        
        if invalid_count == 0:
            print(f'✅ {field}: tots els valors són 0 o 1')
        else:
            print(f'❌ {field}: {invalid_count} valors invàlids')
            for example in invalid_examples:
                print(f'   - ID {example["id"]} ({example["nom"]}): valor = {example["valor"]}')
    
    print()
    return not invalid_found, data

def verificar_missatges_matelas(data):
    """Verifica que tots els refugis amb places_matelas=1 tinguin informació sobre matalassos."""
    print('VERIFICACIÓ MISSATGES MATELAS')
    print('==============================')
    
    refugis_matelas = 0
    refugis_sense_info = []
    refugis_amb_places_sur_matelas = 0
    refugis_amb_il_y_a = 0
    
    for node in data['nodes']:
        if 'info_comp' in node and node['info_comp'].get('places_matelas') == 1:
            refugis_matelas += 1
            description = node.get('description', '')
            
            # Buscar patrons 'Il y a X matelas' o 'Places sur Matelas: X'
            has_il_y_a = bool(re.search(r'Il y a \d+ matelas', description))
            has_places_sur = bool(re.search(r'Places sur Matelas:\s*\d+', description))
            
            if has_il_y_a:
                refugis_amb_il_y_a += 1
            if has_places_sur:
                refugis_amb_places_sur_matelas += 1
            
            # Si no té cap dels dos patrons, és un error
            if not has_il_y_a and not has_places_sur:
                refugis_sense_info.append({
                    'id': node['id'],
                    'nom': node['nom'],
                    'description_end': description[-100:] if len(description) > 100 else description
                })
    
    print(f'Total refugis amb places_matelas=1: {refugis_matelas}')
    print(f'Refugis amb "Places sur Matelas: X": {refugis_amb_places_sur_matelas}')
    print(f'Refugis amb "Il y a X matelas": {refugis_amb_il_y_a}')
    print(f'Refugis sense informació de matalassos: {len(refugis_sense_info)}')
    
    if refugis_sense_info:
        print()
        print('❌ Refugis que NO tenen informació de matalassos:')
        for i, refugi in enumerate(refugis_sense_info[:10]):  # Mostrar només els primers 10
            print(f'   {i+1}. ID {refugi["id"]} ({refugi["nom"]})')
            print(f'      Final descripció: ...{refugi["description_end"]}')
            print()
        
        if len(refugis_sense_info) > 10:
            print(f'   ... i {len(refugis_sense_info) - 10} més')
    else:
        print('✅ TOTS els refugis amb places_matelas=1 tenen informació de matalassos')
    
    print()
    return len(refugis_sense_info) == 0

def main():
    """Funció principal."""
    camps_ok, data = verificar_camps_info_comp()
    matelas_ok = verificar_missatges_matelas(data)
    
    print('=== RESUM FINAL ===')
    if camps_ok and matelas_ok:
        print('✅ VERIFICACIÓ COMPLETA: Tot està correcte!')
    else:
        if not camps_ok:
            print('❌ Hi ha valors invàlids en info_comp')
        if not matelas_ok:
            print('❌ Hi ha refugis sense missatge de matalassos')
        print('❌ La verificació ha trobat errors')

if __name__ == "__main__":
    main()