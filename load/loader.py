from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd, os

load_dotenv()

def get_engine():
    return create_engine(
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

def load_to_postgres(
    df: pd.DataFrame,
    table: str,
    schema: str = 'staging',
    if_exists: str = 'replace'
):
    """
    Load a DataFrame into a PostgreSQL table.
    if_exists options: 'replace' (drop+recreate), 'append', 'fail'
    """
    engine = get_engine()
    print(f"[LOAD] Writing {len(df):,} rows → {schema}.{table}...")

    df.to_sql(
        name=table,
        con=engine,
        schema=schema,
        if_exists=if_exists,
        index=False,
        method='multi',   # Batch inserts — much faster
        chunksize=1000
    )
    print(f"[LOAD] ✅ Done. Table: {schema}.{table}")