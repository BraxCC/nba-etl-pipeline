import pandas as pd
import pytest
from transform.metrics import add_advanced_metrics

def make_test_df(pts, fga, fta, player_id=1):
    return pd.DataFrame([{
        'player_id': player_id, 'player_name': 'Test Player',
        'game_date': '2024-01-01', 'game_id': 1,
        'pts': float(pts), 'reb': 5.0, 'ast': 3.0,
        'fga': float(fga), 'fta': float(fta)
    }])

def test_ts_pct_normal_game():
    df = make_test_df(pts=20, fga=15, fta=4)
    result = add_advanced_metrics(df)
    ts = result['true_shooting_pct'].iloc[0]
    assert 0 < ts < 1, "TS% should be between 0 and 1"

def test_ts_pct_zero_attempts():
    # Edge case: player with DNP (no attempts)
    df = make_test_df(pts=0, fga=0, fta=0)
    result = add_advanced_metrics(df)
    assert result['true_shooting_pct'].iloc[0] == 0.0, \
        "Should return 0 for zero attempts, not crash"

def test_rolling_columns_created():
    df = make_test_df(pts=25, fga=18, fta=6)
    result = add_advanced_metrics(df)
    for col in ['rolling_10_pts', 'rolling_10_reb', 'rolling_10_ast']:
        assert col in result.columns, f"Missing column: {col}"

# Run all tests with: pytest tests/ -v