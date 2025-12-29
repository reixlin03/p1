#!/usr/bin/env python3
"""
Download TPU boundary data from ArcGIS/Esri China open data portals.
"""

import requests
import json
import os
from pathlib import Path

# TPU data sources - ArcGIS REST API endpoints
TPU_SOURCES = {
    '2021': {
        'name': '2021 TPU Boundaries',
        'base_url': 'https://opendata.arcgis.com/api/v3/datasets',
        'dataset_id': 'c4c71147985b4be1aade0fb1401530c2',
        'feature_service': 'https://services1.arcgis.com/EbqNbzKqJqFqFqFq/arcgis/rest/services/TPU_2021/FeatureServer/0'
    },
    '2016': {
        'name': '2016 TPU Boundaries',
        'webmap_id': '9800de8d31f646a9b191a0c8f5cd36c6',
        'feature_service': None  # Will need to extract from webmap
    },
    '2011': {
        'name': '2011 TPU Boundaries',
        'dataset_id': 'boundaries-of-tertiary-planning-units-street-blocks-village-clusters-in-hong-kong-for-2011-population-census',
        'feature_service': 'https://opendata.arcgis.com/api/v3/datasets/boundaries-of-tertiary-planning-units-street-blocks-village-clusters-in-hong-kong-for-2011-population-census'
    },
    '2006': {
        'name': '2006 TPU Boundaries',
        'dataset_id': 'esrihk::boundaries-of-tertiary-planning-units-street-blocks-village-clusters-in-hong-kong-for-2006-population-by-census-1',
        'feature_service': 'https://opendata.arcgis.com/api/v3/datasets/esrihk::boundaries-of-tertiary-planning-units-street-blocks-village-clusters-in-hong-kong-for-2006-population-by-census-1'
    },
    '2001': {
        'name': '2001 TPU Boundaries',
        'dataset_id': 'boundaries-of-tertiary-planning-units-street-blocks-village-clusters-in-hong-kong-for-2001-population-census-1',
        'feature_service': 'https://opendata.arcgis.com/api/v3/datasets/boundaries-of-tertiary-planning-units-street-blocks-village-clusters-in-hong-kong-for-2001-population-census-1'
    }
}


def download_from_arcgis_rest(feature_service_url: str, output_file: str, where_clause: str = "1=1"):
    """
    Download data from ArcGIS REST Feature Service.
    """
    print(f"Downloading from: {feature_service_url}")
    
    # Query parameters
    params = {
        'where': where_clause,
        'outFields': '*',
        'f': 'geojson',
        'outSR': '4326'  # WGS84
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # Try to get all features (may need pagination)
        response = requests.get(f"{feature_service_url}/query", params=params, headers=headers, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if we need to paginate
        if 'exceededTransferLimit' in data and data.get('exceededTransferLimit'):
            print("  Large dataset detected, using pagination...")
            all_features = []
            offset = 0
            record_count = 1000
            
            while True:
                params['resultOffset'] = offset
                params['resultRecordCount'] = record_count
                
                response = requests.get(f"{feature_service_url}/query", params=params, headers=headers, timeout=60)
                response.raise_for_status()
                page_data = response.json()
                
                if 'features' in page_data and page_data['features']:
                    all_features.extend(page_data['features'])
                    offset += record_count
                    
                    if len(page_data['features']) < record_count:
                        break
                else:
                    break
            
            data = {
                'type': 'FeatureCollection',
                'features': all_features
            }
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        feature_count = len(data.get('features', []))
        print(f"  ✓ Downloaded {feature_count} features to {output_file}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error downloading: {e}")
        return False


def get_feature_service_from_dataset(dataset_id: str):
    """
    Get feature service URL from dataset ID via ArcGIS Open Data API.
    """
    api_url = f"https://opendata.arcgis.com/api/v3/datasets/{dataset_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Try to find feature service URL in the response
        if 'data' in data and 'services' in data['data']:
            services = data['data']['services']
            for service in services:
                if service.get('type') == 'FeatureServer':
                    return service.get('url')
        
        # Alternative: try to construct from dataset metadata
        if 'data' in data and 'url' in data['data']:
            return data['data']['url']
            
    except Exception as e:
        print(f"  Error getting feature service URL: {e}")
    
    return None


def download_tpu_data(year: str, output_dir: Path = None):
    """
    Download TPU boundary data for a specific year.
    """
    if output_dir is None:
        project_root = Path(__file__).parent.parent.parent
        output_dir = project_root / 'data' / 'raw' / 'tpu'
    os.makedirs(output_dir, exist_ok=True)
    
    source = TPU_SOURCES.get(year)
    if not source:
        print(f"Unknown year: {year}")
        return False
    
    print(f"\n{'='*60}")
    print(f"Downloading {source['name']}")
    print(f"{'='*60}")
    
    output_file = output_dir / f'tpu_boundaries_{year}.geojson'
    
    # If feature service URL is provided, use it directly
    if source.get('feature_service'):
        feature_service = source['feature_service']
        
        # If it's a dataset URL, try to get the actual feature service
        if 'api/v3/datasets' in feature_service:
            feature_service = get_feature_service_from_dataset(source.get('dataset_id', ''))
            if not feature_service:
                print(f"  ✗ Could not determine feature service URL")
                return False
        
        return download_from_arcgis_rest(feature_service, output_file)
    
    # For 2016, we need to extract from webmap
    elif source.get('webmap_id'):
        print(f"  Note: 2016 data requires manual extraction from webmap")
        print(f"  Webmap ID: {source['webmap_id']}")
        print(f"  Please download manually or use alternative source")
        return False
    
    return False


def main():
    """
    Download TPU boundary data for all years.
    """
    print("=" * 60)
    print("TPU Boundary Data Downloader")
    print("=" * 60)
    
    years = ['2001', '2006', '2011', '2016', '2021']
    
    # Try alternative approach: use Esri China Open Data portal directly
    # These portals often have direct download links
    
    # For Esri China Open Data, we'll try to construct feature service URLs
    esri_china_base = "https://services1.arcgis.com"
    
    # Try common patterns for Esri China services
    # ArcGIS Open Data portal URLs - try REST API query endpoints
    alternative_sources = {
        '2021': [
            'https://opendata.arcgis.com/datasets/c4c71147985b4be1aade0fb1401530c2_0.geojson',
            'https://opendata.esrichina.hk/datasets/c4c71147985b4be1aade0fb1401530c2_0.geojson',
            # Try REST API query
            ('https://services1.arcgis.com/EbqNbzKqJqFqFqFq/arcgis/rest/services/TPU_2021/FeatureServer/0/query', True)
        ],
        '2011': [
            'https://opendata.arcgis.com/datasets/boundaries-of-tertiary-planning-units-street-blocks-village-clusters-in-hong-kong-for-2011-population-census.geojson',
            'https://opendata.esrichina.hk/datasets/boundaries-of-tertiary-planning-units-street-blocks-village-clusters-in-hong-kong-for-2011-population-census.geojson',
            # Try REST API - common Esri China pattern
            ('https://services1.arcgis.com/EbqNbzKqJqFqFqFq/arcgis/rest/services/TPU_2011/FeatureServer/0/query', True),
            ('https://opendata.arcgis.com/api/v3/datasets/boundaries-of-tertiary-planning-units-street-blocks-village-clusters-in-hong-kong-for-2011-population-census/downloads/data?format=geojson&spatialRefId=4326', False)
        ],
        '2006': [
            'https://opendata.arcgis.com/datasets/esrihk::boundaries-of-tertiary-planning-units-street-blocks-village-clusters-in-hong-kong-for-2006-population-by-census-1.geojson'
        ],
        '2001': [
            'https://opendata.arcgis.com/datasets/boundaries-of-tertiary-planning-units-street-blocks-village-clusters-in-hong-kong-for-2001-population-census-1.geojson',
            'https://opendata.esrichina.hk/datasets/boundaries-of-tertiary-planning-units-street-blocks-village-clusters-in-hong-kong-for-2001-population-census-1.geojson',
            ('https://opendata.arcgis.com/api/v3/datasets/boundaries-of-tertiary-planning-units-street-blocks-village-clusters-in-hong-kong-for-2001-population-census-1/downloads/data?format=geojson&spatialRefId=4326', False)
        ]
    }
    
    # Get project root (2 levels up from this script)
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / 'data' / 'raw' / 'tpu'
    os.makedirs(output_dir, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for year in years:
        print(f"\nDownloading {year} TPU boundaries...")
        
        # Try direct GeoJSON download first (simpler)
        if year in alternative_sources:
            urls = alternative_sources[year] if isinstance(alternative_sources[year], list) else [alternative_sources[year]]
            output_file = output_dir / f'tpu_boundaries_{year}.geojson'
            success = False
            
            for url_item in urls:
                url = None
                is_rest_api = False
                
                # Handle tuple (url, is_rest_api) or string
                if isinstance(url_item, tuple):
                    url, is_rest_api = url_item
                else:
                    url = url_item
                
                if is_rest_api:
                    # REST API query endpoint
                    try:
                        print(f"  Trying REST API query: {url}")
                        params = {
                            'where': '1=1',
                            'outFields': '*',
                            'f': 'geojson',
                            'outSR': '4326'
                        }
                        response = requests.get(url, params=params, headers=headers, timeout=60)
                        if response.status_code == 200:
                            data = response.json()
                            if 'features' in data:
                                with open(output_file, 'w', encoding='utf-8') as f:
                                    json.dump(data, f, indent=2, ensure_ascii=False)
                                feature_count = len(data.get('features', []))
                                print(f"  ✓ Downloaded {feature_count} features to {output_file}")
                                success = True
                                break
                    except Exception as e:
                        print(f"  REST API query failed: {e}")
                        continue
                else:
                    # Regular URL download
                    try:
                        print(f"  Trying direct download: {url}")
                        response = requests.get(url, headers=headers, timeout=60, params={'outSR': '4326'} if '?' not in url else {})
                        
                        if response.status_code == 200:
                            data = response.json()
                            with open(output_file, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            
                            feature_count = len(data.get('features', []))
                            print(f"  ✓ Downloaded {feature_count} features to {output_file}")
                            success = True
                            break
                    except Exception as e:
                        print(f"  Direct download failed: {e}")
                        continue
            
            if success:
                continue
        
        # Fallback to REST API method
        download_tpu_data(year, output_dir)
    
    print(f"\n{'='*60}")
    print("Download complete!")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()

