import pandas as pd
from datetime import datetime

def clean_player_logs(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize and clean raw player game log data."""
    print(f"[TRANSFORM] Cleaning {len(df):,} rows...")

    # Step 1: Normalize column names → snake_case
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Step 2: Convert game_date string to datetime
    df['game_date'] = pd.to_datetime(df['game_date'])

    # Step 3: Drop rows missing core stats
    before = len(df)
    df = df.dropna(subset=['pts', 'reb', 'ast', 'fga', 'fta'])
    print(f"[TRANSFORM] Dropped {before - len(df)} rows with missing stats.")

    # Step 4: Cast stat columns to float
    num_cols = ['pts', 'reb', 'ast', 'stl', 'blk', 'fga', 'fta',
                'fg3a', 'fg3m', 'min']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Step 5: Add pipeline metadata timestamp
    df['load_date'] = datetime.utcnow()

    print(f"[TRANSFORM] ✅ Clean data: {len(df):,} rows remaining.")
    return df