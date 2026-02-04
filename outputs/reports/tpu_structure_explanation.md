# TPU Structure Explanation: Why TPUs Are Split

## The Question

You noticed that some TPUs appear to be "split" into smaller pieces, but they all share the same TPU_ID. You asked: **"How did you decide to split them up?"**

## The Answer: I Didn't Split Them

**The TPU boundaries come pre-split from the Hong Kong Planning Department data.** The processing script preserves this structure - it doesn't merge or split anything.

## Hong Kong Planning Unit Hierarchy

The data follows a hierarchical structure:

```
PPU (Planning Primary Unit)
  └── SPU (Small Planning Unit)
      └── TPU (Tertiary Planning Unit) ← We use this level
          └── SB_VC (Small Base/Voting Constituency) ← Most granular
```

### Real Example: TPU 221

- **PPU**: 2
- **SPU**: 22  
- **TPU**: 221
- **SB_VCs**: 91 separate boundaries

All 91 SB_VC boundaries have `TPU_ID = '221'` because they all belong to TPU 221, but each is a separate voting/statistical area.

## Why Are They Split?

Each TPU is subdivided into **SB_VCs (Small Base/Voting Constituencies)** - the smallest statistical and voting units in Hong Kong's planning system. This is how the data is structured by the source (Hong Kong Planning Department via Esri China Open Data Portal).

### Statistics (2016 Data)

- **Total features**: 5,034 (these are SB_VC boundaries)
- **Unique TPUs**: 291
- **Average SB_VCs per TPU**: 17.3
- **Range**: Some TPUs have just 1 SB_VC, others have 91+ SB_VCs

## What the Processing Script Does

Looking at `scripts/data_processing/process_tpu_data.py`:

1. **Loads the raw data** - which already has multiple features per TPU
2. **Extracts TPU_ID** - from the 'TPU' column (line 72)
3. **Preserves all boundaries** - doesn't merge SB_VCs together
4. **Assigns TPU_ID** - all SB_VCs in the same TPU get the same TPU_ID

```python
# From process_tpu_data.py, line 72
standardized['TPU_ID'] = standardized[tpu_id_col].astype(str)
```

**The script does NOT merge geometries** - it keeps all individual SB_VC boundaries.

## Why Keep Them Split? (Design Decision)

The processing script *could* merge all SB_VCs with the same TPU_ID into a single polygon, but it doesn't. This is intentional because:

### Advantages of Keeping SB_VC Granularity:

1. **More Precise Spatial Analysis**
   - Can calculate MTR proximity for each small area
   - More accurate distance measurements
   - Better identification of which parts of a TPU are close to MTR stations

2. **Preserves Original Data Structure**
   - Maintains the hierarchical planning system
   - Allows analysis at SB_VC level if needed
   - Matches how Hong Kong government structures the data

3. **Better Visualization**
   - Can see internal structure of TPUs
   - More detailed map representation
   - Shows voting/statistical boundaries

### If We Merged Them:

- Would lose granularity
- Less precise MTR proximity calculations
- Wouldn't match the original data structure
- Would have only 291 features instead of 5,034

## Example: TPU 221

TPU 221 consists of **91 separate SB_VC boundaries**:
- Each has unique SB_VC number (1, 2, 3, ..., 91)
- All have `TPU_ID = '221'`
- All belong to `SPU = 22` and `PPU = 2`
- Each is a separate voting/statistical area

When you see TPU 221 on the map, you're seeing all 91 of these small areas together, each with its own boundary.

## Summary

- **I didn't decide to split them** - the data comes that way
- **The processing preserves the structure** - doesn't merge or split
- **All SB_VCs in a TPU share the same TPU_ID** - because they belong to the same TPU
- **This is beneficial** - allows more precise spatial analysis

The "split" is actually the natural hierarchical structure of Hong Kong's planning system, where each TPU is composed of multiple smaller SB_VC units.

