import json
from collections import defaultdict, Counter

def analyze_info_comp(file_path):
    """Analiza todos los campos de info_comp y sus valores."""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Diccionario para almacenar los análisis
    field_analysis = defaultdict(lambda: {
        'values': Counter(),
        'refugios_with_field': [],
        'refugios_without_field': []
    })
    
    total_refugios = len(data['nodes'])
    refugios_with_info_comp = 0
    refugios_without_info_comp = []
    
    print(f"Analizando {total_refugios} refugios...")
    
    for refugio in data['nodes']:
        refugio_id = refugio.get('id')
        refugio_name = refugio.get('nom')
        
        if 'info_comp' in refugio and refugio['info_comp']:
            refugios_with_info_comp += 1
            info_comp = refugio['info_comp']
            
            # Analizar cada campo posible
            for field in ['manque_un_mur', 'cheminee', 'poele', 'couvertures', 'latrines', 'bois', 'eau', 'places_matelas']:
                if field in info_comp:
                    value = info_comp[field]
                    field_analysis[field]['values'][value] += 1
                    field_analysis[field]['refugios_with_field'].append({
                        'id': refugio_id,
                        'nom': refugio_name,
                        'value': value
                    })
                else:
                    field_analysis[field]['refugios_without_field'].append({
                        'id': refugio_id,
                        'nom': refugio_name
                    })
        else:
            refugios_without_info_comp.append({
                'id': refugio_id,
                'nom': refugio_name
            })
    
    return field_analysis, refugios_with_info_comp, refugios_without_info_comp, total_refugios

def write_analysis_to_file(field_analysis, refugios_with_info_comp, refugios_without_info_comp, total_refugios):
    """Escribe el análisis completo en un archivo de texto."""
    
    with open('analisis_info_comp.txt', 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS COMPLETO DE LOS CAMPOS 'info_comp'\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Total de refugios: {total_refugios}\n")
        f.write(f"Refugios con info_comp: {refugios_with_info_comp}\n")
        f.write(f"Refugios sin info_comp: {len(refugios_without_info_comp)}\n\n")
        
        if refugios_without_info_comp:
            f.write("REFUGIOS SIN CAMPO 'info_comp':\n")
            f.write("-" * 30 + "\n")
            for refugio in refugios_without_info_comp:
                f.write(f"ID: {refugio['id']} - {refugio['nom']}\n")
            f.write("\n")
        
        # Análisis por campo
        for field_name, analysis in field_analysis.items():
            f.write(f"CAMPO: {field_name}\n")
            f.write("-" * 30 + "\n")
            
            # Estadísticas generales
            total_with_field = len(analysis['refugios_with_field'])
            total_without_field = len(analysis['refugios_without_field'])
            
            f.write(f"Refugios con este campo: {total_with_field}\n")
            f.write(f"Refugios sin este campo: {total_without_field}\n")
            f.write("\nDistribución de valores:\n")
            
            # Valores y frecuencias
            for value, count in analysis['values'].most_common():
                percentage = (count / refugios_with_info_comp) * 100 if refugios_with_info_comp > 0 else 0
                f.write(f"  Valor '{value}': {count} refugios ({percentage:.1f}%)\n")
            
            # Ejemplos de refugios por valor
            if analysis['values']:
                f.write("\nEjemplos por valor:\n")
                # Ordenar valores convirtiendo todo a string para evitar errores de tipo
                try:
                    sorted_values = sorted(analysis['values'].keys())
                except TypeError:
                    # Si no se pueden ordenar directamente, convertir a string
                    sorted_values = sorted(analysis['values'].keys(), key=str)
                
                for value in sorted_values:
                    refugios_con_valor = [r for r in analysis['refugios_with_field'] if r['value'] == value]
                    f.write(f"\n  Valor '{value}' ({len(refugios_con_valor)} refugios):\n")
                    # Mostrar máximo 5 ejemplos
                    for refugio in refugios_con_valor[:5]:
                        f.write(f"    ID: {refugio['id']} - {refugio['nom']}\n")
                    if len(refugios_con_valor) > 5:
                        f.write(f"    ... y {len(refugios_con_valor) - 5} más\n")
            
            # Refugios sin este campo específico
            if analysis['refugios_without_field']:
                f.write(f"\nRefugios sin el campo '{field_name}' ({len(analysis['refugios_without_field'])}):\n")
                for refugio in analysis['refugios_without_field'][:10]:  # Máximo 10 ejemplos
                    f.write(f"  ID: {refugio['id']} - {refugio['nom']}\n")
                if len(analysis['refugios_without_field']) > 10:
                    f.write(f"  ... y {len(analysis['refugios_without_field']) - 10} más\n")
            
            f.write("\n" + "=" * 50 + "\n\n")
        
        # Resumen estadístico
        f.write("RESUMEN ESTADÍSTICO DE CAMPOS\n")
        f.write("=" * 30 + "\n")
        for field_name, analysis in sorted(field_analysis.items()):
            total_with_field = len(analysis['refugios_with_field'])
            percentage = (total_with_field / refugios_with_info_comp) * 100 if refugios_with_info_comp > 0 else 0
            f.write(f"{field_name}: {total_with_field}/{refugios_with_info_comp} refugios ({percentage:.1f}%)\n")

if __name__ == "__main__":
    file_path = "refusInfo_normalized_with_types.json"
    
    print("Iniciando análisis de campos info_comp...")
    field_analysis, refugios_with_info_comp, refugios_without_info_comp, total_refugios = analyze_info_comp(file_path)
    
    print("Escribiendo resultados en analisis_info_comp.txt...")
    write_analysis_to_file(field_analysis, refugios_with_info_comp, refugios_without_info_comp, total_refugios)
    
    print("¡Análisis completado!")
    print(f"Total refugios analizados: {total_refugios}")
    print(f"Refugios con info_comp: {refugios_with_info_comp}")
    print(f"Refugios sin info_comp: {len(refugios_without_info_comp)}")
    
    print("\nResumen de campos encontrados:")
    for field_name, analysis in sorted(field_analysis.items()):
        total_with_field = len(analysis['refugios_with_field'])
        unique_values = len(analysis['values'])
        print(f"- {field_name}: {total_with_field} refugios, {unique_values} valores únicos")