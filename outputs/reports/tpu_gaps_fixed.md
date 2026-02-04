# TPU Boundary Gaps Fixed

**Date:** 2025-12-29

## Issue Identified

The TPU boundaries were incomplete due to pagination limits in the download script. Each year was only downloading 2,000 features when the actual totals were much higher.

## Problem

- **2001**: Only 2,000 features downloaded (missing 2,815)
- **2006**: Only 2,000 features downloaded (missing 2,977)
- **2011**: Only 2,000 features downloaded (missing 2,993)
- **2016**: Only 2,000 features downloaded (missing 3,034)

This caused visible gaps in the TPU boundary coverage on the map.

## Solution

Updated the download script (`download_tpu_simple.py`) to use pagination for all years, downloading all features in batches of 1,000 until complete.

## Results

### Complete TPU Boundary Counts

| Year | Previous | Complete | Added | Unique TPU IDs |
|------|----------|----------|-------|----------------|
| 2001 | 2,000    | 4,815    | +2,815 | 283            |
| 2006 | 2,000    | 4,976    | +2,976 | 287            |
| 2011 | 2,000    | 4,992    | +2,992 | 289            |
| 2016 | 2,000    | 5,033    | +3,033 | 291            |

### Updated Spatial Analysis

All years now have complete spatial analysis:

- **2001**: 4,815 TPUs analyzed, 98 TPUs with MTR stations
- **2006**: 4,976 TPUs analyzed, 99 TPUs with MTR stations
- **2011**: 4,992 TPUs analyzed, 99 TPUs with MTR stations
- **2016**: 5,033 TPUs analyzed, 99 TPUs with MTR stations

## Technical Details

### Download Method

The Esri ArcGIS REST API has a default maximum record count of 2,000 per query. To download all features, we implemented pagination:

```python
all_features = []
offset = 0
page_size = 1000

while True:
    params = {
        'where': '1=1',
        'outFields': '*',
        'f': 'geojson',
        'outSR': '4326',
        'resultOffset': offset,
        'resultRecordCount': page_size
    }
    # Download page...
    if len(features) < page_size:
        break  # Last page
    offset += page_size
```

### Service URLs

All TPU boundaries downloaded from:
```
https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/TPU_SB_VC_{YEAR}_PlanD_gdb/FeatureServer/0
```

## Verification

✅ All TPU boundaries now have complete coverage
✅ No gaps visible on the map
✅ Spatial analysis updated for all years
✅ Map regenerated with complete data

## Files Updated

1. `scripts/data_collection/download_tpu_simple.py` - Added pagination for all years
2. `data/raw/tpu/tpu_boundaries_*.geojson` - Complete datasets downloaded
3. `data/processed/tpu/tpu_boundaries_*_processed.geojson` - Reprocessed with complete data
4. `data/analysis/mtr_tpu_spatial_join_*.geojson` - Updated spatial analysis
5. `outputs/maps/tpu_mtr_map.html` - Regenerated map with complete boundaries

## Impact

The map now shows complete TPU boundary coverage for all years, eliminating gaps and providing accurate spatial analysis of MTR station proximity across Hong Kong.

