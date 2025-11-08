import json
import math
from difflib import SequenceMatcher

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calcula la distància en metres entre dos punts geogràfics
    utilitzant la fórmula de Haversine
    """
    R = 6371000  # Radi de la Terra en metres
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distance = R * c
    return distance

def text_similarity(text1, text2):
    """
    Calcula la similitud entre dos textos (0-1)
    """
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def have_similar_words(name1, name2, min_word_length=4):
    """
    Comprova si dos noms comparteixen paraules semblants
    """
    # Normalitzar i dividir en paraules
    words1 = set(name1.lower().split())
    words2 = set(name2.lower().split())
    
    # Filtrar paraules molt comunes o curtes
    common_words = {'de', 'la', 'le', 'du', 'des', 'el', 'les', 'cabane', 'refuge', 'abri', 'borda', 'borde'}
    words1 = {w for w in words1 if len(w) >= min_word_length and w not in common_words}
    words2 = {w for w in words2 if len(w) >= min_word_length and w not in common_words}
    
    # Comprovar paraules iguals
    if words1.intersection(words2):
        return True, words1.intersection(words2)
    
    # Comprovar paraules similars
    for w1 in words1:
        for w2 in words2:
            if text_similarity(w1, w2) >= 0.75:  # 75% de similitud
                return True, {f"{w1}~{w2}"}
    
    return False, set()

def check_nearby_similar_refuges(json_file, max_distance=100, min_name_similarity=0.6):
    """
    Busca refugis que estiguin a prop (menys de max_distance metres)
    i que tinguin noms semblants
    """
    # Carregar les dades
    with open(json_file, 'r', encoding='utf-8') as f:
        refuges = json.load(f)
    
    print(f"Total de refugis carregats: {len(refuges)}")
    
    nearby_similar = []
    
    # Comparar tots els parells de refugis
    for i in range(len(refuges)):
        for j in range(i+1, len(refuges)):
            refuge1 = refuges[i]
            refuge2 = refuges[j]
            
            # Obtenir coordenades
            lat1 = refuge1['coord']['lat']
            lon1 = refuge1['coord']['long']
            lat2 = refuge2['coord']['lat']
            lon2 = refuge2['coord']['long']
            
            # Calcular distància
            distance = haversine_distance(lat1, lon1, lat2, lon2)
            
            # Si estan a prop
            if distance <= max_distance:
                name1 = refuge1.get('name', '')
                name2 = refuge2.get('name', '')
                
                # Calcular similitud dels noms
                similarity = text_similarity(name1, name2)
                
                # Comprovar si tenen paraules semblants
                has_similar, similar_words = have_similar_words(name1, name2)
                
                # Si els noms són similars o tenen paraules semblants
                if similarity >= min_name_similarity or has_similar:
                    nearby_similar.append({
                        'refuge1': {
                            'name': name1,
                            'coord': refuge1['coord'],
                            'altitude': refuge1.get('altitude'),
                            'type': refuge1.get('type'),
                            'links': refuge1.get('links', [])
                        },
                        'refuge2': {
                            'name': name2,
                            'coord': refuge2['coord'],
                            'altitude': refuge2.get('altitude'),
                            'type': refuge2.get('type'),
                            'links': refuge2.get('links', [])
                        },
                        'distance_m': round(distance, 2),
                        'name_similarity': round(similarity, 3),
                        'similar_words': list(similar_words) if has_similar else []
                    })
    
    return nearby_similar

def write_results_to_file(results, output_file):
    """
    Escriu els resultats en un fitxer de text
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("REFUGIS A PROP AMB NOMS SEMBLANTS (distància < 100m)\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total de parells trobats: {len(results)}\n\n")
        
        for idx, pair in enumerate(results, 1):
            f.write(f"\n{'='*80}\n")
            f.write(f"PARELLA #{idx}\n")
            f.write(f"{'='*80}\n\n")
            
            f.write(f"Distància: {pair['distance_m']} metres\n")
            f.write(f"Similitud del nom: {pair['name_similarity']*100:.1f}%\n")
            if pair['similar_words']:
                f.write(f"Paraules semblants: {', '.join(pair['similar_words'])}\n")
            f.write("\n")
            
            f.write("REFUGI 1:\n")
            f.write(f"  Nom: {pair['refuge1']['name']}\n")
            f.write(f"  Coordenades: {pair['refuge1']['coord']['lat']}, {pair['refuge1']['coord']['long']}\n")
            f.write(f"  Altitud: {pair['refuge1']['altitude']}m\n")
            f.write(f"  Tipus: {pair['refuge1']['type']}\n")
            if pair['refuge1']['links']:
                f.write(f"  Link: {pair['refuge1']['links'][0]}\n")
            
            f.write("\nREFUGI 2:\n")
            f.write(f"  Nom: {pair['refuge2']['name']}\n")
            f.write(f"  Coordenades: {pair['refuge2']['coord']['lat']}, {pair['refuge2']['coord']['long']}\n")
            f.write(f"  Altitud: {pair['refuge2']['altitude']}m\n")
            f.write(f"  Tipus: {pair['refuge2']['type']}\n")
            if pair['refuge2']['links']:
                f.write(f"  Link: {pair['refuge2']['links'][0]}\n")
            
            f.write("\n")
    
    print(f"\nResultats escrits a: {output_file}")

def main():
    input_file = 'data_refugis_updated_types.json'
    output_file = 'refugis_propers_noms_semblants.txt'
    
    print("Buscant refugis a prop amb noms semblants...\n")
    
    results = check_nearby_similar_refuges(input_file, max_distance=100, min_name_similarity=0.6)
    
    print(f"\nS'han trobat {len(results)} parells de refugis a prop amb noms semblants.")
    
    # Escriure resultats
    write_results_to_file(results, output_file)
    
    # També guardar en JSON per si és útil
    json_output = 'refugis_propers_noms_semblants.json'
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Resultats també guardats en JSON: {json_output}")

if __name__ == "__main__":
    main()
