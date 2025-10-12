#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per verificar els refugis units amb la nova estructura d'arrays
"""

import json

def verificar_refugis_v2():
    # Carregar el fitxer resultat
    with open('data_refugis.json', 'r', encoding='utf-8') as f:
        refugis = json.load(f)
    
    print(f"Total de refugis: {len(refugis)}")
    
    # Comptar refugis units (tenen 'surname')
    refugis_units = [r for r in refugis if 'surname' in r]
    refugis_nomes_un_doc = [r for r in refugis if 'surname' not in r]
    
    print(f"Refugis units: {len(refugis_units)}")
    print(f"Refugis només d'un document: {len(refugis_nomes_un_doc)}")
    
    # Verificar estructura d'arrays per refugis units
    print("\nExemples de refugis units amb arrays:")
    for i, refugi in enumerate(refugis_units[:3]):
        print(f"\n{i+1}. {refugi['name']} (surname: {refugi['surname']})")
        print(f"   Description: {type(refugi['description']).__name__} amb {len(refugi['description'])} elements")
        print(f"   Remarque: {type(refugi['remarque']).__name__} amb {len(refugi['remarque'])} elements")
        print(f"   Links: {len(refugi.get('links', []))} enllaços")
        if refugi['description']:
            print(f"   Primera descripció: {refugi['description'][0][:100]}...")
        if refugi['remarque']:
            print(f"   Primera remarque: {refugi['remarque'][0][:100]}...")
    
    # Verificar estructura d'arrays per refugis d'un sol document
    print(f"\nExemples de refugis d'un sol document:")
    for i, refugi in enumerate(refugis_nomes_un_doc[:3]):
        print(f"\n{i+1}. {refugi['name']}")
        print(f"   Description: {type(refugi['description']).__name__} amb {len(refugi['description'])} elements")
        print(f"   Remarque: {type(refugi['remarque']).__name__} amb {len(refugi['remarque'])} elements")
        print(f"   Region: {refugi.get('region')}")
        print(f"   Departement: {refugi.get('departement')}")
        print(f"   Modified_at: {refugi.get('modified_at')}")
        
        # Verificar info_comp complet
        info_comp_keys = set(refugi['info_comp'].keys())
        required_keys = {'cheminee', 'bois', 'eau', 'matelas', 'couchage', 'bas_flancs', 'lits', 'mezzanine/etage'}
        missing_keys = required_keys - info_comp_keys
        if missing_keys:
            print(f"   ❌ Info_comp incomplet, falten: {missing_keys}")
        else:
            print(f"   ✅ Info_comp complet amb {len(info_comp_keys)} camps")
    
    # Verificar que tots els refugis tenen camps obligatoris amb la nova estructura
    camps_obligatoris = ['coord', 'name', 'info_comp', 'altitude', 'places', 'description', 'remarque']
    refugis_amb_camps_faltants = []
    
    for i, refugi in enumerate(refugis):
        camps_faltants = [camp for camp in camps_obligatoris if camp not in refugi]
        if camps_faltants:
            refugis_amb_camps_faltants.append((i, camps_faltants))
        
        # Verificar que description i remarque són arrays
        for field in ['description', 'remarque']:
            if field in refugi and not isinstance(refugi[field], list):
                print(f"❌ Refugi {i} ({refugi['name']}): {field} no és array: {type(refugi[field])}")
    
    if refugis_amb_camps_faltants:
        print(f"\n❌ Refugis amb camps faltants: {len(refugis_amb_camps_faltants)}")
        for i, (idx, camps) in enumerate(refugis_amb_camps_faltants[:3]):
            print(f"   {i+1}. Refugi {idx}: Falten {camps}")
    else:
        print(f"\n✅ Tots els refugis tenen els camps obligatoris")
    
    # Estadístiques finals
    total_descriptions = sum(len(r['description']) for r in refugis)
    total_remarques = sum(len(r['remarque']) for r in refugis)
    
    print(f"\nEstadístiques finals:")
    print(f"   Total elements description: {total_descriptions}")
    print(f"   Total elements remarque: {total_remarques}")
    print(f"   Refugis amb múltiples descriptions: {len([r for r in refugis if len(r['description']) > 1])}")
    print(f"   Refugis amb múltiples remarques: {len([r for r in refugis if len(r['remarque']) > 1])}")

if __name__ == "__main__":
    verificar_refugis_v2()