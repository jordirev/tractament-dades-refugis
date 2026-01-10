import json
import os
from openai import OpenAI

def merge_descriptions_with_gpt(input_file, output_file):
    """
    Uneix els camps description i remarque de cada refugi utilitzant GPT-4
    """
    
    # Configurar el client d'OpenAI (necessita OPENAI_API_KEY en variables d'entorn)
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Carregar el fitxer JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        refuges = json.load(f)
    
    print(f"Total de refugis a processar: {len(refuges)}")
    
    merged_refuges = []
    
    # Prompt del sistema
    system_prompt = """Ets un assistent expert en unir i resumir informació sobre refugis de muntanya.
                        La teva tasca és combinar els camps 'description' i 'remarque' en un sol text descriptiu.

                        INSTRUCCIONS:
                        1. Uneix primer els valors de description i remarque en un sol text.
                        2. Després, combina aquests textos unificats en un sol text final.
                        3. Assegura't que el text final sigui cohesionat, clar i resumit, sense repetir informació.
                        4. NO suprimeixis ni modifiquis dades numèriques, com nombres de places, dates o quantitats.
                        5. El resultat ha de ser un text fluït i comprensible que resumeixi tota la informació de manera natural.
                        6. Respon NOMÉS amb el text unificat, sense explicacions addicionals."""
    
    # Processar cada refugi
    for i, refuge in enumerate(refuges, 1):
        name = refuge.get('name', 'Sense nom')
        description = refuge.get('description', '')
        remarque = refuge.get('remarque', '')
        
        # Convertir a string si són llistes
        if isinstance(description, list):
            description = ' '.join(str(d) for d in description if d)
        if isinstance(remarque, list):
            remarque = ' '.join(str(r) for r in remarque if r)
        
        # Si tots dos estan buits, guardar buit
        if not description and not remarque:
            merged_refuges.append({
                'name': name,
                'description': ''
            })
            print(f"[{i}/{len(refuges)}] {name}: Sense descripció ni remarque")
            continue
        
        # Si només un està omplert, usar-lo directament
        if not description:
            merged_refuges.append({
                'name': name,
                'description': remarque
            })
            print(f"[{i}/{len(refuges)}] {name}: Només remarque")
            continue
        
        if not remarque:
            merged_refuges.append({
                'name': name,
                'description': description
            })
            print(f"[{i}/{len(refuges)}] {name}: Només description")
            continue
        
        # Si tots dos estan omplerts, enviar a GPT-4
        user_prompt = f"""Refugi: {name}

Description: {description}

Remarque: {remarque}

Uneix aquests dos textos en una sola descripció cohesionada."""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",  # o "gpt-4" segons disponibilitat
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            merged_description = response.choices[0].message.content.strip()
            
            merged_refuges.append({
                'name': name,
                'description': merged_description
            })
            
            print(f"[{i}/{len(refuges)}] {name}: Processat correctament")
            
        except Exception as e:
            print(f"[{i}/{len(refuges)}] {name}: ERROR - {str(e)}")
            # En cas d'error, combinar manualment
            merged_refuges.append({
                'name': name,
                'description': f"{description} {remarque}"
            })
    
    # Guardar el resultat
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_refuges, f, ensure_ascii=False, indent=2)
    
    print(f"\nProcessament completat!")
    print(f"Resultat guardat a: {output_file}")
    print(f"Total refugis processats: {len(merged_refuges)}")

if __name__ == "__main__":
    input_file = "refuges_name_description_remarque.json"
    output_file = "data_refuges_description_merged.json"
    
    # Verificar que la clau API està configurada
    if not os.getenv('OPENAI_API_KEY'):
        print("ERROR: Cal configurar la variable d'entorn OPENAI_API_KEY")
        print("Exemple: $env:OPENAI_API_KEY='sk-...'")
    else:
        merge_descriptions_with_gpt(input_file, output_file)
