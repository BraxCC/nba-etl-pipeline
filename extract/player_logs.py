from nba_api.stats.endpoints import PlayerGameLogs
import pandas as pd
import time, os

def extract_player_logs(season: str = '2024-25') -> pd.DataFrame:
    """
    Extract all player game logs for a given NBA season.
    Returns a raw DataFrame with all stats columns.
    """
    print(f"[EXTRACT] Pulling player logs for {season}...")

    try:
        logs = PlayerGameLogs(season_nullable=season)
        time.sleep(0.6)  # Be polite to the API

        df = logs.get_data_frames()[0]
        print(f"[EXTRACT] ✅ Got {len(df):,} rows, {len(df.columns)} columns.")
        return df

    except Exception as e:
        print(f"[EXTRACT] ❌ Failed: {e}")
        raise

if __name__ == '__main__':
    df = extract_player_logs()
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/raw_player_logs.csv', index=False)
    print("[EXTRACT] 💾 Saved checkpoint to data/raw/raw_player_logs.csv")

