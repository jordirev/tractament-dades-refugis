import json
import os

# Load the JSON file
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'refusInfoCompleta.json')
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Function to normalize the structure of a node
def normalize_node(node):
    normalized_node = {
        "id": node.get("id", ""),
        "nom": node.get("nom", ""),
        "lien": node.get("lien", ""),
        "coord": {
            "long": "",
            "lat": ""
        },
        "alt": "",
        "places": "",
        "etat": {
            "valeur": "",
            "id": "ouverture"
        },
        "remarque": "",
        "info_comp": {
            "site_officiel": {
                "nom": "Site Internet",
                "valeur": "0"
            },
            "manque_un_mur": "0",
            "cheminee": "0",
            "poele": "0",
            "couvertures": "0",
            "places_matelas": "0",
            "latrines": "0",
            "bois": "0",
            "eau": "0"
        },
        "description": ""
    }
    
    # Handle coordinates
    if "coord" in node:
        if "long" in node["coord"]:
            normalized_node["coord"]["long"] = node["coord"]["long"]
        if "lat" in node["coord"]:
            normalized_node["coord"]["lat"] = node["coord"]["lat"]
    
    # Handle altitude
    if "alt" in node:
        normalized_node["alt"] = node["alt"]
    elif "coord" in node and "alt" in node["coord"]:
        normalized_node["alt"] = node["coord"]["alt"]
    
    # Handle places
    if "places" in node:
        if isinstance(node["places"], dict) and "valeur" in node["places"]:
            normalized_node["places"] = node["places"]["valeur"]
        else:
            normalized_node["places"] = str(node["places"])
    
    # Handle etat (state)
    if "etat" in node:
        if isinstance(node["etat"], dict):
            if "valeur" in node["etat"]:
                normalized_node["etat"]["valeur"] = node["etat"]["valeur"]
            if "id" in node["etat"]:
                normalized_node["etat"]["id"] = node["etat"]["id"]
    
    # Handle remarque (remark)
    if "remarque" in node:
        if isinstance(node["remarque"], dict) and "valeur" in node["remarque"]:
            normalized_node["remarque"] = node["remarque"]["valeur"]
        else:
            normalized_node["remarque"] = str(node["remarque"])
    
    # Handle info_comp (complementary information)
    if "info_comp" in node:
        # Site officiel
        if "site_officiel" in node["info_comp"]:
            normalized_node["info_comp"]["site_officiel"] = node["info_comp"]["site_officiel"]
        
        # Process boolean or object fields and convert to simple strings
        for field in ["manque_un_mur", "cheminee", "poele", "couvertures", "latrines", "bois", "eau"]:
            if field in node["info_comp"]:
                if isinstance(node["info_comp"][field], dict) and "valeur" in node["info_comp"][field]:
                    normalized_node["info_comp"][field] = node["info_comp"][field]["valeur"]
                else:
                    normalized_node["info_comp"][field] = str(node["info_comp"][field])
        
        # Handle places_matelas specifically
        if "places_matelas" in node["info_comp"]:
            if isinstance(node["info_comp"]["places_matelas"], dict) and "valeur" in node["info_comp"]["places_matelas"]:
                normalized_node["info_comp"]["places_matelas"] = node["info_comp"]["places_matelas"]["valeur"]
            else:
                normalized_node["info_comp"]["places_matelas"] = str(node["info_comp"]["places_matelas"])
    
    # Handle description
    if "description" in node:
        normalized_node["description"] = node["description"]
    
    return normalized_node

# Normalize all nodes
normalized_nodes = [normalize_node(node) for node in data["nodes"]]

# Replace the nodes in the original data
data["nodes"] = normalized_nodes

# Write the normalized data back to file
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'refusInfoCompleta_normalized.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Normalized JSON written to {output_path}")
