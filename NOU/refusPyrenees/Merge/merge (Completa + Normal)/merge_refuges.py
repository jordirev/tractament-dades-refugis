import json
import re
from difflib import SequenceMatcher

def normalize_name(name):
    """Normalize name for comparison - remove accents, convert to lowercase, remove extra spaces"""
    if not name:
        return ""
    
    # Convert to lowercase and remove extra spaces
    name = re.sub(r'\s+', ' ', name.lower().strip())
    
    # Remove common prefixes/suffixes that might vary
    prefixes_to_remove = ['refuge', 'cabane', 'refugio', 'cabana', 'chalet', 'abri', 'grange', 'orri', 'cayolar']
    suffixes_to_remove = ['(ruines)', 'ruines', 'ou', 'de', 'du', 'des', 'da', 'del', 'dels', 'de la', 'del']
    
    # Remove articles and common words
    articles = ['le', 'la', 'les', 'el', 'los', 'las', 'de', 'du', 'des', 'da', 'del', 'dels', 'de la']
    
    words = name.split()
    filtered_words = []
    
    for word in words:
        # Skip articles and very short words
        if len(word) > 2 and word not in articles:
            filtered_words.append(word)
    
    return ' '.join(filtered_words)

def similarity_score(str1, str2):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, str1, str2).ratio()

def find_best_match(norm_item, comp_items, threshold=0.6):
    """Find the best matching item from comp_items for norm_item"""
    best_match = None
    best_score = 0
    matching_info = []
    
    norm_name = normalize_name(norm_item.get('name', ''))
    norm_altitude = str(norm_item.get('altitude', '')).replace('m', '').strip()
    norm_cap_ete = str(norm_item.get('cap_ete', ''))
    norm_cap_hiver = str(norm_item.get('cap_hiver', ''))
    norm_region = normalize_name(norm_item.get('region', ''))
    
    for comp_item in comp_items:
        comp_name = normalize_name(comp_item.get('name', ''))
        comp_altitude = str(comp_item.get('altitude', '')).replace('m', '').strip()
        comp_capete = str(comp_item.get('capete', ''))
        comp_caphiv = str(comp_item.get('caphiv', ''))
        comp_ville = normalize_name(comp_item.get('ville', ''))
        
        # Calculate name similarity
        name_sim = similarity_score(norm_name, comp_name)
        
        # Check altitude match
        altitude_match = (norm_altitude == comp_altitude and norm_altitude != '') or (norm_altitude == '' and comp_altitude == '')
        
        # Check capacity matches
        capete_match = (norm_cap_ete == comp_capete and norm_cap_ete != '') or (norm_cap_ete == '' and comp_capete == '')
        caphiv_match = (norm_cap_hiver == comp_caphiv and norm_cap_hiver != '') or (norm_cap_hiver == '' and comp_caphiv == '')
        
        # Check region/ville match
        region_sim = similarity_score(norm_region, comp_ville)
        
        # Calculate total score
        score = name_sim * 0.6  # Name is most important
        if altitude_match:
            score += 0.15
        if capete_match:
            score += 0.1
        if caphiv_match:
            score += 0.1
        if region_sim > 0.7:
            score += 0.05
        
        if score > best_score and score >= threshold:
            best_score = score
            best_match = comp_item
            matching_info = {
                'name_similarity': name_sim,
                'altitude_match': altitude_match,
                'capete_match': capete_match,
                'caphiv_match': caphiv_match,
                'region_similarity': region_sim,
                'total_score': score
            }
    
    return best_match, best_score, matching_info

# Load the JSON files
norm_file = r"c:\Users\jordi\Desktop\UNI\TFG\INFO\NOU\refusPyrenees\Normal\refusPyrinees_norm.json"
comp_file = r"c:\Users\jordi\Desktop\UNI\TFG\INFO\NOU\refusPyrenees\Completa (té serveis)\refusPyrineesComp_norm.json"
output_file = r"c:\Users\jordi\Desktop\UNI\TFG\INFO\NOU\refusPyrenees\refusPyrinees_merged.json"

print("Carregant fitxers...")
with open(norm_file, 'r', encoding='utf-8') as f:
    norm_data = json.load(f)

with open(comp_file, 'r', encoding='utf-8') as f:
    comp_data = json.load(f)

print(f"Fitxer norm: {len(norm_data)} elements")
print(f"Fitxer comp: {len(comp_data)} elements")

# Merge the data
merged_data = []
matched_count = 0
difficult_matches = []
unmatched_items = []

print("\nProcessant emparellaments...")

for i, norm_item in enumerate(norm_data):
    if i % 100 == 0:
        print(f"Processat {i}/{len(norm_data)} elements...")
    
    # Find the best match
    best_match, score, match_info = find_best_match(norm_item, comp_data)
    
    # Create the merged item
    merged_item = norm_item.copy()
    
    if best_match:
        # Add the fields from the complete file
        merged_item['departement'] = best_match.get('departement', '')
        merged_item['cheminee'] = best_match.get('cheminee', '')
        merged_item['bois'] = best_match.get('bois', '')
        merged_item['eau'] = best_match.get('eau', '')
        merged_item['couchage'] = best_match.get('couchage', '')
        
        matched_count += 1
        
        # If the match is uncertain (low score), add to difficult matches
        if score < 0.8:
            difficult_matches.append({
                'norm_name': norm_item.get('name', ''),
                'comp_name': best_match.get('name', ''),
                'score': score,
                'match_info': match_info,
                'norm_altitude': norm_item.get('altitude', ''),
                'comp_altitude': best_match.get('altitude', ''),
                'norm_region': norm_item.get('region', ''),
                'comp_ville': best_match.get('ville', '')
            })
    else:
        # No match found - add empty fields
        merged_item['departement'] = ''
        merged_item['cheminee'] = ''
        merged_item['bois'] = ''
        merged_item['eau'] = ''
        merged_item['couchage'] = ''
        
        unmatched_items.append({
            'name': norm_item.get('name', ''),
            'altitude': norm_item.get('altitude', ''),
            'region': norm_item.get('region', ''),
            'cap_ete': norm_item.get('cap_ete', ''),
            'cap_hiver': norm_item.get('cap_hiver', '')
        })
    
    merged_data.append(merged_item)

# Save the merged data
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=4)

print(f"\nResultats:")
print(f"Total elements processats: {len(norm_data)}")
print(f"Elements emparellats: {matched_count}")
print(f"Elements no emparellats: {len(unmatched_items)}")
print(f"Emparellaments amb baixa confiança: {len(difficult_matches)}")

print(f"\nFitxer resultat creat: {output_file}")

# Show difficult matches
if difficult_matches:
    print(f"\n=== EMPARELLAMENTS AMB DIFICULTAT (puntuació < 0.8) ===")
    for i, match in enumerate(difficult_matches[:20]):  # Show first 20
        print(f"\n{i+1}. Puntuació: {match['score']:.3f}")
        print(f"   Norm: '{match['norm_name']}' (alt: {match['norm_altitude']}, regió: {match['norm_region']})")
        print(f"   Comp: '{match['comp_name']}' (alt: {match['comp_altitude']}, ville: {match['comp_ville']})")
        print(f"   Similitud nom: {match['match_info']['name_similarity']:.3f}")
    
    if len(difficult_matches) > 20:
        print(f"\n... i {len(difficult_matches) - 20} més")

# Show unmatched items
if unmatched_items:
    print(f"\n=== ELEMENTS NO EMPARELLATS ===")
    for i, item in enumerate(unmatched_items[:10]):  # Show first 10
        print(f"{i+1}. '{item['name']}' (alt: {item['altitude']}, regió: {item['region']})")
    
    if len(unmatched_items) > 10:
        print(f"... i {len(unmatched_items) - 10} més")

print(f"\nProcessament completat!")