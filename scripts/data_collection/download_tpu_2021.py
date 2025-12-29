#!/usr/bin/env python3
"""
Download 2021 TPU boundaries from Hong Kong data.gov.hk
"""

import requests
import json
import os
from pathlib import Path

def download_tpu_2021():
    """Download 2021 TPU boundaries from data.gov.hk"""
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / 'data' / 'raw' / 'tpu'
    os.makedirs(output_dir, exist_ok=True)
    
    # Try multiple sources for 2021 TPU data
    urls_to_try = [
        # Direct GeoJSON download from data.gov.hk
        {
            'url': 'https://www.geodata.gov.hk/gs/api/v1.0.0/collections/TPU_2021/items?f=json&limit=10000',
            'method': 'get',
            'params': None
        },
        # ArcGIS REST API - try different service names
        {
            'url': 'https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2021_PlanD/FeatureServer/0/query',
            'method': 'get',
            'params': {
                'where': '1=1',
                'outFields': '*',
                'f': 'geojson',
                'outSR': '4326',
                'resultRecordCount': 10000
            }
        },
        # Alternative service
        {
            'url': 'https://services1.arcgis.com/EbqNbzKqJqFqFqFq/arcgis/rest/services/TPU_2021/FeatureServer/0/query',
            'method': 'get',
            'params': {
                'where': '1=1',
                'outFields': '*',
                'f': 'geojson',
                'outSR': '4326',
                'resultRecordCount': 10000
            }
        }
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    print("Downloading 2021 TPU boundaries...")
    
    for attempt in urls_to_try:
        try:
            url = attempt['url']
            params = attempt.get('params')
            
            print(f"  Trying: {url[:80]}...")
            
            if params:
                response = requests.get(url, params=params, headers=headers, timeout=120)
            else:
                response = requests.get(url, headers=headers, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if valid GeoJSON
                if 'features' in data or (isinstance(data, dict) and 'type' in data):
                    output_file = output_dir / 'tpu_boundaries_2021.geojson'
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    feature_count = len(data.get('features', []))
                    print(f"  ✓ Downloaded {feature_count} features to {output_file}")
                    return True
                else:
                    print(f"  Response structure unexpected: {list(data.keys()) if isinstance(data, dict) else type(data)}")
            else:
                print(f"  Status {response.status_code}")
                
        except Exception as e:
            print(f"  Error: {str(e)[:100]}")
            continue
    
    print("\n⚠️  Could not download 2021 TPU data automatically.")
    print("   Manual download option:")
    print("   https://data.gov.hk/en-data/dataset/hk-pland-pland1-boundaries-of-tpu-sb-vc")
    print("   Save the file as: data/raw/tpu/tpu_boundaries_2021.geojson")
    return False


if __name__ == '__main__':
    download_tpu_2021()

