#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from collections import defaultdict

def analyze_service_values(json_file_path, output_file_path):
    """
    Analitza tots els valors dels paràmetres de serveis en el fitxer JSON
    i escriu els resultats en un fitxer de text.
    """
    
    # Paràmetres a analitzar
    parameters = ["cheminee", "bois", "eau", "couchage"]
    
    # Diccionari per emmagatzemar els valors únics de cada paràmetre
    values_dict = {param: defaultdict(int) for param in parameters}
    
    try:
        # Llegir el fitxer JSON
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total_refuges = len(data)
        print(f"Analitzant {total_refuges} refugis...")
        
        # Analitzar cada refugi
        for refuge in data:
            for param in parameters:
                if param in refuge:
                    value = refuge[param]
                    # Convertir None a string buit per consistència
                    if value is None:
                        value = ""
                    values_dict[param][str(value)] += 1
        
        # Escriure els resultats al fitxer de text
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("ANÀLISI DE VALORS DELS PARÀMETRES DE SERVEIS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total de refugis analitzats: {total_refuges}\n\n")
            
            for param in parameters:
                f.write(f"PARÀMETRE: {param.upper()}\n")
                f.write("-" * 30 + "\n")
                
                # Ordenar per freqüència (de major a menor)
                sorted_values = sorted(values_dict[param].items(), 
                                     key=lambda x: x[1], reverse=True)
                
                f.write(f"Total de valors únics: {len(sorted_values)}\n\n")
                
                for i, (value, count) in enumerate(sorted_values, 1):
                    percentage = (count / total_refuges) * 100
                    if value == "":
                        display_value = "[BUIT]"
                    else:
                        display_value = value
                    
                    f.write(f"{i:2d}. '{display_value}' - "
                           f"{count} vegades ({percentage:.1f}%)\n")
                
                f.write("\n" + "=" * 50 + "\n\n")
        
        print(f"Anàlisi completada! Resultats guardats a: {output_file_path}")
        
        # Mostrar un resum per pantalla
        print("\nRESUM:")
        for param in parameters:
            unique_count = len(values_dict[param])
            print(f"- {param}: {unique_count} valors únics")
    
    except FileNotFoundError:
        print(f"Error: No s'ha trobat el fitxer {json_file_path}")
    except json.JSONDecodeError:
        print(f"Error: El fitxer {json_file_path} no és un JSON vàlid")
    except Exception as e:
        print(f"Error inesperat: {e}")

if __name__ == "__main__":
    # Fitxers d'entrada i sortida
    input_file = "refusPyrenees_finished.json"
    output_file = "analisi_valors_serveis.txt"
    
    analyze_service_values(input_file, output_file)