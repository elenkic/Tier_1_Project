import pandas as pd

def generate_exceedance_table(input_csv: str, output_csv: str):
    """
    Reads a CSV with sample results, calculates exceedance ratio and type,
    rounds values, and saves a new CSV with derived columns.

    Args:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path to save the output CSV file.
    """
    # Load the CSV
    df = pd.read_csv(input_csv)

    # Ensure numeric columns
    df['concentration_value'] = pd.to_numeric(df['concentration_value'], errors='coerce')
    df['guideline_value'] = pd.to_numeric(df['guideline_value'], errors='coerce')

    # Calculate exceedance ratio
    df['exceedance_ratio'] = df['concentration_value'] / df['guideline_value']

    # Round exceedance ratio to 2 decimals for readability
    df['exceedance_ratio'] = df['exceedance_ratio'].round(2)

    # Determine exceedance type
    def get_exceedance_type(row):
        if row['concentration_value'] > row['guideline_value']:
            return 'above_max'
        elif row['concentration_value'] < row['guideline_value']:
            return 'below_min'
        else:
            return 'within_range'

    df['exceedance_type'] = df.apply(get_exceedance_type, axis=1)

    # Select desired columns
    final_df = df[[
        'sample_id', 'sample_name', 'parameter', 'soil_type', 'land_use',
        'concentration_value', 'guideline_value', 'exceedance_ratio', 'exceedance_type'
    ]]

    # Optional: remove exact duplicate rows
    final_df = final_df.drop_duplicates()

    # Save output CSV
    final_df.to_csv(output_csv, index=False)
    print(f"Exceedance table created (rounded): {output_csv}")
