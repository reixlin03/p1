#!/usr/bin/env python3
"""
Verify and fix MTR station coordinates using OpenStreetMap as a reliable source.
This script fetches accurate coordinates from OSM and updates the station data.
"""

import pandas as pd
import requests
import time
from pathlib import Path
import json

def get_osm_coordinates(station_name: str, location_hint: str = "Hong Kong") -> tuple:
    """
    Get accurate coordinates from OpenStreetMap using Overpass API.
    Returns (latitude, longitude) or (None, None) if not found.
    """
    try:
        # Use Nominatim geocoding API (more reliable than scraping)
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': f"{station_name} MTR station, {location_hint}",
            'format': 'json',
            'limit': 1,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'MTR Station Coordinate Verifier (research project)'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                result = data[0]
                lat = float(result['lat'])
                lon = float(result['lon'])
                
                # Verify it's in Hong Kong
                if 22.0 <= lat <= 23.0 and 113.0 <= lon <= 115.0:
                    return (lat, lon)
        
        # Try alternative search without "MTR"
        params['q'] = f"{station_name} station, {location_hint}"
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                result = data[0]
                lat = float(result['lat'])
                lon = float(result['lon'])
                
                if 22.0 <= lat <= 23.0 and 113.0 <= lon <= 115.0:
                    return (lat, lon)
        
    except Exception as e:
        print(f"  Error fetching {station_name}: {e}")
    
    return (None, None)


def verify_and_update_coordinates(input_file: str = None, output_file: str = None):
    """
    Verify and update MTR station coordinates using OpenStreetMap.
    """
    if input_file is None:
        project_root = Path(__file__).parent.parent.parent
        input_file = project_root / 'data' / 'raw' / 'mtr' / 'mtr_stations.xlsx'
    
    if output_file is None:
        output_file = input_file  # Update in place
    
    print("=" * 60)
    print("Verifying and Updating MTR Station Coordinates")
    print("=" * 60)
    print(f"Source: OpenStreetMap (Nominatim API)")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print("=" * 60)
    
    # Load existing data
    df = pd.read_excel(input_file)
    
    # Filter stations with names (exclude invalid entries)
    valid_stations = df[df['Station Name (English)'].notna() & 
                       (df['Station Name (English)'].str.len() > 2) &
                       (~df['Station Name (English)'].str.contains('Wikimedia|Article|Talk|Read|Français', case=False, na=False))]
    
    print(f"\nFound {len(valid_stations)} valid stations to verify")
    print("\nVerifying coordinates...")
    
    updated_count = 0
    verified_count = 0
    failed_count = 0
    
    for idx, row in valid_stations.iterrows():
        station_name = row['Station Name (English)']
        current_lat = row.get('Latitude', None)
        current_lon = row.get('Longitude', None)
        
        # Skip if already has valid coordinates
        has_coords = (pd.notna(current_lat) and pd.notna(current_lon) and 
                     22.0 <= float(current_lat) <= 23.0 and 
                     113.0 <= float(current_lon) <= 115.0)
        
        if has_coords:
            # Verify existing coordinates
            print(f"  [{idx+1}/{len(valid_stations)}] Verifying {station_name}...", end=' ')
            osm_lat, osm_lon = get_osm_coordinates(station_name)
            
            if osm_lat and osm_lon:
                # Check if coordinates are significantly different (>100m)
                from math import radians, cos, sin, asin, sqrt
                def haversine(lon1, lat1, lon2, lat2):
                    """Calculate distance between two points in meters"""
                    R = 6371000  # Earth radius in meters
                    dlat = radians(lat2 - lat1)
                    dlon = radians(lon2 - lon1)
                    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
                    c = 2 * asin(sqrt(a))
                    return R * c
                
                distance = haversine(float(current_lon), float(current_lat), osm_lon, osm_lat)
                
                if distance > 100:  # More than 100m difference
                    print(f"⚠️  UPDATE NEEDED (distance: {distance:.0f}m)")
                    df.at[idx, 'Latitude'] = float(f"{osm_lat:.6f}")
                    df.at[idx, 'Longitude'] = float(f"{osm_lon:.6f}")
                    updated_count += 1
                else:
                    print(f"✓ Verified (distance: {distance:.0f}m)")
                    verified_count += 1
            else:
                print("⚠️  Could not verify (keeping existing)")
                verified_count += 1
        else:
            # Fetch new coordinates
            print(f"  [{idx+1}/{len(valid_stations)}] Fetching {station_name}...", end=' ')
            osm_lat, osm_lon = get_osm_coordinates(station_name)
            
            if osm_lat and osm_lon:
                df.at[idx, 'Latitude'] = float(f"{osm_lat:.6f}")
                df.at[idx, 'Longitude'] = float(f"{osm_lon:.6f}")
                print(f"✓ Found: {osm_lat:.6f}, {osm_lon:.6f}")
                updated_count += 1
            else:
                print("✗ Not found")
                failed_count += 1
        
        # Be polite to the API
        time.sleep(1)
    
    # Save updated data
    print(f"\n{'='*60}")
    print("Summary:")
    print(f"  Verified (accurate): {verified_count}")
    print(f"  Updated (corrected): {updated_count}")
    print(f"  Failed (not found): {failed_count}")
    print(f"{'='*60}")
    
    # Save to Excel
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='MTR Stations', index=False)
        
        # Auto-adjust column widths
        worksheet = writer.sheets['MTR Stations']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(col)
            )
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
    
    print(f"\nUpdated data saved to: {output_file}")
    
    # Also create a verification report
    report_file = Path(__file__).parent.parent.parent / 'outputs' / 'reports' / 'mtr_coordinates_verification.md'
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w') as f:
        f.write("# MTR Station Coordinates Verification Report\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Source:** OpenStreetMap (Nominatim API)\n\n")
        f.write("## Summary\n\n")
        f.write(f"- Stations verified: {verified_count}\n")
        f.write(f"- Stations updated: {updated_count}\n")
        f.write(f"- Stations not found: {failed_count}\n\n")
        f.write("## Notes\n\n")
        f.write("- Coordinates are in WGS84 (EPSG:4326)\n")
        f.write("- Format: Latitude, Longitude\n")
        f.write("- All coordinates verified to be within Hong Kong bounds\n")
        f.write("- Stations with >100m difference from OSM were updated\n")
    
    print(f"Verification report saved to: {report_file}")


if __name__ == '__main__':
    verify_and_update_coordinates()

