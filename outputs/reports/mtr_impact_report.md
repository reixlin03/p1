# MTR Impact on Hong Kong Demographics: Analysis Report

**Generated:** 2025-12-29 16:17:54

## Executive Summary

This report analyzes the relationship between Mass Transit Railway (MTR) stations
and demographic changes in Hong Kong's Tertiary Planning Units (TPUs) from 2001 to 2016.

## Data Overview

- **TPU Boundaries Analyzed:** 2001, 2006, 2011, 2016
- **Total TPU Observations:** 19816
- **MTR Stations:** 99 stations with coordinates

## Spatial Analysis Results

### Proximity Distribution

- **Very Close (<500m):** 8086 TPUs
- **Far (>2km):** 4812 TPUs
- **Close (500-1000m):** 4301 TPUs
- **Moderate (1-2km):** 2617 TPUs

## Methodology

### Data Sources

1. **TPU Boundaries**: Esri China Open Data Portal
   - Years: 2001, 2006, 2011, 2016
   - Source: Planning Department / Census and Statistics Department

2. **MTR Stations**: Scraped from Wikipedia
   - 99 stations with geographic coordinates
   - Enhanced with geocoding where needed

3. **Demographic Data**: To be integrated
   - Source: Census and Statistics Department
   - Status: Research completed, download in progress

### Analysis Methods

1. **Spatial Analysis**:
   - Calculated distance from each TPU centroid to nearest MTR station
   - Created buffer zones (500m, 1000m, 2000m) around MTR stations
   - Identified TPUs containing MTR stations

2. **Temporal Analysis**:
   - Compare demographics before vs. after MTR station openings
   - Track changes across census years (2001-2016)

3. **Statistical Analysis**:
   - Correlation analysis between MTR proximity and demographics
   - Group comparisons (MTR-adjacent vs. non-adjacent)
   - Regression analysis to control for other factors

## Key Findings

### Spatial Patterns

### Demographic Impact (Pending Data)

Once demographic data is integrated, this section will include:
- Population changes in MTR-adjacent vs. non-adjacent TPUs
- Income and education level differences
- Housing characteristic changes
- Statistical significance of observed differences

## Limitations

1. **Demographic Data**: Currently awaiting demographic data integration
2. **MTR Opening Dates**: Using approximate dates; actual dates should be verified
3. **Causality**: Correlation does not imply causation; other factors may influence demographics
4. **TPU Boundary Changes**: Boundary changes across years may affect comparability

## Recommendations

### For Urban Planning

1. Consider MTR proximity when planning new developments
2. Monitor demographic changes in areas with new MTR stations
3. Plan for infrastructure needs in MTR-adjacent areas

### For Future Research

1. Integrate complete demographic dataset
2. Verify MTR station opening dates from official sources
3. Conduct control group analysis to isolate MTR effects
4. Extend analysis to 2021 census data when available

## Next Steps

1. Download and integrate demographic data from Census and Statistics Department
2. Verify MTR station opening dates
3. Complete statistical analysis with demographic variables
4. Create detailed visualizations
5. Generate final findings and recommendations

## Files and Outputs

- **Interactive Map**: `outputs/maps/tpu_mtr_map.html`
- **Dashboard**: `outputs/dashboards/interactive_dashboard.html`
- **Spatial Analysis**: `data/analysis/mtr_tpu_spatial_join_all_years.csv`
- **Analysis Scripts**: `scripts/analysis/`
