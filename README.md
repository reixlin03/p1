# MTR Impact on Hong Kong Demographics

🌐 **Live Site:** [View on GitHub Pages](https://reixlin03.github.io/p1/)

## Project Overview

This project analyzes how Mass Transit Railway (MTR) stations influence demographic changes in Hong Kong's Tertiary Planning Units (TPUs) across census years (2001-2016). The study examines population, age, income, education, and housing characteristics in relation to MTR proximity and station openings.

## Research Questions

1. **Proximity Effects**: Do TPUs closer to MTR stations show different demographic characteristics?
2. **Temporal Effects**: How do demographics change after MTR station openings?
3. **Cumulative Effects**: Do TPUs with longer MTR access show greater changes?
4. **Spatial Patterns**: Are there spatial clusters of demographic change?
5. **Line-Specific Effects**: Do different MTR lines have different impacts?
6. **Control Analysis**: Are changes due to MTR or other factors?

## Project Structure

```
Xier Project/
├── data/
│   ├── raw/              # Original data files
│   ├── processed/        # Cleaned and standardized data
│   └── analysis/         # Analysis-ready datasets
├── scripts/
│   ├── data_collection/  # Data downloading/scraping
│   ├── data_processing/  # Data cleaning and transformation
│   ├── analysis/         # Statistical and spatial analysis
│   └── visualization/    # Map and chart creation
├── outputs/
│   ├── maps/             # Interactive and static maps
│   ├── reports/          # Analysis reports
│   ├── figures/          # Charts and graphs
│   └── dashboards/       # Interactive dashboards
└── notebooks/            # Jupyter notebooks for exploration
```

## Current Data Assets

### MTR Station Data
- **Source**: Scraped from Wikipedia
- **Stations**: 99 stations with coordinates
- **Location**: `data/raw/mtr/mtr_stations.xlsx`
- **Fields**: Station name (English/Chinese), coordinates, lines, station codes

### TPU Boundary Data
- **Source**: Esri China Open Data Portal / Hong Kong Planning Department
- **Years Available**: 2001, 2006, 2011, 2016
- **TPU Counts**: 
  - 2001: 4,815 TPUs
  - 2006: 4,976 TPUs
  - 2011: 4,992 TPUs
  - 2016: 5,033 TPUs
- **Location**: `data/raw/tpu/` (raw), `data/processed/tpu/` (processed)

### Interactive Map
- **File**: `outputs/maps/tpu_mtr_map.html`
- **Features**: 
  - Toggleable TPU boundaries by year
  - MTR station markers with popups
  - Multiple base map options
  - Fullscreen and measurement tools

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or download this repository

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Required Packages

- `geopandas` - Geospatial data processing
- `pandas` - Data manipulation
- `shapely` - Geometric operations
- `folium` - Interactive mapping
- `requests` - HTTP requests for data downloading
- `beautifulsoup4` - Web scraping
- `openpyxl` - Excel file handling
- `lxml` - XML/HTML parsing

## Usage

### Data Collection

1. **Download TPU boundaries**:
```bash
python scripts/data_collection/download_tpu_data.py
```

2. **Scrape MTR stations** (if needed):
```bash
python scripts/data_collection/scrape_mtr_stations.py
```

### Data Processing

1. **Process TPU boundaries**:
```bash
python scripts/data_processing/process_tpu_data.py
```

### Visualization

1. **Create interactive map**:
```bash
python scripts/visualization/create_tpu_mtr_map.py
```

The map will be saved to `outputs/maps/tpu_mtr_map.html`

## Data Sources

### TPU Boundaries
- **2001, 2006, 2011, 2016**: Esri China Open Data Portal
  - Service: `https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/`
  - Datasets: `TPU_SB_VC_{YEAR}_PlanD_gdb`

### MTR Stations
- Wikipedia: List of MTR stations
- Enhanced with coordinates from individual station pages and geocoding

### Demographic Data (To Be Added)
- Hong Kong Census and Statistics Department
- Planning Department statistics
- TPU-level census data for 2001, 2006, 2011, 2016

## Analysis Workflow

1. **Data Collection**: Download/scrape all required data
2. **Data Processing**: Clean, standardize, and integrate datasets
3. **Spatial Analysis**: Calculate MTR proximity metrics for each TPU
4. **Temporal Analysis**: Compare demographics before/after MTR openings
5. **Statistical Analysis**: Correlations, regressions, significance tests
6. **Visualization**: Create maps, charts, and dashboards
7. **Reporting**: Generate comprehensive analysis reports

## Outputs

- **Maps**: Interactive HTML maps showing TPU boundaries, MTR stations, and demographic patterns
- **Reports**: Markdown reports with analysis findings
- **Charts**: Statistical visualizations (scatter plots, time series, box plots)
- **Dashboards**: Interactive dashboards for exploring results
- **Datasets**: Analysis-ready CSV files with integrated data

## Future Work

- [ ] Download and integrate demographic data
- [ ] Perform spatial proximity analysis
- [ ] Implement before/after temporal analysis
- [ ] Statistical correlation and regression analysis
- [ ] Create demographic heatmaps
- [ ] Build comprehensive interactive dashboard
- [ ] Generate final analysis report

## License

This project is for research purposes. Data sources are credited to their respective providers.

## Contact

For questions or contributions, please refer to the project repository.

## 🔗 Links

- **Live Site**: [https://reixlin03.github.io/p1/](https://reixlin03.github.io/p1/)
- **Repository**: [https://github.com/reixlin03/p1](https://github.com/reixlin03/p1)
- **Interactive Map**: [TPU & MTR Map](https://reixlin03.github.io/p1/outputs/maps/tpu_mtr_map.html)
- **Dashboard**: [Analysis Dashboard](https://reixlin03.github.io/p1/outputs/dashboards/interactive_dashboard.html)

