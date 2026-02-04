# Maps Directory

This directory contains generated interactive HTML maps.

## Regenerating Maps

To regenerate the maps after cloning the repository, run:

```bash
# Process TPU data (if needed)
python scripts/data_processing/process_tpu_data.py

# Run spatial analysis (if needed)
python scripts/analysis/spatial_analysis.py

# Generate the interactive map
python scripts/visualization/create_tpu_mtr_map.py
```

The map will be saved to `tpu_mtr_map.html` in this directory.

## Note

Large HTML map files (>100MB) are excluded from git due to GitHub file size limits. They can be regenerated using the scripts above.

## File Sizes

- `tpu_mtr_map.html`: ~200MB (contains complete TPU boundaries for all years)
- `interactive_dashboard.html`: ~130MB

These files are generated locally and can be opened directly in a web browser.

