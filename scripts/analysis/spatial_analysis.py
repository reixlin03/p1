#!/usr/bin/env python3
"""
Spatial analysis: Join MTR stations to TPUs and calculate proximity metrics.
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
import os
from shapely.geometry import Point
import numpy as np

def load_mtr_stations() -> gpd.GeoDataFrame:
    """
    Load processed MTR station data.
    """
    project_root = Path(__file__).parent.parent.parent
    mtr_file = project_root / 'data' / 'processed' / 'mtr' / 'mtr_stations_processed.geojson'
    
    if not mtr_file.exists():
        # Try to process MTR data first
        from scripts.data_processing.process_mtr_data import process_mtr_stations
        process_mtr_stations()
    
    if mtr_file.exists():
        return gpd.read_file(mtr_file)
    else:
        print("Error: MTR stations file not found")
        return gpd.GeoDataFrame()


def calculate_proximity_metrics(tpu_gdf: gpd.GeoDataFrame, mtr_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Calculate proximity metrics for each TPU to MTR stations.
    """
    print("Calculating proximity metrics...")
    
    # Convert to projected CRS for accurate distance calculations (Hong Kong uses EPSG:2326)
    # Use a local projection for Hong Kong
    hk_crs = 'EPSG:2326'  # Hong Kong 1980 Grid System
    tpu_gdf_proj = tpu_gdf.to_crs(hk_crs)
    mtr_gdf_proj = mtr_gdf.to_crs(hk_crs)
    
    # Calculate distance to nearest MTR station for each TPU
    # Use centroid of TPU for distance calculation
    tpu_centroids = tpu_gdf_proj.geometry.centroid
    
    # Create spatial index for faster lookups
    mtr_sindex = mtr_gdf_proj.sindex
    
    # Initialize columns
    tpu_gdf['nearest_mtr_distance'] = np.nan
    tpu_gdf['nearest_mtr_station'] = None
    tpu_gdf['nearest_mtr_lat'] = np.nan
    tpu_gdf['nearest_mtr_lon'] = np.nan
    tpu_gdf['mtr_stations_count'] = 0
    tpu_gdf['has_mtr_station'] = False
    
    # Calculate distances (in projected CRS, distance is already in meters)
    for idx, centroid in enumerate(tpu_centroids):
        # Find nearest MTR station
        nearest_idx = mtr_gdf_proj.distance(centroid).idxmin()
        nearest_station_proj = mtr_gdf_proj.loc[nearest_idx]
        nearest_station = mtr_gdf.loc[nearest_idx]  # Get original for lat/lon
        
        # Calculate distance in meters (already in meters in projected CRS)
        distance_m = centroid.distance(nearest_station_proj.geometry)
        
        tpu_gdf.loc[tpu_gdf.index[idx], 'nearest_mtr_distance'] = distance_m
        tpu_gdf.loc[tpu_gdf.index[idx], 'nearest_mtr_station'] = nearest_station.get('Station Name (English)', 'Unknown')
        tpu_gdf.loc[tpu_gdf.index[idx], 'nearest_mtr_lat'] = nearest_station.geometry.y
        tpu_gdf.loc[tpu_gdf.index[idx], 'nearest_mtr_lon'] = nearest_station.geometry.x
        
        # Check if TPU contains any MTR station (use projected CRS)
        tpu_geom_proj = tpu_gdf_proj.loc[tpu_gdf_proj.index[idx], 'geometry']
        contains_station = mtr_gdf_proj.geometry.within(tpu_geom_proj).any()
        tpu_gdf.loc[tpu_gdf.index[idx], 'has_mtr_station'] = contains_station
        
        # Count stations within TPU
        stations_in_tpu = mtr_gdf_proj.geometry.within(tpu_geom_proj).sum()
        tpu_gdf.loc[tpu_gdf.index[idx], 'mtr_stations_count'] = stations_in_tpu
    
    # Create proximity categories
    tpu_gdf['mtr_proximity_category'] = pd.cut(
        tpu_gdf['nearest_mtr_distance'],
        bins=[0, 500, 1000, 2000, float('inf')],
        labels=['Very Close (<500m)', 'Close (500-1000m)', 'Moderate (1-2km)', 'Far (>2km)']
    )
    
    print(f"  Calculated proximity for {len(tpu_gdf)} TPUs")
    print(f"  TPUs with MTR stations: {tpu_gdf['has_mtr_station'].sum()}")
    print(f"  Average distance to nearest MTR: {tpu_gdf['nearest_mtr_distance'].mean():.0f}m")
    
    return tpu_gdf


def create_buffer_analysis(tpu_gdf: gpd.GeoDataFrame, mtr_gdf: gpd.GeoDataFrame, 
                           buffer_distances: list = [500, 1000, 2000]) -> gpd.GeoDataFrame:
    """
    Create buffer analysis: identify TPUs within walking distance of MTR stations.
    """
    print("Creating buffer analysis...")
    
    # Convert to projected CRS for accurate buffer calculations
    hk_crs = 'EPSG:2326'  # Hong Kong 1980 Grid System
    tpu_gdf_proj = tpu_gdf.to_crs(hk_crs)
    mtr_gdf_proj = mtr_gdf.to_crs(hk_crs)
    
    # Create buffers (distance is already in meters in projected CRS)
    for buffer_m in buffer_distances:
        # Create buffers around MTR stations (buffer distance in meters)
        mtr_buffers = mtr_gdf_proj.geometry.buffer(buffer_m)
        
        # Check which TPUs intersect with buffers
        col_name = f'within_{buffer_m}m_buffer'
        tpu_gdf[col_name] = False
        
        for idx, tpu_geom_proj in enumerate(tpu_gdf_proj.geometry):
            intersects = mtr_buffers.intersects(tpu_geom_proj).any()
            tpu_gdf.loc[tpu_gdf.index[idx], col_name] = intersects
        
        count = tpu_gdf[col_name].sum()
        print(f"  TPUs within {buffer_m}m of MTR stations: {count}")
    
    return tpu_gdf


def spatial_join_mtr_tpu(year: str = None):
    """
    Perform spatial join between MTR stations and TPU boundaries.
    """
    project_root = Path(__file__).parent.parent.parent
    
    # Load MTR stations
    mtr_gdf = load_mtr_stations()
    if mtr_gdf.empty:
        print("Error: No MTR stations loaded")
        return
    
    # Process each year or specific year
    years = [year] if year else ['2001', '2006', '2011', '2016', '2021']
    
    print("=" * 60)
    print("Spatial Analysis: MTR-TPU Join")
    print("=" * 60)
    
    for year in years:
        print(f"\nProcessing {year}...")
        
        # Load TPU boundaries
        tpu_file = project_root / 'data' / 'processed' / 'tpu' / f'tpu_boundaries_{year}_processed.geojson'
        
        if not tpu_file.exists():
            print(f"  TPU boundaries not found for {year}, skipping...")
            continue
        
        tpu_gdf = gpd.read_file(tpu_file)
        
        # Calculate proximity metrics
        tpu_gdf = calculate_proximity_metrics(tpu_gdf, mtr_gdf)
        
        # Create buffer analysis
        tpu_gdf = create_buffer_analysis(tpu_gdf, mtr_gdf)
        
        # Save results
        output_dir = project_root / 'data' / 'analysis'
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = output_dir / f'mtr_tpu_spatial_join_{year}.geojson'
        tpu_gdf.to_file(output_file, driver='GeoJSON')
        
        # Also save as CSV
        csv_file = output_dir / f'mtr_tpu_spatial_join_{year}.csv'
        tpu_gdf.drop(columns=['geometry']).to_csv(csv_file, index=False)
        
        print(f"  Saved results to {output_file} and {csv_file}")
    
    # Create combined dataset
    print("\nCreating combined spatial analysis dataset...")
    combined_data = []
    
    for year in years:
        csv_file = project_root / 'data' / 'analysis' / f'mtr_tpu_spatial_join_{year}.csv'
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            df['year'] = year
            combined_data.append(df)
    
    if combined_data:
        combined_df = pd.concat(combined_data, ignore_index=True)
        combined_file = project_root / 'data' / 'analysis' / 'mtr_tpu_spatial_join_all_years.csv'
        combined_df.to_csv(combined_file, index=False)
        print(f"  Saved combined dataset to {combined_file}")
    
    print("\n" + "=" * 60)
    print("Spatial analysis complete!")
    print("=" * 60)


if __name__ == '__main__':
    spatial_join_mtr_tpu()

