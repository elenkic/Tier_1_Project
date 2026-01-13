from load_data import load_tables
from exceedances import calculate_exceedances
import pandas as pd

def main():
    # Load data
    df_results, df_samples, df_guidelines = load_tables()


    # df_results, df_samples, df_guidelines are already in memory

    # Calculate fails
    df_fails = calculate_exceedances(df_results, df_samples, df_guidelines)
    df_fails.to_csv("exceedances_raw.csv", index=False)

    # Summary tables
    df_fails.groupby('parameter').size().reset_index(name='fail_count').to_csv("fails_per_parameter.csv", index=False)
    df_fails.groupby('sample_name').size().reset_index(name='fail_count').to_csv("fails_per_sample.csv", index=False)
    df_fails.groupby('soil_type').size().reset_index(name='fail_count').to_csv("fails_per_soil.csv", index=False)
    df_fails.groupby('land_use').size().reset_index(name='fail_count').to_csv("fails_per_landuse.csv", index=False)

    # Pivot table: parameter vs soil type
    pivot_table = pd.pivot_table(
        df_fails,
        values='sample_id',
        index='parameter',
        columns='soil_type',
        aggfunc='count',
        fill_value=0
    )
    pivot_table.to_csv("pivot_parameter_vs_soil.csv")

    print("All fail tables saved as CSVs.")

if __name__ == "__main__":
    main()
