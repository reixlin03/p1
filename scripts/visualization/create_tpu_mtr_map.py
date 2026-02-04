#!/usr/bin/env python3
"""
Create interactive HTML map with TPU boundaries and MTR stations.
"""

import geopandas as gpd
import pandas as pd
import json
import os
from pathlib import Path
import folium
from folium import plugins

def load_mtr_stations(excel_file: str = None) -> pd.DataFrame:
    """
    Load MTR station data from Excel file.
    """
    if excel_file is None:
        project_root = Path(__file__).parent.parent.parent
        excel_file = project_root / 'data' / 'raw' / 'mtr' / 'mtr_stations.xlsx'
    """
    Load MTR station data from Excel file.
    """
    try:
        df = pd.read_excel(excel_file)
        # Filter stations with valid coordinates
        df = df[df['Latitude'].notna() & df['Longitude'].notna()]
        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
        df = df[df['Latitude'].notna() & df['Longitude'].notna()]
        print(f"Loaded {len(df)} MTR stations with coordinates")
        return df
    except Exception as e:
        print(f"Error loading MTR stations: {e}")
        return pd.DataFrame()


def load_tpu_boundaries(data_dir: str = None, use_spatial_join: bool = True) -> dict:
    """
    Load all processed TPU boundary data.
    If use_spatial_join is True, loads the spatial join data which includes MTR proximity info.
    """
    project_root = Path(__file__).parent.parent.parent
    
    if use_spatial_join:
        # Try to load spatial join data first (includes MTR proximity metrics)
        analysis_dir = project_root / 'data' / 'analysis'
        data_path = analysis_dir
    else:
        if data_dir is None:
            data_dir = project_root / 'data' / 'processed' / 'tpu'
        data_path = Path(data_dir)
    
    tpu_data = {}
    years = ['2001', '2006', '2011', '2016']  # Excluding 2021 as requested
    
    for year in years:
        if use_spatial_join:
            # Try spatial join file first
            file_path = data_path / f'mtr_tpu_spatial_join_{year}.geojson'
            if not file_path.exists():
                # Fallback to processed TPU boundaries
                file_path = project_root / 'data' / 'processed' / 'tpu' / f'tpu_boundaries_{year}_processed.geojson'
        else:
            file_path = data_path / f'tpu_boundaries_{year}_processed.geojson'
        
        if file_path.exists():
            try:
                gdf = gpd.read_file(file_path)
                tpu_data[year] = gdf
                source = "spatial join" if use_spatial_join and "spatial_join" in str(file_path) else "processed"
                print(f"Loaded {year} TPU boundaries: {len(gdf)} TPUs ({source})")
            except Exception as e:
                print(f"Error loading {year}: {e}")
    
    return tpu_data


def create_map(tpu_data: dict, mtr_stations: pd.DataFrame, output_file: str = None):
    """
    Create interactive HTML map with TPU boundaries and MTR stations.
    """
    if output_file is None:
        project_root = Path(__file__).parent.parent.parent
        output_file = project_root / 'outputs' / 'maps' / 'tpu_mtr_map.html'
    output_file = Path(output_file)
    os.makedirs(output_file.parent, exist_ok=True)
    
    # Hong Kong center coordinates
    hk_center = [22.3193, 114.1694]
    
    # Create base map
    m = folium.Map(
        location=hk_center,
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Add tile layer options
    folium.TileLayer('CartoDB positron', name='CartoDB Positron').add_to(m)
    folium.TileLayer('CartoDB dark_matter', name='CartoDB Dark Matter').add_to(m)
    
    # Color scheme for different years
    year_colors = {
        '2001': '#FF6B6B',  # Red
        '2006': '#4ECDC4',  # Teal
        '2011': '#45B7D1',  # Blue
        '2016': '#FFA07A',  # Light Salmon
        '2021': '#98D8C8'   # Mint
    }
    
    # Add TPU boundary layers for each year
    tpu_layers = {}
    # Get the most recent year to show by default
    years_available = sorted([int(y) for y in tpu_data.keys()])
    most_recent_year = str(years_available[-1]) if years_available else None
    
    for year, gdf in tpu_data.items():
        color = year_colors.get(year, '#808080')
        
        # Create GeoJSON layer
        geojson_data = json.loads(gdf.to_json())
        
        # Show most recent year by default, hide others
        show_by_default = (year == most_recent_year)
        
        # Enhanced style function that colors by MTR proximity if available
        def style_function(feature, color=color):
            style = {
                'fillColor': color,
                'color': color,
                'weight': 2,
                'fillOpacity': 0.3,
                'opacity': 0.7
            }
            
            # If spatial join data is available, color by MTR proximity
            props = feature.get('properties', {})
            if 'has_mtr_station' in props and props.get('has_mtr_station'):
                style['fillColor'] = '#00FF00'  # Green for TPUs with MTR stations
                style['fillOpacity'] = 0.5
            elif 'within_500m_buffer' in props and props.get('within_500m_buffer'):
                style['fillColor'] = '#90EE90'  # Light green for very close
                style['fillOpacity'] = 0.4
            elif 'within_1000m_buffer' in props and props.get('within_1000m_buffer'):
                style['fillColor'] = '#FFFF99'  # Yellow for close
                style['fillOpacity'] = 0.35
            
            return style
        
        layer = folium.GeoJson(
            geojson_data,
            name=f'TPU Boundaries {year}',
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(
                fields=[f for f in ['TPU_ID', 'YEAR', 'nearest_mtr_distance', 'nearest_mtr_station', 'has_mtr_station'] if f in gdf.columns],
                aliases=[f.replace('_', ' ').title() + ':' for f in ['TPU_ID', 'YEAR', 'nearest_mtr_distance', 'nearest_mtr_station', 'has_mtr_station'] if f in gdf.columns],
                localize=True
            ),
            show=show_by_default  # Show most recent year by default
        )
        
        layer.add_to(m)
        tpu_layers[year] = layer
    
    # Add MTR station markers
    if len(mtr_stations) > 0:
        mtr_group = folium.FeatureGroup(name='MTR Stations', show=True)
        
        # Tseung Kwan O line stations to highlight in purple
        tko_line_stations = [
            'Po Lam', 'Hang Hau', 'LOHAS Park', 'Tseung Kwan O', 'Tiu Keng Leng', 
            'Yau Tong', 'Quarry Bay', 'North Point'
        ]
        
        for idx, station in mtr_stations.iterrows():
            station_name = station.get('Station Name (English)', 'Unknown')
            chinese_name = station.get('Station Name (Chinese)', '')
            lines = station.get('Lines', '')
            lat = station['Latitude']
            lon = station['Longitude']
            code = station.get('Station Code', '')
            
            # Check if this is a Tseung Kwan O line station to highlight
            is_tko_station = any(tko_name.lower() in station_name.lower() for tko_name in tko_line_stations)
            
            # Set color based on station
            if is_tko_station:
                marker_color = '#800080'  # Purple for Tseung Kwan O line stations
                marker_fill = '#800080'
            else:
                marker_color = '#FFFFFF'  # White for other stations
                marker_fill = '#FFFFFF'
            
            # Create popup content
            popup_html = f"""
            <div style="min-width: 200px;">
                <h4 style="margin: 5px 0;">{station_name}</h4>
                {f'<p style="margin: 3px 0; color: #666;">{chinese_name}</p>' if chinese_name else ''}
                {f'<p style="margin: 3px 0;"><strong>Code:</strong> {code}</p>' if code else ''}
                {f'<p style="margin: 3px 0;"><strong>Lines:</strong> {lines}</p>' if lines else ''}
                {'<p style="margin: 3px 0; color: #800080;"><strong>📍 Tseung Kwan O Line</strong></p>' if is_tko_station else ''}
                <p style="margin: 3px 0; font-size: 0.9em; color: #888;">
                    <strong>Coordinates:</strong><br>
                    {lat:.6f}, {lon:.6f}
                </p>
            </div>
            """
            
            # Create marker
            folium.CircleMarker(
                location=[lat, lon],
                radius=8,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=station_name,
                color=marker_color,
                fillColor=marker_fill,
                fillOpacity=0.8,
                weight=2
            ).add_to(mtr_group)
        
        mtr_group.add_to(m)
    
    # Add layer control
    folium.LayerControl(collapsed=False).add_to(m)
    
    # Add fullscreen button
    plugins.Fullscreen().add_to(m)
    
    # Add measure tool
    plugins.MeasureControl().add_to(m)
    
    # Add draw plugin for custom annotations
    draw = plugins.Draw(
        export=True,
        filename='tpu_mtr_map_drawings.geojson',
        position='topleft',
        draw_options={
            'polyline': False,
            'rectangle': True,
            'polygon': True,
            'circle': False,
            'marker': True,
            'circlemarker': False
        }
    )
    draw.add_to(m)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 200px; height: auto; 
                background-color: white; z-index:9999; font-size:14px;
                border:2px solid grey; border-radius: 5px; padding: 10px">
    <h4 style="margin-top: 0;">TPU Boundary Years</h4>
    <p><span style="color: #FF6B6B;">■</span> 2001</p>
    <p><span style="color: #4ECDC4;">■</span> 2006</p>
    <p><span style="color: #45B7D1;">■</span> 2011</p>
    <p><span style="color: #FFA07A;">■</span> 2016</p>
    <hr>
    <p><span style="color: #FFFFFF; text-shadow: 1px 1px 2px #000;">●</span> MTR Stations</p>
    <p><span style="color: #800080;">●</span> Tseung Kwan O Line</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save map
    m.save(output_file)
    print(f"\nMap saved to: {output_file}")
    print(f"Open {output_file} in a web browser to view the interactive map.")


def main():
    """
    Main function to create the map.
    """
    print("=" * 60)
    print("Creating TPU & MTR Interactive Map")
    print("=" * 60)
    
    # Load data
    print("\nLoading TPU boundaries...")
    tpu_data = load_tpu_boundaries()
    
    print("\nLoading MTR stations...")
    mtr_stations = load_mtr_stations()
    
    if not tpu_data and len(mtr_stations) == 0:
        print("No data available to create map!")
        return
    
    # Create map
    print("\nCreating interactive map...")
    create_map(tpu_data, mtr_stations)
    
    print(f"\n{'='*60}")
    print("Map creation complete!")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()

