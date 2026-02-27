import pandas as pd
import numpy as np

def add_advanced_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Add True Shooting % and rolling averages to game log data."""

    # --- True Shooting % ---
    # Formula: TS% = PTS / (2 * (FGA + 0.44 * FTA))
    # np.where handles the edge case where a player didn't attempt anything
    denominator = 2 * (df['fga'] + 0.44 * df['fta'])
    df['true_shooting_pct'] = np.where(
        denominator > 0,
        (df['pts'] / denominator).round(3),
        0.0
    )

    # --- Rolling 10-game averages per player ---
    # IMPORTANT: Sort by player + date FIRST so rolling window is chronological
    df = df.sort_values(['player_id', 'game_date']).reset_index(drop=True)

    for stat in ['pts', 'reb', 'ast']:
        col_name = f'rolling_10_{stat}'
        df[col_name] = (
            df.groupby('player_id')[stat]
              .transform(lambda x: x.rolling(10, min_periods=1).mean())
              .round(2)
        )

    print("[TRANSFORM] ✅ Advanced metrics added: TS%, rolling_10_pts/reb/ast")
    return df

def build_player_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate game logs into a season summary per player.
    This becomes its own table in Postgres.
    """
    summary = df.groupby(['player_id', 'player_name']).agg(
        games_played  = ('game_id',           'count'),
        avg_pts       = ('pts',               'mean'),
        avg_reb       = ('reb',               'mean'),
        avg_ast       = ('ast',               'mean'),
        avg_ts_pct    = ('true_shooting_pct', 'mean'),
        total_pts     = ('pts',               'sum')
    ).round(2).reset_index()

    print(f"[TRANSFORM] ✅ Built summary for {len(summary)} players.")
    return summary