import json

def analyze_null_altitudes(json_file_path):
    """Analyze refuges with null altitude values"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        null_altitudes = []
        for i, refuge in enumerate(data):
            if refuge.get('altitude') is None:
                null_altitudes.append({
                    'index': i,
                    'name': refuge.get('name', 'Unknown'),
                    'coord': refuge.get('coord', {}),
                })
        
        print(f"Total refugis: {len(data)}")
        print(f"Refugis amb altitud nul·la: {len(null_altitudes)}")
        
        print("\nPrimers 10 refugis amb altitud nul·la:")
        for i, refuge in enumerate(null_altitudes[:10]):
            coord = refuge['coord']
            lat = coord.get('lat', 'N/A')
            lon = coord.get('long', 'N/A')
            print(f"{i+1:3d}. {refuge['name']} - Coord: ({lat}, {lon})")
            
        return len(null_altitudes)
        
    except Exception as e:
        print(f"Error: {e}")
        return 0

if __name__ == "__main__":
    count = analyze_null_altitudes("data_refugis.json")
    print(f"\nTotal refugis amb altitud nul·la: {count}")