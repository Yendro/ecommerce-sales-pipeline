import pandas as pd
from sqlalchemy import create_engine

def load_data_to_sqlite(df: pd.DataFrame):
    engine = create_engine("sqlite:///data/amazon_dw.db")
    df.to_sql("ventas", engine, if_exists="replace", index=False)
    print("\nData loaded into the local database: data/amazon_dw.db")

    with engine.connect() as conn:
        sample = pd.read_sql("SELECT * FROM ventas LIMIT 5;", conn)
        print("\n=== DEBUG: PREVIEW OF THE SALES TABLE ===")
        print(sample)