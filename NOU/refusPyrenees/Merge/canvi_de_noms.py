import json

def transform_refuge_data(input_file, output_file):
    """
    Transforms the refuge data according to specified requirements:
    - Transform coordinates array to dictionary format
    - Change url field to links array
    - Rename descriptif to description
    - Rename commentaire to remarque
    """
    
    # Load the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        refuges = json.load(f)
    
    # Transform each refuge
    for refuge in refuges:
        # Transform coordinates from array to dictionary
        if 'coordinates' in refuge and isinstance(refuge['coordinates'], list) and len(refuge['coordinates']) >= 2:
            longitude = refuge['coordinates'][0]
            latitude = refuge['coordinates'][1]
            refuge['coord'] = {
                "long": longitude,
                "lat": latitude
            }
            # Remove the old coordinates field
            del refuge['coordinates']
        
        # Transform url to links array
        if 'url' in refuge:
            refuge['links'] = [refuge['url']]
            # Remove the old url field
            del refuge['url']
        
        # Rename descriptif to description
        if 'descriptif' in refuge:
            refuge['description'] = refuge['descriptif']
            del refuge['descriptif']
        
        # Rename commentaire to remarque
        if 'commentaire' in refuge:
            refuge['remarque'] = refuge['commentaire']
            del refuge['commentaire']
    
    # Save the transformed data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(refuges, f, ensure_ascii=False, indent=2)
    
    print(f"Transformation completed successfully!")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Total refuges processed: {len(refuges)}")

if __name__ == "__main__":
    input_file = "refusPyrenees_finished_services.json"
    output_file = "refusPyrenees_definitiu.json"
    
    transform_refuge_data(input_file, output_file)