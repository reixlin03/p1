# Esri TPU Boundary Service Links

## Direct Service URLs

### 2001 TPU Boundaries
**Feature Service:**
```
https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2001_PlanD_gdb/FeatureServer/0
```

**Query Endpoint (GeoJSON):**
```
https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2001_PlanD_gdb/FeatureServer/0/query?where=1%3D1&outFields=*&f=geojson&outSR=4326
```

**Parameters:**
- `where`: 1=1 (all features)
- `outFields`: * (all fields)
- `f`: geojson (output format)
- `outSR`: 4326 (WGS84 coordinate system)

---

### 2006 TPU Boundaries
**Feature Service:**
```
https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2006_PlanD_gdb/FeatureServer/0
```

**Query Endpoint (GeoJSON):**
```
https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2006_PlanD_gdb/FeatureServer/0/query?where=1%3D1&outFields=*&f=geojson&outSR=4326
```

---

### 2011 TPU Boundaries
**Feature Service:**
```
https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2011_PlanD_gdb/FeatureServer/0
```

**Query Endpoint (GeoJSON):**
```
https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2011_PlanD_gdb/FeatureServer/0/query?where=1%3D1&outFields=*&f=geojson&outSR=4326
```

---

### 2016 TPU Boundaries
**Feature Service:**
```
https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2016_PlanD_gdb/FeatureServer/0
```

**Query Endpoint (GeoJSON):**
```
https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_2016_PlanD_gdb/FeatureServer/0/query?where=1%3D1&outFields=*&f=geojson&outSR=4326
```

---

## Base Service URL Pattern

All TPU boundary services follow this pattern:
```
https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_{YEAR}_PlanD_gdb/FeatureServer/0
```

Where `{YEAR}` is: `2001`, `2006`, `2011`, or `2016`

## Service Information

- **Provider:** Esri China Open Data Portal / Hong Kong Planning Department
- **Coordinate System:** WGS84 (EPSG:4326)
- **Format:** GeoJSON (via query endpoint)
- **Data Source:** Hong Kong Planning Department / Census and Statistics Department

## Usage Examples

### Download via Python (requests)
```python
import requests

year = '2016'
url = f"https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_{year}_PlanD_gdb/FeatureServer/0/query"

params = {
    'where': '1=1',
    'outFields': '*',
    'f': 'geojson',
    'outSR': '4326',
    'resultRecordCount': 10000
}

response = requests.get(url, params=params)
data = response.json()
```

### View in ArcGIS Online
You can view these services in ArcGIS Online by adding them as a layer:
1. Go to ArcGIS Online Map Viewer
2. Click "Add" → "Add Layer from Web"
3. Select "An ArcGIS Server Web Service"
4. Paste the Feature Service URL above

## Notes

- These services are publicly accessible
- No authentication required
- Data is updated by the Hong Kong Planning Department
- TPU boundaries represent Tertiary Planning Units (TPUs), Street Blocks (SB), and Village Clusters (VC)

