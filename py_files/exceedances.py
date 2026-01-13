import pandas as pd

def calculate_exceedances(df_results, df_samples, df_guidelines):
    # Merge land use from samples
    df = df_results.merge(
        df_samples[['sample_id', 'sample_name', 'land_use']],
        on='sample_id',
        how='left'
    )

    # Standardize strings for matching
    for col in ['parameter', 'soil_type', 'land_use']:
        df[col] = df[col].str.strip().str.lower()
        df_guidelines[col] = df_guidelines[col].str.strip().str.lower()

    # Merge with guidelines
    df = df.merge(
        df_guidelines,
        on=['parameter', 'soil_type', 'land_use'],
        how='left'
    )

    # Parse guideline values
    def parse_guideline_value(value):
        if pd.isna(value):
            return None, None
        value = str(value).strip()
        if '-' in value:
            try:
                min_val, max_val = value.split('-')
                return float(min_val), float(max_val)
            except:
                return None, None
        try:
            return None, float(value)
        except:
            return None, None

    df[['guideline_min', 'guideline_max']] = (
        df['guideline_value'].apply(parse_guideline_value).apply(pd.Series)
    )

    # Exceedance flag
    df['exceeds'] = False

    # Range-based for pH
    ph_mask = df['parameter'] == 'pH (in 0.01m cacl2)'
    df.loc[ph_mask, 'exceeds'] = (
        (df.loc[ph_mask, 'concentration_value'] < df.loc[ph_mask, 'guideline_min']) |
        (df.loc[ph_mask, 'concentration_value'] > df.loc[ph_mask, 'guideline_max'])
    )

    # Max-only for everything else
    df.loc[~ph_mask, 'exceeds'] = df.loc[~ph_mask, 'concentration_value'] > df.loc[~ph_mask, 'guideline_max']

    # Keep only relevant info for exceeded samples
    df_exceeded = df[df['exceeds']].copy()
    df_exceeded = df_exceeded[[
        'sample_id', 'sample_name', 'parameter', 'soil_type', 'land_use',
        'concentration_value', 'guideline_value', 'exceeds'
    ]]

    return df_exceeded



