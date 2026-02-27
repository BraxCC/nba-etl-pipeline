from nba_api.stats.endpoints import LeagueStandingsV3
import pandas as pd
import time, os

def extract_standings(season: str = '2024-25') -> pd.DataFrame:
    """Extract current team standings for the season."""
    print(f"[EXTRACT] Pulling team standings for {season}...")

    standings = LeagueStandingsV3(season=season)
    time.sleep(0.6)
    df = standings.get_data_frames()[0]

    print(f"[EXTRACT] ✅ Got standings for {len(df)} teams.")
    return df

if __name__ == '__main__':
    df = extract_standings()
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/raw_standings.csv', index=False)
    print("[EXTRACT] 💾 Saved checkpoint to data/raw/raw_standings.csv")