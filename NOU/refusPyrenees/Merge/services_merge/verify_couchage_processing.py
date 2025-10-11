#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from collections import defaultdict

def verify_couchage_processing(json_file):
    """
    Verifica que el processament de couchage s'hagi aplicat correctament
    """
    print("VERIFICACIÓ DEL PROCESSAMENT DE COUCHAGE")
    print("=" * 60)
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Total de refugis carregats: {len(data)}")
        
        # Contadors per verificar l'estructura
        stats = {
            'total_refugis': len(data),
            'info_comp_present': 0,
            'couchage_0': 0,
            'couchage_1': 0,
            'couchage_other': 0,
            'matelas_1': 0,
            'bas_flancs_1': 0,
            'lits_1': 0,
            'mezzanine_etage_1': 0,
            'info_couchage_present': 0,
            'info_eau_present': 0,
            'cheminee_binary': 0,
            'bois_binary': 0,
            'eau_binary': 0,
            'all_fields_present': 0
        }
        
        missing_fields = []
        invalid_values = []
        examples = {
            'couchage_0': [],
            'couchage_1': [],
            'matelas_1': [],
            'bas_flancs_1': [],
            'lits_1': [],
            'mezzanine_etage_1': [],
            'info_couchage': []
        }
        
        for i, refuge in enumerate(data):
            refuge_name = refuge.get('name', f'Refugi #{i}')
            
            # Verificar presència d'info_comp
            if 'info_comp' not in refuge:
                missing_fields.append(f"{refuge_name}: Manca 'info_comp'")
                continue
            
            stats['info_comp_present'] += 1
            info_comp = refuge['info_comp']
            
            # Verificar camps obligatoris dins d'info_comp
            required_fields = ['cheminee', 'bois', 'eau', 'couchage', 'matelas', 'bas_flancs', 'lits', 'mezzanine/etage']
            missing_in_refuge = []
            
            for field in required_fields:
                if field not in info_comp:
                    missing_in_refuge.append(field)
            
            if missing_in_refuge:
                missing_fields.append(f"{refuge_name}: Manquen camps {missing_in_refuge}")
                continue
            
            stats['all_fields_present'] += 1
            
            # Verificar valors de couchage
            couchage_val = info_comp['couchage']
            if couchage_val == 0:
                stats['couchage_0'] += 1
                if len(examples['couchage_0']) < 3:
                    examples['couchage_0'].append(refuge_name)
            elif couchage_val == 1:
                stats['couchage_1'] += 1
                if len(examples['couchage_1']) < 3:
                    examples['couchage_1'].append(refuge_name)
            else:
                stats['couchage_other'] += 1
                invalid_values.append(f"{refuge_name}: couchage={couchage_val} (no és 0 o 1)")
            
            # Verificar camps binaris
            for field in ['matelas', 'bas_flancs', 'lits']:
                val = info_comp[field]
                if val == 1:
                    stats[f'{field}_1'] += 1
                    if len(examples[f'{field}_1']) < 3:
                        examples[f'{field}_1'].append(refuge_name)
                elif val != 0:
                    invalid_values.append(f"{refuge_name}: {field}={val} (no és 0 o 1)")
            
            # Verificar mezzanine/etage
            mez_val = info_comp['mezzanine/etage']
            if mez_val == 1:
                stats['mezzanine_etage_1'] += 1
                if len(examples['mezzanine_etage_1']) < 3:
                    examples['mezzanine_etage_1'].append(refuge_name)
            elif mez_val != 0:
                invalid_values.append(f"{refuge_name}: mezzanine/etage={mez_val} (no és 0 o 1)")
            
            # Verificar camps de serveis bàsics (han de ser binaris)
            for field in ['cheminee', 'bois', 'eau']:
                val = info_comp[field]
                if val in [0, 1]:
                    stats[f'{field}_binary'] += 1
                else:
                    invalid_values.append(f"{refuge_name}: {field}={val} (no és 0 o 1)")
            
            # Verificar info_couchage
            if 'info_couchage' in refuge:
                stats['info_couchage_present'] += 1
                if len(examples['info_couchage']) < 3:
                    examples['info_couchage'].append(f"{refuge_name}: '{refuge['info_couchage']}'")
            
            # Verificar info_eau
            if 'info_eau' in refuge:
                stats['info_eau_present'] += 1
        
        # Mostrar resultats
        print(f"\n📊 ESTADÍSTIQUES GENERALS:")
        print(f"- Refugis amb info_comp: {stats['info_comp_present']}/{stats['total_refugis']}")
        print(f"- Refugis amb tots els camps: {stats['all_fields_present']}/{stats['total_refugis']}")
        
        print(f"\n🏠 VALORS DE COUCHAGE:")
        print(f"- Couchage = 0: {stats['couchage_0']} refugis")
        print(f"- Couchage = 1: {stats['couchage_1']} refugis") 
        print(f"- Couchage altres valors: {stats['couchage_other']} refugis")
        
        print(f"\n🛏️ TIPUS D'ALLOTJAMENT:")
        print(f"- Matelas = 1: {stats['matelas_1']} refugis")
        print(f"- Bas_flancs = 1: {stats['bas_flancs_1']} refugis")
        print(f"- Lits = 1: {stats['lits_1']} refugis")
        print(f"- Mezzanine/etage = 1: {stats['mezzanine_etage_1']} refugis")
        
        print(f"\n⚙️ SERVEIS BÀSICS (binaris):")
        print(f"- Cheminee binari: {stats['cheminee_binary']}/{stats['total_refugis']}")
        print(f"- Bois binari: {stats['bois_binary']}/{stats['total_refugis']}")  
        print(f"- Eau binari: {stats['eau_binary']}/{stats['total_refugis']}")
        
        print(f"\n📝 INFORMACIÓ ADDICIONAL:")
        print(f"- Info_couchage present: {stats['info_couchage_present']} refugis")
        print(f"- Info_eau present: {stats['info_eau_present']} refugis")
        
        # Mostrar exemples
        print(f"\n🔍 EXEMPLES:")
        for key, example_list in examples.items():
            if example_list:
                print(f"- {key}: {', '.join(example_list[:3])}")
        
        # Mostrar errors si n'hi ha
        if missing_fields:
            print(f"\n❌ CAMPS MANCANTS ({len(missing_fields)} errors):")
            for error in missing_fields[:10]:  # Només els primers 10
                print(f"  {error}")
            if len(missing_fields) > 10:
                print(f"  ... i {len(missing_fields) - 10} errors més")
        
        if invalid_values:
            print(f"\n⚠️ VALORS INVÀLIDS ({len(invalid_values)} errors):")
            for error in invalid_values[:10]:  # Només els primers 10
                print(f"  {error}")
            if len(invalid_values) > 10:
                print(f"  ... i {len(invalid_values) - 10} errors més")
        
        # Verificar coherència
        print(f"\n✅ VERIFICACIÓ DE COHERÈNCIA:")
        
        # Els refugis amb info_couchage haurien de tenir couchage = 1
        refugis_amb_info_couchage_i_couchage_0 = 0
        for refuge in data:
            if 'info_couchage' in refuge:
                couchage_val = refuge.get('info_comp', {}).get('couchage', 0)
                if couchage_val == 0:
                    refugis_amb_info_couchage_i_couchage_0 += 1
        
        print(f"- Refugis amb info_couchage però couchage=0: {refugis_amb_info_couchage_i_couchage_0}")
        
        # Verificar que els camps de couchage especial sumen correctament
        total_couchage_flags = stats['matelas_1'] + stats['bas_flancs_1'] + stats['lits_1'] + stats['mezzanine_etage_1']
        print(f"- Total flags d'allotjament: {total_couchage_flags}")
        
        if len(missing_fields) == 0 and len(invalid_values) == 0:
            print(f"\n🎉 VERIFICACIÓ COMPLETADA AMB ÈXIT!")
            print(f"Tots els refugis tenen l'estructura correcta i valors vàlids.")
        else:
            print(f"\n⚠️ VERIFICACIÓ COMPLETADA AMB ADVERTÈNCIES")
            print(f"Hi ha {len(missing_fields)} camps mancants i {len(invalid_values)} valors invàlids.")
        
        return stats, missing_fields, invalid_values
        
    except FileNotFoundError:
        print(f"❌ Error: No s'ha trobat el fitxer {json_file}")
        return None, [], []
    except json.JSONDecodeError:
        print(f"❌ Error: El fitxer {json_file} no és un JSON vàlid")
        return None, [], []
    except Exception as e:
        print(f"❌ Error inesperat: {e}")
        return None, [], []

if __name__ == "__main__":
    json_file = "refusPyrenees_finished_services.json"
    verify_couchage_processing(json_file)