import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm
import requests

def get_nfl_data(seasons=range(2020, 2024)):
    """
    Fetch NFL play-by-play data from nflfastR
    """
    base_url = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{}.parquet"
    all_data = []
    
    for season in tqdm(seasons, desc="Fetching seasons"):
        try:
            url = base_url.format(season)
            df = pd.read_parquet(url)
            df['season'] = season
            all_data.append(df)
            print(f"Successfully loaded {season} season data")
        except Exception as e:
            print(f"Error loading {season} season: {e}")
    
    return pd.concat(all_data, ignore_index=True)

def create_game_level_data(play_by_play_df):
    """
    Aggregate play-by-play data to game level
    """
    # First, calculate game-level passing and rushing yards
    game_stats = play_by_play_df.groupby(['game_id', 'posteam']).agg({
        'passing_yards': 'sum',
        'rushing_yards': 'sum'
    }).reset_index()
    
    # Pivot the stats to get home and away values
    game_stats_pivot = game_stats.pivot(
        index='game_id',
        columns='posteam',
        values=['passing_yards', 'rushing_yards']
    ).reset_index()
    
    # Flatten column names
    game_stats_pivot.columns = ['game_id'] + [f'{stat}_{team}' 
        for stat, team in game_stats_pivot.columns[1:]]
    
    # Get basic game information
    game_data = play_by_play_df.groupby('game_id').agg({
        'season': 'first',
        'week': 'first',
        'home_team': 'first',
        'away_team': 'first',
        'home_score': 'max',
        'away_score': 'max',
        'weather': 'first',
        'temp': 'first',
        'wind': 'first'
    }).reset_index()
    
    # Merge stats with game data
    game_data = game_data.merge(game_stats_pivot, on='game_id', how='left')
    
    # Fill missing values
    numeric_columns = game_data.select_dtypes(include=[np.number]).columns
    game_data[numeric_columns] = game_data[numeric_columns].fillna(0)
    
    return game_data

def prepare_features(game_data):
    """
    Create features for modeling
    """
    df = game_data.copy()
    
    # Create basic features
    df['total_points'] = df['home_score'] + df['away_score']
    df['point_differential'] = df['home_score'] - df['away_score']
    df['home_team_won'] = df['point_differential'] > 0
    
    # Create team performance features
    for team in df['home_team'].unique():
        # Get all games for this team
        team_games = pd.concat([
            df[df['home_team'] == team].assign(is_home=1),
            df[df['away_team'] == team].assign(is_home=0)
        ]).sort_values(['season', 'week'])
        
        # Calculate points scored and allowed
        team_games['points_scored'] = np.where(
            team_games['is_home'],
            team_games['home_score'],
            team_games['away_score']
        )
        
        team_games['points_allowed'] = np.where(
            team_games['is_home'],
            team_games['away_score'],
            team_games['home_score']
        )
        
        # Calculate rolling averages
        team_games[f'{team}_rolling_pts_scored'] = team_games['points_scored'].rolling(3, min_periods=1).mean()
        team_games[f'{team}_rolling_pts_allowed'] = team_games['points_allowed'].rolling(3, min_periods=1).mean()
        
        # Merge back to main dataframe
        df = df.merge(
            team_games[['game_id', f'{team}_rolling_pts_scored', f'{team}_rolling_pts_allowed']],
            on='game_id',
            how='left'
        )
    
    return df

if __name__ == "__main__":
    # Get raw play-by-play data
    print("Fetching NFL data...")
    pbp_data = get_nfl_data()
    
    # Create game-level dataset
    print("Creating game-level dataset...")
    game_data = create_game_level_data(pbp_data)
    
    # Prepare features
    print("Preparing features...")
    final_data = prepare_features(game_data)
    
    # Save to CSV
    final_data.to_csv('nfl_prepared_data.csv', index=False)
    print("Data saved to 'nfl_prepared_data.csv'")
    
    # Display data info
    print("\nDataset information:")
    print(final_data.info())
    print("\nSample of the data:")
    print(final_data.head())
