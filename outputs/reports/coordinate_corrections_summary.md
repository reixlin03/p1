# MTR Station Coordinate Corrections Summary

## Issue Identified

The original MTR station coordinates were scraped from Wikipedia, which led to several inaccuracies in station placements. Some stations had coordinates that were significantly off from their actual locations.

## Verification Process

**Source Used:** OpenStreetMap (Nominatim API) - a reliable, community-maintained geographic database

**Method:**
1. Cross-referenced all existing coordinates with OpenStreetMap data
2. Calculated distance differences between existing and OSM coordinates
3. Updated stations with >100m difference (indicating significant error)
4. Fetched missing coordinates for stations without data

## Results

### Summary Statistics
- **Total stations processed:** 113 valid stations
- **Stations verified as accurate:** 74 (within 100m of OSM)
- **Stations corrected:** 31 (had errors >100m)
- **Stations not found:** 8 (invalid entries or duplicates)

### Notable Corrections

Several stations had significant errors that were corrected:

1. **Wan Chai** - **6.7 km error corrected!**
   - Old: 22.277300, 114.172800
   - New: 22.264453, 114.237044

2. **Mong Kok** - 428m error corrected
   - Updated to more accurate location

3. **Causeway Bay** - 108m error corrected
   - Old: 22.280200, 114.183500
   - New: 22.279392, 114.182926

4. **Central** - Missing coordinates added
   - New: 22.281938, 114.158077

5. **Tsim Sha Tsui** - Verified accurate (75m difference, within tolerance)

### Other Significant Corrections (>100m)
- Kowloon Tong: 110m
- Fanling: 158m
- Whampoa: 126m
- Ho Man Tin: 145m
- Wong Tai Sin: 187m
- Choi Hung: 152m
- Kwun Tong: 130m
- Tai Wo Hau: 139m
- Mei Foo: 332m
- Sham Shui Po: 116m
- Sheung Wan: 199m
- Sunny Bay: 100m
- Tsing Yi: 210m
- Nam Cheong: 135m
- AsiaWorld–Expo: 107m
- Sung Wong Toi: 109m
- East Tsim Sha Tsui: 161m
- Tsuen Wan West: 108m
- Long Ping: 270m
- Tin Shui Wai: 223m
- Siu Hong: 148m
- Tuen Mun: 145m

## Data Source Information

### Original Source
- **Method:** Web scraping from Wikipedia
- **Issues:** 
  - Inconsistent coordinate extraction
  - Some stations had missing coordinates
  - Geocoding fallback sometimes produced inaccurate results

### New Source
- **Method:** OpenStreetMap Nominatim API
- **Advantages:**
  - Community-verified and maintained
  - More accurate and up-to-date
  - Standardized coordinate format
  - Better coverage of Hong Kong MTR stations

## Coordinate System

- **Format:** WGS84 (EPSG:4326)
- **Order:** Latitude, Longitude
- **Precision:** 6 decimal places (~0.1m accuracy)
- **Validation:** All coordinates verified to be within Hong Kong bounds (22.0-23.0°N, 113.0-115.0°E)

## Files Updated

1. **`data/raw/mtr/mtr_stations.xlsx`** - Updated with corrected coordinates
2. **`data/processed/mtr/mtr_stations_processed.geojson`** - Reprocessed with new coordinates
3. **`outputs/maps/tpu_mtr_map.html`** - Regenerated with accurate station locations
4. **`outputs/dashboards/interactive_dashboard.html`** - Regenerated with accurate station locations

## Verification Report

A detailed verification report is available at:
`outputs/reports/mtr_coordinates_verification.md`

## Next Steps

1. ✅ Coordinates verified and corrected
2. ✅ Maps regenerated with accurate locations
3. ✅ Dashboard updated
4. ⚠️  Review the 8 stations that couldn't be found - these may be duplicates or invalid entries

## Recommendations

1. **Use OpenStreetMap as primary source** for future updates
2. **Regular verification** - Periodically check coordinates against authoritative sources
3. **Documentation** - Keep track of coordinate sources and update dates
4. **Validation** - Always validate coordinates are within expected geographic bounds

## Contact

For questions about coordinate accuracy or to report issues, please refer to the project repository.

