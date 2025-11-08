import json
import requests
import time
from typing import List, Dict, Optional

def load_refuges_data(json_file_path: str) -> List[Dict]:
    """Load refuges data from JSON file"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []

def find_null_altitude_refuges(refuges_data: List[Dict]) -> List[Dict]:
    """Find refuges with null altitude values"""
    null_altitude_refuges = []
    
    for i, refuge in enumerate(refuges_data):
        if refuge.get('altitude') is None:
            refuge_info = {
                'index': i,
                'name': refuge.get('name', 'Unknown'),
                'coord': refuge.get('coord', {}),
                'original_altitude': refuge.get('altitude')
            }
            null_altitude_refuges.append(refuge_info)
    
    return null_altitude_refuges

def get_elevation_from_api(latitude: float, longitude: float) -> Optional[float]:
    """Get elevation from Open Elevation API"""
    try:
        url = f"https://api.open-elevation.com/api/v1/lookup?locations={latitude},{longitude}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                elevation = data['results'][0].get('elevation')
                return float(elevation) if elevation is not None else None
        
        print(f"API request failed for coordinates ({latitude}, {longitude}): {response.status_code}")
        return None
        
    except Exception as e:
        print(f"Error getting elevation for coordinates ({latitude}, {longitude}): {e}")
        return None

def update_altitudes_with_api(refuges_data: List[Dict], null_altitude_refuges: List[Dict]) -> Dict:
    """Update altitudes using the Open Elevation API"""
    results = {
        'updated_refuges': [],
        'failed_updates': [],
        'statistics': {
            'total_null_altitudes': len(null_altitude_refuges),
            'successful_updates': 0,
            'failed_updates': 0
        }
    }
    
    print(f"Updating altitudes for {len(null_altitude_refuges)} refuges...")
    
    for i, refuge_info in enumerate(null_altitude_refuges):
        print(f"Processing {i+1}/{len(null_altitude_refuges)}: {refuge_info['name']}")
        
        coord = refuge_info.get('coord', {})
        lat = coord.get('lat')
        lon = coord.get('long')
        
        if lat is not None and lon is not None:
            # Get elevation from API
            elevation = get_elevation_from_api(lat, lon)
            
            if elevation is not None:
                # Update the original data
                refuge_index = refuge_info['index']
                refuges_data[refuge_index]['altitude'] = elevation
                
                # Record successful update
                update_info = {
                    'name': refuge_info['name'],
                    'coordinates': {'lat': lat, 'long': lon},
                    'new_altitude': elevation,
                    'original_altitude': refuge_info['original_altitude']
                }
                results['updated_refuges'].append(update_info)
                results['statistics']['successful_updates'] += 1
                
                print(f"  ✓ Updated altitude to {elevation}m")
            else:
                # Record failed update
                failed_info = {
                    'name': refuge_info['name'],
                    'coordinates': {'lat': lat, 'long': lon},
                    'reason': 'API returned null elevation'
                }
                results['failed_updates'].append(failed_info)
                results['statistics']['failed_updates'] += 1
                print(f"  ✗ Failed to get elevation from API")
        else:
            # Record failed update due to missing coordinates
            failed_info = {
                'name': refuge_info['name'],
                'coordinates': coord,
                'reason': 'Missing or invalid coordinates'
            }
            results['failed_updates'].append(failed_info)
            results['statistics']['failed_updates'] += 1
            print(f"  ✗ Missing coordinates")
        
        # Add delay to avoid overwhelming the API
        if i < len(null_altitude_refuges) - 1:
            time.sleep(0.5)  # 500ms delay between requests
    
    return results

def save_results(updated_data: List[Dict], update_results: Dict, original_filename: str):
    """Save updated data and results"""
    # Save updated refuges data
    output_filename = original_filename.replace('.json', '_updated_altitudes.json')
    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=2)
    
    # Save update results
    results_filename = original_filename.replace('.json', '_altitude_update_results.json')
    with open(results_filename, 'w', encoding='utf-8') as file:
        json.dump(update_results, file, ensure_ascii=False, indent=2)
    
    # Save summary report
    summary_filename = original_filename.replace('.json', '_altitude_update_summary.txt')
    with open(summary_filename, 'w', encoding='utf-8') as file:
        file.write("RESUM DE L'ACTUALITZACIÓ D'ALTITUDS\n")
        file.write("=" * 50 + "\n\n")
        
        stats = update_results['statistics']
        file.write(f"Total refugis amb altitud nul·la: {stats['total_null_altitudes']}\n")
        file.write(f"Actualitzacions exitoses: {stats['successful_updates']}\n")
        file.write(f"Actualitzacions fallides: {stats['failed_updates']}\n")
        file.write(f"Percentatge d'èxit: {(stats['successful_updates']/stats['total_null_altitudes']*100):.1f}%\n\n")
        
        file.write("REFUGIS ACTUALITZATS EXITOSAMENT:\n")
        file.write("-" * 40 + "\n")
        for i, refuge in enumerate(update_results['updated_refuges'], 1):
            file.write(f"{i:3d}. {refuge['name']} - Nova altitud: {refuge['new_altitude']}m\n")
        
        file.write(f"\nREFUGIS AMB ERRORS:\n")
        file.write("-" * 20 + "\n")
        for i, refuge in enumerate(update_results['failed_updates'], 1):
            file.write(f"{i:3d}. {refuge['name']} - Motiu: {refuge['reason']}\n")
    
    return output_filename, results_filename, summary_filename

def main():
    input_file = "data_refugis.json"
    
    print("Carregant dades dels refugis...")
    refuges_data = load_refuges_data(input_file)
    
    if not refuges_data:
        print("Error: No s'han pogut carregar les dades.")
        return
    
    print(f"Dades carregades: {len(refuges_data)} refugis")
    
    # Find refuges with null altitude
    print("Cercant refugis amb altitud nul·la...")
    null_altitude_refuges = find_null_altitude_refuges(refuges_data)
    
    print(f"Trobats {len(null_altitude_refuges)} refugis amb altitud nul·la")
    
    if len(null_altitude_refuges) == 0:
        print("No hi ha refugis amb altitud nul·la per actualitzar.")
        return
    
    # Update altitudes using API
    print("\nIniciant actualització d'altituds amb l'API Open Elevation...")
    update_results = update_altitudes_with_api(refuges_data, null_altitude_refuges)
    
    # Save results
    print("\nGuardant resultats...")
    output_file, results_file, summary_file = save_results(refuges_data, update_results, input_file)
    
    # Print summary
    stats = update_results['statistics']
    print(f"\n{'='*60}")
    print("RESUM FINAL:")
    print(f"{'='*60}")
    print(f"Total refugis amb altitud nul·la: {stats['total_null_altitudes']}")
    print(f"Actualitzacions exitoses: {stats['successful_updates']}")
    print(f"Actualitzacions fallides: {stats['failed_updates']}")
    print(f"Percentatge d'èxit: {(stats['successful_updates']/stats['total_null_altitudes']*100):.1f}%")
    print(f"\nFitxers generats:")
    print(f"- Dades actualitzades: {output_file}")
    print(f"- Resultats detallats: {results_file}")
    print(f"- Resum: {summary_file}")

if __name__ == "__main__":
    main()