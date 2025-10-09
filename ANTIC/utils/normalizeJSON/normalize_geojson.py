import json

# Load the GeoJSON file
file_path = 'refusPyrinees.geojson'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Transform each feature to the new structure
normalized_features = []
for feature in data['features']:
    if 'type' in feature and feature['type'] == 'Feature':
        # Create a new feature with the normalized structure
        new_feature = {}
        
        # Extract coordinates directly from geometry
        if 'geometry' in feature and 'coordinates' in feature['geometry']:
            new_feature['coordinates'] = feature['geometry']['coordinates']
        
        # Extract all properties and add them directly to the feature
        if 'properties' in feature:
            for key, value in feature['properties'].items():
                new_feature[key] = value
                
        normalized_features.append(new_feature)
    else:
        # Feature is already normalized or has a different structure
        normalized_features.append(feature)

# Replace the features in the original data
data['features'] = normalized_features

# Write the normalized data back to file
output_path = 'refusPyrinees_normalized.geojson'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Normalized GeoJSON written to {output_path}")
