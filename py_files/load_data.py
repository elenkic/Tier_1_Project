import pandas as pd
from db import get_engine


def load_tables():
    """
    Load database tables into pandas DataFrames using SQLAlchemy.
    """
    engine = get_engine()

    try:
        df_results = pd.read_sql("SELECT * FROM results", engine)
        df_samples = pd.read_sql("SELECT * FROM samples", engine)
        df_guidelines = pd.read_sql("SELECT * FROM guidelines", engine)

    finally:
        # cleaning up the engine connections
        engine.dispose()

    return df_results, df_samples, df_guidelines