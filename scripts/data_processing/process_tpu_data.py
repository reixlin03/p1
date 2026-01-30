#!/usr/bin/env python3
"""
Process and standardize TPU boundary data into GeoJSON format for each year.
"""

import json
import os
import geopandas as gpd
from pathlib import Path
from typing import Dict, List
import pandas as pd

def load_tpu_geojson(file_path: str) -> gpd.GeoDataFrame:
    """
    Load TPU boundary data from GeoJSON file.
    """
    try:
        gdf = gpd.read_file(file_path)
        print(f"  Loaded {len(gdf)} TPU boundaries from {file_path}")
        return gdf
    except Exception as e:
        print(f"  Error loading {file_path}: {e}")
        return None


def standardize_tpu_data(gdf: gpd.GeoDataFrame, year: str) -> gpd.GeoDataFrame:
    """
    Standardize TPU data format across different years.
    """
    if gdf is None or len(gdf) == 0:
        return None
    
    # Create a standardized GeoDataFrame
    standardized = gdf.copy()
    
    # Try to identify TPU identifier column (common names)
    # TPU codes are typically 3-digit numbers (e.g., 001, 002, etc.)
    tpu_id_cols = ['TPU', 'TPU_CODE', 'TPU_CODE_', 'CODE', 'TPU_ID', 'STPU', 'STPU_CODE', 
                   'TPUCODE', 'TPU_CD', 'ID', 'OBJECTID', 'FID']
    tpu_id_col = None
    
    for col in tpu_id_cols:
        if col in standardized.columns:
            # Check if this column contains TPU-like codes (3-digit numbers typically)
            sample_values = standardized[col].dropna().head(10)
            if len(sample_values) > 0:
                tpu_id_col = col
                break
    
    # If no standard ID column found, try to find any column with TPU-like codes
    if tpu_id_col is None:
        for col in standardized.columns:
            if col.upper() in ['TPU', 'CODE', 'ID'] or 'TPU' in col.upper():
                sample = standardized[col].dropna().head(5)
                # Check if values look like TPU codes (numeric, typically 3 digits)
                if len(sample) > 0:
                    try:
                        # Try to see if values are numeric codes
                        sample_str = sample.astype(str)
                        if all(len(str(v)) <= 4 and (str(v).isdigit() or str(v).startswith('0')) for v in sample_str):
                            tpu_id_col = col
                            break
                    except:
                        pass
    
    # If still no ID column found, create one
    if tpu_id_col is None:
        standardized['TPU_ID'] = standardized.index.astype(str).str.zfill(3)
        tpu_id_col = 'TPU_ID'
    else:
        # Use the found column and ensure proper formatting
        standardized['TPU_ID'] = standardized[tpu_id_col].astype(str)
        # Pad with zeros if needed to make 3-digit codes
        standardized['TPU_ID'] = standardized['TPU_ID'].str.zfill(3)
    
    # Add year column
    standardized['YEAR'] = year
    
    # Ensure geometry is valid
    standardized = standardized[standardized.geometry.notna()]
    standardized = standardized[standardized.geometry.is_valid]
    
    # Select key columns
    key_columns = ['TPU_ID', 'YEAR', 'geometry']
    
    # Add any other useful columns if they exist
    for col in ['NAME', 'TPU_NAME', 'DISTRICT', 'AREA']:
        if col in standardized.columns:
            key_columns.append(col)
    
    # Keep only key columns
    standardized = standardized[key_columns]
    
    # Ensure CRS is WGS84
    if standardized.crs is None:
        standardized.set_crs('EPSG:4326', inplace=True)
    else:
        standardized.to_crs('EPSG:4326', inplace=True)
    
    return standardized


def process_all_tpu_data(data_dir: str = None, output_dir: str = None):
    """
    Process all available TPU boundary data files.
    """
    # Get project root
    project_root = Path(__file__).parent.parent.parent
    if data_dir is None:
        data_dir = project_root / 'data' / 'raw' / 'tpu'
    if output_dir is None:
        output_dir = project_root / 'data' / 'processed' / 'tpu'
    """
    Process all available TPU boundary data files.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    data_path = Path(data_dir)
    output_path = Path(output_dir)
    processed_data = {}
    
    years = ['2001', '2006', '2011', '2016', '2021']
    
    print("=" * 60)
    print("Processing TPU Boundary Data")
    print("=" * 60)
    
    for year in years:
        geojson_file = data_path / f'tpu_boundaries_{year}.geojson'
        
        if not geojson_file.exists():
            print(f"\n{year}: File not found - {geojson_file}")
            continue
        
        print(f"\n{year}: Processing {geojson_file.name}...")
        
        # Load and standardize
        gdf = load_tpu_geojson(str(geojson_file))
        if gdf is not None:
            standardized = standardize_tpu_data(gdf, year)
            
            if standardized is not None:
                # Save processed version
                output_file = output_path / f'tpu_boundaries_{year}_processed.geojson'
                standardized.to_file(output_file, driver='GeoJSON')
                
                processed_data[year] = standardized
                
                print(f"  ✓ Processed {len(standardized)} TPU boundaries")
                print(f"  ✓ Saved to {output_file}")
                
                # Print summary statistics
                print(f"  Summary:")
                print(f"    - Total TPUs: {len(standardized)}")
                if 'NAME' in standardized.columns or 'TPU_NAME' in standardized.columns:
                    name_col = 'NAME' if 'NAME' in standardized.columns else 'TPU_NAME'
                    print(f"    - TPUs with names: {standardized[name_col].notna().sum()}")
    
    print(f"\n{'='*60}")
    print(f"Processing complete!")
    print(f"Processed data for {len(processed_data)} year(s)")
    print(f"{'='*60}")
    
    return processed_data


def main():
    """
    Main processing function.
    """
    processed_data = process_all_tpu_data()
    
    # Save summary
    summary = {
        'years_processed': list(processed_data.keys()),
        'counts': {year: len(gdf) for year, gdf in processed_data.items()}
    }
    
    project_root = Path(__file__).parent.parent.parent
    summary_file = project_root / 'data' / 'processed' / 'tpu' / 'summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSummary saved to {summary_file}")


if __name__ == '__main__':
    main()


