from nba_api.stats.endpoints import PlayerGameLogs
import time

# Pull game logs for the 2024-25 season
logs = PlayerGameLogs(season_nullable='2024-25')
time.sleep(0.6)  # Always sleep after NBA API calls!

df = logs.get_data_frames()[0]

print("=== Available Columns ===")
print(df.columns.tolist())

print("\n=== First 3 rows ===")
print(df.head(3).to_string())

print(f"\n=== Shape: {df.shape} ===")
print(f"That's {df.shape[0]} game log entries for the season")