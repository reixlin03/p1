#!/usr/bin/env python3
"""
Simple script to download TPU boundaries from Hong Kong government data portal.
Uses data.gov.hk and Esri China Open Data Portal.
"""

import requests
import json
import os
from pathlib import Path

def download_tpu_2016():
    """Download 2016 TPU boundaries"""
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / 'data' / 'raw' / 'tpu'
    os.makedirs(output_dir, exist_ok=True)
    
    # Try Esri China Open Data Portal - 2016 TPU
    url = "https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2016_PlanD_gdb/FeatureServer/0/query"
    
    params = {
        'where': '1=1',
        'outFields': '*',
        'f': 'geojson',
        'outSR': '4326',
        'resultRecordCount': 10000
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("Downloading 2016 TPU boundaries...")
    try:
        response = requests.get(url, params=params, headers=headers, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        output_file = output_dir / 'tpu_boundaries_2016.geojson'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        feature_count = len(data.get('features', []))
        print(f"  ✓ Downloaded {feature_count} features to {output_file}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def download_tpu_2011():
    """Download 2011 TPU boundaries"""
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / 'data' / 'raw' / 'tpu'
    os.makedirs(output_dir, exist_ok=True)
    
    url = "https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2011_PlanD_gdb/FeatureServer/0/query"
    
    params = {
        'where': '1=1',
        'outFields': '*',
        'f': 'geojson',
        'outSR': '4326',
        'resultRecordCount': 10000
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("Downloading 2011 TPU boundaries...")
    try:
        response = requests.get(url, params=params, headers=headers, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        output_file = output_dir / 'tpu_boundaries_2011.geojson'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        feature_count = len(data.get('features', []))
        print(f"  ✓ Downloaded {feature_count} features to {output_file}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def download_tpu_2006():
    """Download 2006 TPU boundaries"""
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / 'data' / 'raw' / 'tpu'
    os.makedirs(output_dir, exist_ok=True)
    
    url = "https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2006_PlanD_gdb/FeatureServer/0/query"
    
    params = {
        'where': '1=1',
        'outFields': '*',
        'f': 'geojson',
        'outSR': '4326',
        'resultRecordCount': 10000
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("Downloading 2006 TPU boundaries...")
    try:
        response = requests.get(url, params=params, headers=headers, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        output_file = output_dir / 'tpu_boundaries_2006.geojson'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        feature_count = len(data.get('features', []))
        print(f"  ✓ Downloaded {feature_count} features to {output_file}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def download_tpu_2001():
    """Download 2001 TPU boundaries"""
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / 'data' / 'raw' / 'tpu'
    os.makedirs(output_dir, exist_ok=True)
    
    url = "https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2001_PlanD_gdb/FeatureServer/0/query"
    
    params = {
        'where': '1=1',
        'outFields': '*',
        'f': 'geojson',
        'outSR': '4326',
        'resultRecordCount': 10000
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("Downloading 2001 TPU boundaries...")
    try:
        response = requests.get(url, params=params, headers=headers, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        output_file = output_dir / 'tpu_boundaries_2001.geojson'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        feature_count = len(data.get('features', []))
        print(f"  ✓ Downloaded {feature_count} features to {output_file}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def download_tpu_2021():
    """Download 2021 TPU boundaries"""
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / 'data' / 'raw' / 'tpu'
    os.makedirs(output_dir, exist_ok=True)
    
    # Try Esri China Open Data Portal - 2021 TPU
    # Try multiple possible service URLs
    urls = [
        "https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2021_PlanD_gdb/FeatureServer/0/query",
        "https://services1.arcgis.com/EbqNbzKqJqFqFqFq/arcgis/rest/services/TPU_2021/FeatureServer/0/query",
        "https://opendata.arcgis.com/api/v3/datasets/c4c71147985b4be1aade0fb1401530c2_0/downloads/data?format=geojson&spatialRefId=4326"
    ]
    
    params = {
        'where': '1=1',
        'outFields': '*',
        'f': 'geojson',
        'outSR': '4326',
        'resultRecordCount': 10000
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("Downloading 2021 TPU boundaries...")
    for url in urls:
        try:
            if 'downloads/data' in url:
                # Direct download URL
                response = requests.get(url, headers=headers, timeout=120)
            else:
                # REST API query
                response = requests.get(url, params=params, headers=headers, timeout=120)
            
            response.raise_for_status()
            data = response.json()
            
            # Check if it's a valid GeoJSON
            if 'features' in data or 'type' in data:
                output_file = output_dir / 'tpu_boundaries_2021.geojson'
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                feature_count = len(data.get('features', []))
                print(f"  ✓ Downloaded {feature_count} features to {output_file}")
                return True
        except Exception as e:
            print(f"  Trying alternative URL... ({e})")
            continue
    
    print(f"  ✗ Error: Could not download 2021 TPU boundaries from any source")
    return False


def main():
    """Download all TPU boundaries"""
    print("=" * 60)
    print("Downloading TPU Boundaries from Esri China Open Data Portal")
    print("=" * 60)
    
    results = {}
    results['2001'] = download_tpu_2001()
    results['2006'] = download_tpu_2006()
    results['2011'] = download_tpu_2011()
    results['2016'] = download_tpu_2016()
    results['2021'] = download_tpu_2021()
    
    print("\n" + "=" * 60)
    print("Download Summary:")
    for year, success in results.items():
        status = "✓ Success" if success else "✗ Failed"
        print(f"  {year}: {status}")
    print("=" * 60)


if __name__ == '__main__':
    main()

