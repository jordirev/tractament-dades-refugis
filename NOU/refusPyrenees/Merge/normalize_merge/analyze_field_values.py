import json
from collections import Counter

def analyze_capacity_fields(json_file_path, output_file_path):
    """
    Analitza els valors possibles dels camps cap_ete i cap_hiver del fitxer JSON
    i escriu els resultats en un fitxer de text.
    """
    
    # Llegir el fitxer JSON
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Recopilar tots els valors dels camps
    cap_ete_values = []
    cap_hiver_values = []
    
    for refuge in data:
        if 'cap_ete' in refuge:
            cap_ete_values.append(refuge['cap_ete'])
        if 'cap_hiver' in refuge:
            cap_hiver_values.append(refuge['cap_hiver'])
    
    # Comptar la freqüència de cada valor
    cap_ete_counter = Counter(cap_ete_values)
    cap_hiver_counter = Counter(cap_hiver_values)
    
    # Obtenir valors únics ordenats
    unique_cap_ete = sorted(set(cap_ete_values), key=lambda x: int(x) if x.isdigit() else float('inf'))
    unique_cap_hiver = sorted(set(cap_hiver_values), key=lambda x: int(x) if x.isdigit() else float('inf'))
    
    # Escriure els resultats al fitxer de text
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write("ANÀLISI DELS CAMPS DE CAPACITAT DELS REFUGIS\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Total de refugis analitzats: {len(data)}\n\n")
        
        # Informació sobre cap_ete
        f.write("CAMP: cap_ete (Capacitat d'estiu)\n")
        f.write("-" * 35 + "\n")
        f.write(f"Nombre total de valors: {len(cap_ete_values)}\n")
        f.write(f"Valors únics: {len(unique_cap_ete)}\n\n")
        
        f.write("Valors possibles ordenats:\n")
        for value in unique_cap_ete:
            count = cap_ete_counter[value]
            f.write(f"  '{value}' - {count} refugis\n")
        
        f.write(f"\nRang de valors numèrics: ")
        numeric_values_ete = [int(v) for v in unique_cap_ete if v.isdigit()]
        if numeric_values_ete:
            f.write(f"{min(numeric_values_ete)} - {max(numeric_values_ete)}\n")
        else:
            f.write("No hi ha valors numèrics\n")
        
        f.write("\n" + "=" * 50 + "\n\n")
        
        # Informació sobre cap_hiver
        f.write("CAMP: cap_hiver (Capacitat d'hivern)\n")
        f.write("-" * 36 + "\n")
        f.write(f"Nombre total de valors: {len(cap_hiver_values)}\n")
        f.write(f"Valors únics: {len(unique_cap_hiver)}\n\n")
        
        f.write("Valors possibles ordenats:\n")
        for value in unique_cap_hiver:
            count = cap_hiver_counter[value]
            f.write(f"  '{value}' - {count} refugis\n")
        
        f.write(f"\nRang de valors numèrics: ")
        numeric_values_hiver = [int(v) for v in unique_cap_hiver if v.isdigit()]
        if numeric_values_hiver:
            f.write(f"{min(numeric_values_hiver)} - {max(numeric_values_hiver)}\n")
        else:
            f.write("No hi ha valors numèrics\n")
        
        f.write("\n" + "=" * 50 + "\n\n")
        
        # Estadístiques addicionals
        f.write("ESTADÍSTIQUES ADDICIONALS\n")
        f.write("-" * 25 + "\n")
        
        # Valors no numèrics
        non_numeric_ete = [v for v in unique_cap_ete if not v.isdigit()]
        non_numeric_hiver = [v for v in unique_cap_hiver if not v.isdigit()]
        
        if non_numeric_ete:
            f.write(f"Valors no numèrics en cap_ete: {non_numeric_ete}\n")
        if non_numeric_hiver:
            f.write(f"Valors no numèrics en cap_hiver: {non_numeric_hiver}\n")
        
        # Refugis amb capacitat 0
        refugis_cap_0_ete = cap_ete_counter.get('0', 0)
        refugis_cap_0_hiver = cap_hiver_counter.get('0', 0)
        
        f.write(f"\nRefugis amb capacitat 0 a l'estiu: {refugis_cap_0_ete}\n")
        f.write(f"Refugis amb capacitat 0 a l'hivern: {refugis_cap_0_hiver}\n")
        
        # Refugis amb major capacitat
        if numeric_values_ete:
            max_cap_ete = max(numeric_values_ete)
            f.write(f"Capacitat màxima d'estiu: {max_cap_ete} places\n")
        
        if numeric_values_hiver:
            max_cap_hiver = max(numeric_values_hiver)
            f.write(f"Capacitat màxima d'hivern: {max_cap_hiver} places\n")

# Executar l'anàlisi
if __name__ == "__main__":
    json_file = r"refusPyrinees_merged_filtered.json"
    output_file = r"analisi_capacitats_refugis.txt"
    
    analyze_capacity_fields(json_file, output_file)
    print(f"Anàlisi completada. Resultats guardats a: {output_file}")