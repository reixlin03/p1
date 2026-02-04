# Summary: TPUs with Colored MTR Stations

**Date:** 2025-12-29  
**Excluded Stations:** Quarry Bay, North Point

## Overview

This report identifies TPU IDs that contain MTR stations that are colored on the map (Purple, Yellow, or Blue), excluding Quarry Bay and North Point stations.

### Colored Station Categories

- **Purple (Tseung Kwan O Line):** Po Lam, Hang Hau, LOHAS Park, Tseung Kwan O, Tiu Keng Leng, Yau Tong
- **Yellow (West Rail):** Tuen Mun, Siu Hong, Tin Shui Wai, Long Ping, Yuen Long, Kam Sheung Road, Tsuen Wan West, Mei Foo, Nam Cheong
- **Blue (Ma On Shan Line):** Wu Kai Sha, Ma On Shan, Heng On, Tai Shui Hang, Shek Mun, City One, Sha Tin Wai, Che Kung Temple, Tai Wai

**Total Colored Stations (excluding Quarry Bay and North Point):** 24 stations

## Summary Table

| TPU_ID | MTR Stations | Years Available |
|--------|-------------|----------------|
| 255 | Nam Cheong | 2006, 2011, 2016 |
| 260 | Mei Foo | 2001, 2006, 2011, 2016 |
| 265 | Nam Cheong | 2001 |
| 298 | Yau Tong | 2001, 2006, 2011, 2016 |
| 324 | Tsuen Wan West | 2006, 2011, 2016 |
| 423 | Siu Hong | 2001, 2006, 2011, 2016 |
| 424 | Tuen Mun | 2001, 2006, 2011, 2016 |
| 510 | Tin Shui Wai | 2001 |
| 515 | Tin Shui Wai | 2006, 2011, 2016 |
| 524 | Long Ping, Yuen Long | 2001, 2006, 2011, 2016 |
| 531 | Kam Sheung Road | 2001, 2006, 2011, 2016 |
| 755 | Sha Tin Wai | 2001, 2006, 2011, 2016 |
| 756 | City One, Shek Mun | 2001, 2006, 2011, 2016 |
| 757 | Heng On, Ma On Shan, Tai Shui Hang, Wu Kai Sha | 2001, 2006, 2011, 2016 |
| 759 | Che Kung Temple, Tai Wai | 2001, 2006, 2011, 2016 |
| 833 | Tiu Keng Leng | 2001, 2006, 2011, 2016 |
| 836 | Po Lam | 2001, 2006, 2011, 2016 |
| 837 | Hang Hau | 2001, 2006, 2011, 2016 |
| 838 | Tseung Kwan O | 2001, 2006, 2011, 2016 |
| 839 | LOHAS Park | 2001, 2006, 2011, 2016 |

## Statistics

- **Total Unique TPU IDs with Colored Stations:** 20
- **TPUs with Multiple Stations:** 3
  - TPU 524: Long Ping, Yuen Long
  - TPU 756: City One, Shek Mun
  - TPU 757: Heng On, Ma On Shan, Tai Shui Hang, Wu Kai Sha
  - TPU 759: Che Kung Temple, Tai Wai

## Breakdown by Line

### Tseung Kwan O Line (Purple)
- TPU 298: Yau Tong
- TPU 833: Tiu Keng Leng
- TPU 836: Po Lam
- TPU 837: Hang Hau
- TPU 838: Tseung Kwan O
- TPU 839: LOHAS Park

### West Rail (Yellow)
- TPU 255: Nam Cheong (2006-2016)
- TPU 260: Mei Foo
- TPU 265: Nam Cheong (2001)
- TPU 324: Tsuen Wan West
- TPU 423: Siu Hong
- TPU 424: Tuen Mun
- TPU 510: Tin Shui Wai (2001)
- TPU 515: Tin Shui Wai (2006-2016)
- TPU 524: Long Ping, Yuen Long
- TPU 531: Kam Sheung Road

### Ma On Shan Line (Blue)
- TPU 755: Sha Tin Wai
- TPU 756: City One, Shek Mun
- TPU 757: Heng On, Ma On Shan, Tai Shui Hang, Wu Kai Sha
- TPU 759: Che Kung Temple, Tai Wai

## Notes

- Some TPUs appear in multiple years due to boundary changes between census years
- TPU 255 and 265 both contain Nam Cheong station but in different years (boundary change)
- TPU 510 and 515 both contain Tin Shui Wai station but in different years (boundary change)
- TPU 757 contains the most stations (4 stations: Heng On, Ma On Shan, Tai Shui Hang, Wu Kai Sha)

## Files Generated

- `tpu_colored_stations_summary.csv` - Summary table (TPU_ID, MTR_Stations, Years)
- `tpu_colored_stations_detailed.csv` - Detailed data with year-by-year breakdown

