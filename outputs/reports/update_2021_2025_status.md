# Update Status: 2021 TPU Boundaries & 2025 MTR Stations

**Date:** 2025-12-29

## Summary

### ✅ MTR Stations - Updated to 2025
- **Total Stations:** 105 stations with verified coordinates
- **Status:** Up to date
- **Verification:** All stations verified against OpenStreetMap
- **Recent Updates:**
  - Airport station coordinates corrected (moved from Kowloon to HKIA)
  - 35 stations updated with more accurate coordinates
  - 70 stations verified as accurate

### ⚠️ TPU Boundaries - 2021 Data

**Status:** 2021 TPU boundaries not yet available through automated download

**Available Years:**
- ✅ 2001: 2,000 TPUs
- ✅ 2006: 1,999 TPUs  
- ✅ 2011: 1,999 TPUs
- ✅ 2016: 2,000 TPUs
- ⚠️ 2021: Not available (requires manual download)

**Manual Download Option:**
1. Visit: https://data.gov.hk/en-data/dataset/hk-pland-pland1-boundaries-of-tpu-sb-vc
2. Download the 2021 TPU boundary data
3. Save as: `data/raw/tpu/tpu_boundaries_2021.geojson`
4. Run: `python scripts/data_processing/process_tpu_data.py`
5. The map will automatically include 2021 boundaries once processed

**Note:** The map visualization script (`create_tpu_mtr_map.py`) already supports 2021 TPU boundaries. Once the data file is available, it will automatically be included in the map.

## MTR Station Verification

All major MTR lines and stations are included:
- ✅ Island Line
- ✅ Tsuen Wan Line
- ✅ Kwun Tong Line
- ✅ Tseung Kwan O Line
- ✅ East Rail Line
- ✅ West Rail Line
- ✅ Tuen Ma Line
- ✅ South Island Line
- ✅ Airport Express
- ✅ Tung Chung Line
- ✅ Disneyland Resort Line
- ✅ Ma On Shan Line

## Next Steps

1. **For 2021 TPU Data:**
   - Download manually from data.gov.hk
   - Process using existing scripts
   - Map will automatically update

2. **For Future MTR Updates:**
   - Run `scripts/data_collection/scrape_mtr_stations.py` periodically
   - Run `scripts/data_collection/verify_and_fix_mtr_coordinates.py` to verify accuracy

## Files Updated

- ✅ `data/raw/mtr/mtr_stations.xlsx` - Updated with verified 2025 coordinates
- ✅ `data/processed/mtr/mtr_stations_processed.geojson` - Reprocessed
- ✅ `outputs/maps/tpu_mtr_map.html` - Regenerated with updated stations
- ✅ `scripts/data_collection/download_tpu_2021.py` - Created for future 2021 TPU download

