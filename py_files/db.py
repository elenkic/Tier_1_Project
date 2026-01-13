#Database connection

import os
from sqlalchemy import create_engine

def get_engine():
    engine_url = "postgresql+psycopg2://postgres:112123@localhost:5432/tier_1"
    engine = create_engine(engine_url)
    return engine