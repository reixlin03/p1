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


def load_new_town_boundaries(shp_file: str = None) -> gpd.GeoDataFrame:
    """
    Load New Town boundaries from shapefile.
    """
    if shp_file is None:
        project_root = Path(__file__).parent.parent.parent
        shp_file = project_root.parent / 'BoundariesofNewTownsfor2006PopulationBycensus_SHP' / 'NewTown_2006.shp'
    
    shp_path = Path(shp_file)
    if not shp_path.exists():
        print(f"New Town boundaries file not found: {shp_path}")
        return None
    
    try:
        gdf = gpd.read_file(shp_path)
        # Convert to WGS84 to match the map
        if gdf.crs is None:
            # Assume it's in Hong Kong 1980 Grid System (EPSG:2326)
            gdf.set_crs('EPSG:2326', inplace=True)
        gdf = gdf.to_crs('EPSG:4326')
        print(f"Loaded {len(gdf)} New Town boundaries")
        return gdf
    except Exception as e:
        print(f"Error loading New Town boundaries: {e}")
        return None


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


def create_map(tpu_data: dict, mtr_stations: pd.DataFrame, new_town_boundaries: gpd.GeoDataFrame = None, output_file: str = None):
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
        
        # Yellow stations
        yellow_stations = [
            'Tuen Mun', 'Siu Hong', 'Tin Shui Wai', 'Long Ping', 'Yuen Long', 
            'Kam Sheung Road', 'Tsuen Wan West', 'Mei Foo', 'Nam Cheong'
        ]
        
        # Blue stations
        blue_stations = [
            'Wu Kai Sha', 'Ma On Shan', 'Heng On', 'Tai Shui Hang', 'Shek Mun', 
            'City One', 'Sha Tin Wai', 'Che Kung Temple', 'Tai Wai'
        ]
        
        for idx, station in mtr_stations.iterrows():
            station_name = station.get('Station Name (English)', 'Unknown')
            chinese_name = station.get('Station Name (Chinese)', '')
            lines = station.get('Lines', '')
            lat = station['Latitude']
            lon = station['Longitude']
            code = station.get('Station Code', '')
            
            # Check station category
            is_tko_station = any(tko_name.lower() in station_name.lower() for tko_name in tko_line_stations)
            is_yellow_station = any(yellow_name.lower() in station_name.lower() for yellow_name in yellow_stations)
            is_blue_station = any(blue_name.lower() in station_name.lower() for blue_name in blue_stations)
            
            # Set color based on station category (priority: purple > yellow > blue > white)
            if is_tko_station:
                marker_color = '#800080'  # Purple for Tseung Kwan O line stations
                marker_fill = '#800080'
                category_label = '📍 Tseung Kwan O Line'
                category_color = '#800080'
            elif is_yellow_station:
                marker_color = '#FFD700'  # Yellow (Gold)
                marker_fill = '#FFD700'
                category_label = '📍 West Rail'
                category_color = '#FFD700'
            elif is_blue_station:
                marker_color = '#0000FF'  # Blue
                marker_fill = '#0000FF'
                category_label = '📍 Ma On Shan Line'
                category_color = '#0000FF'
            else:
                marker_color = '#FFFFFF'  # White for other stations
                marker_fill = '#FFFFFF'
                category_label = ''
                category_color = ''
            
            # Create popup content
            popup_html = f"""
            <div style="min-width: 200px;">
                <h4 style="margin: 5px 0;">{station_name}</h4>
                {f'<p style="margin: 3px 0; color: #666;">{chinese_name}</p>' if chinese_name else ''}
                {f'<p style="margin: 3px 0;"><strong>Code:</strong> {code}</p>' if code else ''}
                {f'<p style="margin: 3px 0;"><strong>Lines:</strong> {lines}</p>' if lines else ''}
                {f'<p style="margin: 3px 0; color: {category_color};"><strong>{category_label}</strong></p>' if category_label else ''}
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
    
    # Add New Town boundaries layer
    if new_town_boundaries is not None and len(new_town_boundaries) > 0:
        new_town_group = folium.FeatureGroup(name='New Town Boundaries (2006)', show=True)
        
        # Create GeoJSON from New Town boundaries
        new_town_geojson = json.loads(new_town_boundaries.to_json())
        
        # Style function for New Town boundaries
        def new_town_style(feature):
            return {
                'fillColor': '#FFA500',  # Orange
                'color': '#FF8C00',      # Dark orange border
                'weight': 3,
                'fillOpacity': 0.2,
                'opacity': 0.8,
                'dashArray': '5, 5'      # Dashed line
            }
        
        # Add tooltip with New Town name
        def new_town_tooltip(feature):
            props = feature.get('properties', {})
            name_en = props.get('NewTown_en', 'Unknown')
            name_tc = props.get('NewTown_Tc', '')
            return f"{name_en}" + (f" ({name_tc})" if name_tc else "")
        
        # Add popup with more details
        def new_town_popup(feature):
            props = feature.get('properties', {})
            name_en = props.get('NewTown_en', 'Unknown')
            name_tc = props.get('NewTown_Tc', '')
            name_sc = props.get('NewTown_Sc', '')
            
            popup_html = f"""
            <div style="min-width: 200px;">
                <h4 style="margin: 5px 0; color: #FF8C00;">{name_en}</h4>
                {f'<p style="margin: 3px 0; color: #666;">{name_tc}</p>' if name_tc else ''}
                {f'<p style="margin: 3px 0; color: #666;">{name_sc}</p>' if name_sc else ''}
                <p style="margin: 3px 0; font-size: 0.9em; color: #888;">
                    <strong>New Town Boundary (2006 Census)</strong>
                </p>
            </div>
            """
            return popup_html
        
        # Add GeoJSON layer
        folium.GeoJson(
            new_town_geojson,
            style_function=new_town_style,
            tooltip=folium.GeoJsonTooltip(
                fields=['NewTown_en', 'NewTown_Tc'],
                aliases=['New Town: ', '新市鎮: '],
                style=('background-color: white; font-size: 12px; padding: 5px;')
            ),
            popup=folium.GeoJsonPopup(
                fields=['NewTown_en', 'NewTown_Tc', 'NewTown_Sc'],
                aliases=['English: ', 'Traditional Chinese: ', 'Simplified Chinese: '],
                style='font-size: 12px;'
            )
        ).add_to(new_town_group)
        
        new_town_group.add_to(m)
    
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
                bottom: 50px; right: 50px; width: 220px; height: auto; 
                background-color: white; z-index:9999; font-size:14px;
                border:2px solid grey; border-radius: 5px; padding: 10px">
    <h4 style="margin-top: 0;">TPU Boundary Years</h4>
    <p><span style="color: #FF6B6B;">■</span> 2001</p>
    <p><span style="color: #4ECDC4;">■</span> 2006</p>
    <p><span style="color: #45B7D1;">■</span> 2011</p>
    <p><span style="color: #FFA07A;">■</span> 2016</p>
    <hr>
    <p><strong>MTR Stations:</strong></p>
    <p><span style="color: #FFFFFF; text-shadow: 1px 1px 2px #000;">●</span> Other Stations</p>
    <p><span style="color: #800080;">●</span> Tseung Kwan O Line</p>
    <p><span style="color: #FFD700;">●</span> West Rail</p>
    <p><span style="color: #0000FF;">●</span> Ma On Shan Line</p>
    <hr>
    <p><strong>Other Layers:</strong></p>
    <p><span style="color: #FFA500; border: 2px dashed #FF8C00;">━</span> New Town Boundaries (2006)</p>
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
    
    print("\nLoading New Town boundaries...")
    new_town_boundaries = load_new_town_boundaries()
    
    if not tpu_data and len(mtr_stations) == 0:
        print("No data available to create map!")
        return
    
    # Create map
    print("\nCreating interactive map...")
    create_map(tpu_data, mtr_stations, new_town_boundaries)
    
    print(f"\n{'='*60}")
    print("Map creation complete!")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()

