import json

def count_characters_in_fields(input_file, output_file):
    """
    Cuenta los caracteres totales en los campos 'description' y 'remarque'
    """
    
    # Cargar el archivo JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        refuges = json.load(f)
    
    # Contadores
    total_description_chars = 0
    total_remarque_chars = 0
    refuges_with_description = 0
    refuges_with_remarque = 0
    description_entries = 0
    remarque_entries = 0
    
    # Procesar cada refugio
    for refuge in refuges:
        # Procesar description
        if 'description' in refuge and refuge['description']:
            refuges_with_description += 1
            if isinstance(refuge['description'], list):
                for desc in refuge['description']:
                    if desc:  # Solo si no está vacío
                        total_description_chars += len(str(desc))
                        description_entries += 1
            else:
                total_description_chars += len(str(refuge['description']))
                description_entries += 1
        
        # Procesar remarque
        if 'remarque' in refuge and refuge['remarque']:
            refuges_with_remarque += 1
            if isinstance(refuge['remarque'], list):
                for rem in refuge['remarque']:
                    if rem:  # Solo si no está vacío
                        total_remarque_chars += len(str(rem))
                        remarque_entries += 1
            else:
                total_remarque_chars += len(str(refuge['remarque']))
                remarque_entries += 1
    
    # Preparar el resultado
    result = f"""ANÁLISIS DE CARACTERES EN REFUGES_NAME_DESCRIPTION_REMARQUE.JSON
========================================================================

ESTADÍSTICAS GENERALES:
- Total de refugios analizados: {len(refuges)}

CAMPO 'DESCRIPTION':
- Refugios con descripción: {refuges_with_description}
- Número total de entradas de descripción: {description_entries}
- Total de caracteres en descripciones: {total_description_chars:,}
- Promedio de caracteres por refugio con descripción: {total_description_chars/refuges_with_description if refuges_with_description > 0 else 0:.2f}
- Promedio de caracteres por entrada de descripción: {total_description_chars/description_entries if description_entries > 0 else 0:.2f}

CAMPO 'REMARQUE':
- Refugios con remarque: {refuges_with_remarque}
- Número total de entradas de remarque: {remarque_entries}
- Total de caracteres en remarques: {total_remarque_chars:,}
- Promedio de caracteres por refugio con remarque: {total_remarque_chars/refuges_with_remarque if refuges_with_remarque > 0 else 0:.2f}
- Promedio de caracteres por entrada de remarque: {total_remarque_chars/remarque_entries if remarque_entries > 0 else 0:.2f}

TOTALES COMBINADOS:
- Total de caracteres (description + remarque): {total_description_chars + total_remarque_chars:,}
- Total de entradas (description + remarque): {description_entries + remarque_entries}
- Promedio de caracteres por entrada combinada: {(total_description_chars + total_remarque_chars)/(description_entries + remarque_entries) if (description_entries + remarque_entries) > 0 else 0:.2f}

DETALLES ADICIONALES:
- Refugios solo con description: {refuges_with_description - len([r for r in refuges if 'description' in r and r['description'] and 'remarque' in r and r['remarque']])}
- Refugios solo con remarque: {refuges_with_remarque - len([r for r in refuges if 'description' in r and r['description'] and 'remarque' in r and r['remarque']])}
- Refugios con ambos campos: {len([r for r in refuges if 'description' in r and r['description'] and 'remarque' in r and r['remarque']])}
- Refugios sin ninguno de los campos: {len(refuges) - len([r for r in refuges if ('description' in r and r['description']) or ('remarque' in r and r['remarque'])])}

Fecha del análisis: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Guardar el resultado
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"Análisis completado. Resultado guardado en: {output_file}")
    print(f"\nRESUMEN RÁPIDO:")
    print(f"Total caracteres en 'description': {total_description_chars:,}")
    print(f"Total caracteres en 'remarque': {total_remarque_chars:,}")
    print(f"Total caracteres combinados: {total_description_chars + total_remarque_chars:,}")

if __name__ == "__main__":
    input_file = "refuges_name_description_remarque.json"
    output_file = "analisis_caracteres_refuges.txt"
    
    count_characters_in_fields(input_file, output_file)