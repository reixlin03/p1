#!/usr/bin/env python3
"""
Scrape Hong Kong MTR station locations and export to Excel.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from typing import List, Dict
import time
import os

def scrape_mtr_stations() -> List[Dict]:
    """
    Scrape MTR station data from Wikipedia.
    Returns a list of dictionaries containing station information.
    """
    print("Fetching MTR station data from Wikipedia...")
    
    # Wikipedia page for MTR stations
    url = "https://en.wikipedia.org/wiki/List_of_MTR_stations"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching Wikipedia page: {e}")
        return []
    
    soup = BeautifulSoup(response.content, 'lxml')
    stations = []
    
    # Find all station tables - Wikipedia typically has tables with station data
    tables = soup.find_all('table', {'class': 'wikitable'})
    
    print(f"Found {len(tables)} potential data tables...")
    
    for table in tables:
        rows = table.find_all('tr')
        
        if len(rows) < 2:
            continue
        
        # Try to identify header row to understand column structure
        header_row = rows[0]
        headers = [th.get_text(strip=True).lower() for th in header_row.find_all(['th', 'td'])]
        
        # Skip header row
        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            
            if len(cells) < 1:
                continue
            
            station_data = {
                'Station Name (English)': '',
                'Station Name (Chinese)': '',
                'Lines': '',
                'Latitude': '',
                'Longitude': '',
                'Address': '',
                'Station Code': ''
            }
            
            # Extract station name (usually in first cell or link)
            name_cell = cells[0]
            
            # Try to get name from link first (more reliable)
            name_link = name_cell.find('a')
            if name_link:
                station_name = name_link.get_text(strip=True)
            else:
                station_name = name_cell.get_text(strip=True)
            
            # Remove reference numbers and clean up
            station_name = re.sub(r'\[\d+\]', '', station_name).strip()
            
            # Check if name contains Chinese characters in parentheses
            chinese_match = re.search(r'\(([^)]+)\)', station_name)
            if chinese_match:
                chinese_name = chinese_match.group(1)
                # Check if it contains Chinese characters
                if any('\u4e00' <= char <= '\u9fff' for char in chinese_name):
                    station_data['Station Name (Chinese)'] = chinese_name
                    # Remove Chinese name from English name
                    station_data['Station Name (English)'] = re.sub(r'\s*\([^)]+\)', '', station_name).strip()
                else:
                    station_data['Station Name (English)'] = station_name
            else:
                station_data['Station Name (English)'] = station_name
            
            # Extract lines - look for common line names in cells
            for i, cell in enumerate(cells):
                cell_text = cell.get_text(strip=True)
                cell_text = re.sub(r'\[\d+\]', '', cell_text)
                
                # Check if this cell contains line information
                line_keywords = ['island', 'tseung kwan o', 'tung chung', 'airport express', 
                               'disneyland', 'east rail', 'west rail', 'south island', 
                               'kwun tong', 'tuen ma', 'tseung kwan o']
                if any(keyword.lower() in cell_text.lower() for keyword in line_keywords):
                    if not station_data['Lines']:
                        station_data['Lines'] = cell_text
                    else:
                        station_data['Lines'] += ', ' + cell_text
            
            # Try to find coordinates from geohack links (most reliable)
            coord_links = row.find_all('a', href=re.compile(r'geohack'))
            for link in coord_links:
                href = link.get('href', '')
                if 'geohack' in href:
                    # Extract coordinates from geohack URL
                    # Format: params=22.284722_N_114.158611_E
                    coord_match = re.search(r'params=([\d.]+)_([NS])_([\d.]+)_([EW])', href)
                    if coord_match:
                        lat_val = float(coord_match.group(1))
                        lat_dir = coord_match.group(2)
                        lon_val = float(coord_match.group(3))
                        lon_dir = coord_match.group(4)
                        
                        lat = lat_val if lat_dir == 'N' else -lat_val
                        lon = lon_val if lon_dir == 'E' else -lon_val
                        
                        station_data['Latitude'] = f"{lat:.6f}"
                        station_data['Longitude'] = f"{lon:.6f}"
                        break
            
            # Also check for coordinate spans (Wikipedia uses span class="geo")
            if not station_data['Latitude']:
                geo_spans = row.find_all('span', {'class': 'geo'})
                for span in geo_spans:
                    geo_text = span.get_text()
                    # Format: "22.284722; 114.158611"
                    coord_match = re.search(r'([\d.]+)\s*[;，,]\s*([\d.]+)', geo_text)
                    if coord_match:
                        lat = float(coord_match.group(1))
                        lon = float(coord_match.group(2))
                        station_data['Latitude'] = f"{lat:.6f}"
                        station_data['Longitude'] = f"{lon:.6f}"
                        break
            
            # If no geohack link, try to find coordinates in text
            if not station_data['Latitude']:
                for cell in cells:
                    cell_text = cell.get_text()
                    # Look for coordinate patterns like "22.284722°N 114.158611°E"
                    coord_match = re.search(r'(\d+\.\d+)[°\s]*([NS])?\s*[,，\s]+\s*(\d+\.\d+)[°\s]*([EW])?', cell_text)
                    if coord_match:
                        lat_val = float(coord_match.group(1))
                        lat_dir = coord_match.group(2) or 'N'
                        lon_val = float(coord_match.group(3))
                        lon_dir = coord_match.group(4) or 'E'
                        
                        lat = lat_val if lat_dir == 'N' else -lat_val
                        lon = lon_val if lon_dir == 'E' else -lon_val
                        
                        station_data['Latitude'] = f"{lat:.6f}"
                        station_data['Longitude'] = f"{lon:.6f}"
                        break
            
            # Try to find station code (typically 2-3 uppercase letters)
            for cell in cells:
                cell_text = cell.get_text(strip=True)
                # MTR station codes are typically 2-3 uppercase letters
                if re.match(r'^[A-Z]{2,3}$', cell_text) and len(cell_text) >= 2:
                    station_data['Station Code'] = cell_text
                    break
            
            # Only add if we have at least a station name
            if station_data['Station Name (English)']:
                stations.append(station_data)
    
    print(f"Scraped {len(stations)} stations from Wikipedia tables.")
    
    # If we didn't get enough stations, try to get more from individual station pages
    if len(stations) < 50:
        print("Trying to fetch additional station data...")
        # Try alternative method
        additional_stations = scrape_mtr_stations_alternative(soup)
        # Merge without duplicates
        existing_names = {s['Station Name (English)'] for s in stations}
        for station in additional_stations:
            if station['Station Name (English)'] not in existing_names:
                stations.append(station)
    
    return stations


def scrape_mtr_stations_alternative(soup: BeautifulSoup) -> List[Dict]:
    """
    Alternative scraping method using infoboxes and station lists.
    """
    stations = []
    
    # Look for station list items or infoboxes
    station_links = soup.find_all('a', href=re.compile(r'/wiki/[^/]+_station'))
    
    for link in station_links:
        station_name = link.get_text(strip=True)
        if not station_name or len(station_name) < 2:
            continue
        
        # Skip if it's clearly not a station
        if any(word in station_name.lower() for word in ['list', 'category', 'template']):
            continue
        
        station_data = {
            'Station Name (English)': station_name,
            'Station Name (Chinese)': '',
            'Lines': '',
            'Latitude': '',
            'Longitude': '',
            'Address': '',
            'Station Code': ''
        }
        
        stations.append(station_data)
    
    return stations


def get_coordinates_from_station_page(station_name: str) -> tuple:
    """
    Fetch coordinates from individual station Wikipedia page.
    Returns (latitude, longitude) tuple or (None, None) if not found.
    """
    # Construct Wikipedia URL
    wiki_url = f"https://en.wikipedia.org/wiki/{station_name.replace(' ', '_')}_station"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(wiki_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return (None, None)
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Look for geohack links
        coord_links = soup.find_all('a', href=re.compile(r'geohack'))
        for link in coord_links:
            href = link.get('href', '')
            if 'geohack' in href:
                coord_match = re.search(r'params=([\d.]+)_([NS])_([\d.]+)_([EW])', href)
                if coord_match:
                    lat_val = float(coord_match.group(1))
                    lat_dir = coord_match.group(2)
                    lon_val = float(coord_match.group(3))
                    lon_dir = coord_match.group(4)
                    
                    lat = lat_val if lat_dir == 'N' else -lat_val
                    lon = lon_val if lon_dir == 'E' else -lon_val
                    
                    return (lat, lon)
        
        # Look for coordinates in infobox
        infobox = soup.find('table', {'class': 'infobox'})
        if infobox:
            coord_links = infobox.find_all('a', href=re.compile(r'geohack'))
            for link in coord_links:
                href = link.get('href', '')
                if 'geohack' in href:
                    coord_match = re.search(r'params=([\d.]+)_([NS])_([\d.]+)_([EW])', href)
                    if coord_match:
                        lat_val = float(coord_match.group(1))
                        lat_dir = coord_match.group(2)
                        lon_val = float(coord_match.group(3))
                        lon_dir = coord_match.group(4)
                        
                        lat = lat_val if lat_dir == 'N' else -lat_val
                        lon = lon_val if lon_dir == 'E' else -lon_val
                        
                        return (lat, lon)
        
    except Exception as e:
        pass
    
    return (None, None)


def geocode_station(station_name: str, location_hint: str = "Hong Kong") -> tuple:
    """
    Geocode station name using Nominatim (OpenStreetMap) free geocoding service.
    Returns (latitude, longitude) tuple or (None, None) if not found.
    """
    try:
        # Use Nominatim geocoding API
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': f"{station_name} MTR station, {location_hint}",
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'MTR Station Scraper'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return (lat, lon)
    except Exception as e:
        pass
    
    return (None, None)


def enhance_station_data(stations: List[Dict]) -> List[Dict]:
    """
    Enhance station data by fetching coordinates for stations that don't have them.
    """
    print("Enhancing station data with coordinates...")
    
    stations_without_coords = [s for s in stations if not s['Latitude'] or not s['Longitude']]
    print(f"Found {len(stations_without_coords)} stations without coordinates. Fetching...")
    
    for i, station in enumerate(stations_without_coords, 1):
        station_name = station['Station Name (English)']
        print(f"  [{i}/{len(stations_without_coords)}] Fetching coordinates for {station_name}...")
        
        # Try to get from individual station page first
        lat, lon = get_coordinates_from_station_page(station_name)
        
        # If not found, try geocoding
        if lat is None or lon is None:
            lat, lon = geocode_station(station_name)
        
        if lat is not None and lon is not None:
            # Validate coordinates are in Hong Kong
            if 22.0 <= lat <= 23.0 and 113.0 <= lon <= 115.0:
                station['Latitude'] = f"{lat:.6f}"
                station['Longitude'] = f"{lon:.6f}"
                print(f"    ✓ Found coordinates: {lat:.6f}, {lon:.6f}")
            else:
                print(f"    ✗ Coordinates out of range: {lat:.6f}, {lon:.6f}")
        else:
            print(f"    ✗ Could not find coordinates")
        
        # Be polite to the API - add a small delay
        time.sleep(1)
    
    return stations


def clean_and_validate_data(stations: List[Dict]) -> List[Dict]:
    """
    Clean and validate the scraped station data.
    """
    print("Cleaning and validating data...")
    
    cleaned_stations = []
    seen_names = set()
    
    for station in stations:
        # Remove duplicates based on station name
        name = station['Station Name (English)'].strip()
        if not name or name in seen_names:
            continue
        
        seen_names.add(name)
        
        # Clean up lines data
        if station['Lines']:
            # Remove extra whitespace and normalize
            station['Lines'] = ' '.join(station['Lines'].split())
        
        # Validate coordinates
        if station['Latitude'] and station['Longitude']:
            try:
                lat = float(station['Latitude'])
                lon = float(station['Longitude'])
                # Hong Kong is roughly between 22.1-22.6 N and 113.8-114.4 E
                if not (22.0 <= lat <= 23.0) or not (113.0 <= lon <= 115.0):
                    # Coordinates might be invalid, clear them
                    station['Latitude'] = ''
                    station['Longitude'] = ''
            except ValueError:
                station['Latitude'] = ''
                station['Longitude'] = ''
        
        cleaned_stations.append(station)
    
    print(f"After cleaning: {len(cleaned_stations)} unique stations.")
    return cleaned_stations


def export_to_excel(stations: List[Dict], filename: str = None):
    """
    Export station data to Excel file.
    """
    if filename is None:
        from pathlib import Path
        project_root = Path(__file__).parent.parent.parent
        filename = project_root / 'data' / 'raw' / 'mtr' / 'mtr_stations.xlsx'
        os.makedirs(Path(filename).parent, exist_ok=True)
    
    print(f"Exporting {len(stations)} stations to {filename}...")
    
    if not stations:
        print("No stations to export!")
        return
    
    # Create DataFrame
    df = pd.DataFrame(stations)
    
    # Reorder columns for better readability
    column_order = [
        'Station Name (English)',
        'Station Name (Chinese)',
        'Station Code',
        'Lines',
        'Latitude',
        'Longitude',
        'Address'
    ]
    
    # Only include columns that exist
    column_order = [col for col in column_order if col in df.columns]
    df = df[column_order]
    
    # Export to Excel
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='MTR Stations', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['MTR Stations']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
        
        # Count stations with coordinates
        stations_with_coords = sum(1 for s in stations if s.get('Latitude') and s.get('Longitude'))
        
        print(f"Successfully exported to {filename}")
        print(f"Total stations: {len(stations)}")
        print(f"Stations with coordinates: {stations_with_coords} ({stations_with_coords/len(stations)*100:.1f}%)")
        
    except Exception as e:
        print(f"Error exporting to Excel: {e}")
        # Fallback to CSV
        csv_filename = filename.replace('.xlsx', '.csv')
        df.to_csv(csv_filename, index=False)
        print(f"Exported to CSV instead: {csv_filename}")


def main():
    """
    Main function to orchestrate the scraping and export process.
    """
    print("=" * 60)
    print("Hong Kong MTR Station Scraper")
    print("=" * 60)
    
    # Scrape stations
    stations = scrape_mtr_stations()
    
    if not stations:
        print("No stations found. Trying alternative data source...")
        # Could implement fallback to MTR official website here
        return
    
    # Clean and validate
    stations = clean_and_validate_data(stations)
    
    # Enhance with coordinates for stations that don't have them
    stations = enhance_station_data(stations)
    
    # Export to Excel
    export_to_excel(stations)
    
    print("=" * 60)
    print("Scraping complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()

