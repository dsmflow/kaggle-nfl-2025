import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

class NFLDashboard:
    def __init__(self, data):
        self.data = data
        print("Available columns:", self.data.columns)  # Debug print
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("NFL Analysis Dashboard", className="text-center my-4"),
                    dbc.Card([
                        dbc.CardBody([
                            # Team selection
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Home Team"),
                                    dcc.Dropdown(
                                        id='home-team-dropdown',
                                        options=[{'label': team, 'value': team} 
                                                for team in sorted(self.data['home_team'].unique())],
                                        value=sorted(self.data['home_team'].unique())[0]
                                    )
                                ]),
                                dbc.Col([
                                    html.Label("Away Team"),
                                    dcc.Dropdown(
                                        id='away-team-dropdown',
                                        options=[{'label': team, 'value': team} 
                                                for team in sorted(self.data['away_team'].unique())],
                                        value=sorted(self.data['away_team'].unique())[0]
                                    )
                                ])
                            ], className="mb-4"),
                            
                            # Visualization type selection
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Visualization Type"),
                                    dcc.Dropdown(
                                        id='viz-type-dropdown',
                                        options=[
                                            {'label': 'Team Performance', 'value': 'team_comparison'},
                                            {'label': 'Season Trends', 'value': 'historical_trends'},
                                            {'label': 'Weather Impact', 'value': 'weather_analysis'}
                                        ],
                                        value='team_comparison'
                                    )
                                ])
                            ])
                        ])
                    ], className="mb-4")
                ])
            ]),
            
            # Main visualization area
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='main-visualization', style={'height': '800px'})
                ])
            ])
        ], fluid=True)
    
    def setup_callbacks(self):
        @self.app.callback(
            Output('main-visualization', 'figure'),
            [Input('home-team-dropdown', 'value'),
             Input('away-team-dropdown', 'value'),
             Input('viz-type-dropdown', 'value')]
        )
        def update_visualization(home_team, away_team, viz_type):
            if viz_type == 'team_comparison':
                return self.create_team_comparison(home_team, away_team)
            elif viz_type == 'historical_trends':
                return self.create_historical_trends(home_team, away_team)
            else:
                return self.create_weather_analysis(home_team, away_team)
    
    def create_team_comparison(self, home_team, away_team):
        """Create team comparison visualization"""
        home_data = self.data[self.data['home_team'] == home_team]
        away_data = self.data[self.data['away_team'] == away_team]
        
        fig = make_subplots(rows=2, cols=2,
                           subplot_titles=('Scoring Trends', 'Point Differential',
                                         'Offensive Yards', 'Season Performance'))
        
        # Scoring Trends
        fig.add_trace(
            go.Scatter(x=home_data['week'], y=home_data['home_score'],
                      name=f'{home_team} Score', mode='lines+markers'),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=away_data['week'], y=away_data['away_score'],
                      name=f'{away_team} Score', mode='lines+markers'),
            row=1, col=1
        )
        
        # Point Differential
        fig.add_trace(
            go.Bar(x=[home_team, away_team],
                  y=[home_data['point_differential'].mean(),
                     -away_data['point_differential'].mean()],  # Negative for away perspective
                  name='Avg Point Differential'),
            row=1, col=2
        )
        
        # Offensive Yards - Updated to match the actual column names
        try:
            home_passing = home_data[f'passing_yards_{home_team}'].mean()
            away_passing = away_data[f'passing_yards_{away_team}'].mean()
            home_rushing = home_data[f'rushing_yards_{home_team}'].mean()
            away_rushing = away_data[f'rushing_yards_{away_team}'].mean()
        except KeyError:
            # Fallback if columns don't exist
            print(f"Warning: Some yards columns not found. Available columns: {home_data.columns}")
            home_passing = home_rushing = away_passing = away_rushing = 0
        
        fig.add_trace(
            go.Bar(x=[f'{home_team} Pass', f'{home_team} Rush', 
                     f'{away_team} Pass', f'{away_team} Rush'],
                  y=[home_passing, home_rushing, away_passing, away_rushing],
                  name='Yards per Game'),
            row=2, col=1
        )
        
        # Season Performance
        fig.add_trace(
            go.Bar(x=[home_team, away_team],
                  y=[home_data[f'{home_team}_rolling_pts_scored'].mean() if f'{home_team}_rolling_pts_scored' in home_data.columns else home_data['home_score'].mean(),
                     away_data[f'{away_team}_rolling_pts_scored'].mean() if f'{away_team}_rolling_pts_scored' in away_data.columns else away_data['away_score'].mean()],
                  name='Avg Points per Game'),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=800,
            showlegend=True,
            title_text=f"{home_team} vs {away_team} Comparison",
            title_x=0.5,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Week", row=1, col=1)
        fig.update_yaxes(title_text="Points", row=1, col=1)
        fig.update_yaxes(title_text="Point Differential", row=1, col=2)
        fig.update_yaxes(title_text="Yards", row=2, col=1)
        fig.update_yaxes(title_text="Points", row=2, col=2)
        
        return fig
    
    def create_historical_trends(self, home_team, away_team):
        """Create historical trends visualization"""
        home_games = self.data[self.data['home_team'] == home_team]
        away_games = self.data[self.data['away_team'] == away_team]
        
        fig = make_subplots(rows=2, cols=2,
                           subplot_titles=('Home Team Season Trend', 'Away Team Season Trend',
                                         'Home/Away Performance', 'Scoring Distribution'))
        
        # Home team season trend
        fig.add_trace(
            go.Scatter(x=home_games['week'], 
                      y=home_games['home_score'].rolling(3, min_periods=1).mean(),
                      name=f'{home_team} Scoring Trend',
                      mode='lines+markers'),
            row=1, col=1
        )
        
        # Away team season trend
        fig.add_trace(
            go.Scatter(x=away_games['week'],
                      y=away_games['away_score'].rolling(3, min_periods=1).mean(),
                      name=f'{away_team} Scoring Trend',
                      mode='lines+markers'),
            row=1, col=2
        )
        
        # Home/Away Performance Comparison
        home_performance = [
            home_games['home_score'].mean(),
            away_games['away_score'].mean()
        ]
        
        fig.add_trace(
            go.Bar(x=[home_team, away_team],
                  y=home_performance,
                  name='Average Points'),
            row=2, col=1
        )
        
        # Scoring Distribution
        fig.add_trace(
            go.Box(y=home_games['home_score'], name=home_team),
            row=2, col=2
        )
        fig.add_trace(
            go.Box(y=away_games['away_score'], name=away_team),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=True,
                         title_text=f"{home_team} vs {away_team} Historical Trends",
                         title_x=0.5)
        return fig
    
    def create_weather_analysis(self, home_team, away_team):
        """Create weather analysis visualization"""
        home_games = self.data[self.data['home_team'] == home_team]
        away_games = self.data[self.data['away_team'] == away_team]
        
        fig = make_subplots(rows=2, cols=2,
                           subplot_titles=('Temperature vs. Scoring', 'Wind vs. Scoring',
                                         'Weather Conditions', 'Performance by Temperature'))
        
        # Temperature vs. Scoring
        fig.add_trace(
            go.Scatter(x=home_games['temp'],
                      y=home_games['home_score'],
                      mode='markers',
                      name=f'{home_team} Games'),
            row=1, col=1
        )
        
        # Wind vs. Scoring
        fig.add_trace(
            go.Scatter(x=home_games['wind'],
                      y=home_games['home_score'],
                      mode='markers',
                      name=f'{home_team} Games'),
            row=1, col=2
        )
        
        # Weather Conditions Distribution
        weather_counts = home_games['weather'].value_counts()
        fig.add_trace(
            go.Bar(x=weather_counts.index,
                  y=weather_counts.values,
                  name='Weather Conditions'),
            row=2, col=1
        )
        
        # Performance by Temperature Range
        home_games['temp_range'] = pd.cut(home_games['temp'],
                                        bins=[0, 40, 60, 80, 100],
                                        labels=['Cold', 'Cool', 'Moderate', 'Hot'])
        temp_performance = home_games.groupby('temp_range')['home_score'].mean()
        
        fig.add_trace(
            go.Bar(x=temp_performance.index,
                  y=temp_performance.values,
                  name='Avg Score by Temperature'),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=True,
                         title_text=f"{home_team} Weather Impact Analysis",
                         title_x=0.5)
        
        # Update axes labels
        fig.update_xaxes(title_text="Temperature (°F)", row=1, col=1)
        fig.update_xaxes(title_text="Wind Speed", row=1, col=2)
        fig.update_xaxes(title_text="Weather Condition", row=2, col=1)
        fig.update_xaxes(title_text="Temperature Range", row=2, col=2)
        
        fig.update_yaxes(title_text="Points Scored", row=1, col=1)
        fig.update_yaxes(title_text="Points Scored", row=1, col=2)
        fig.update_yaxes(title_text="Number of Games", row=2, col=1)
        fig.update_yaxes(title_text="Average Points", row=2, col=2)
        
        return fig
    
    def run_server(self, debug=True, port=8050):
        """Run the Dash server"""
        self.app.run_server(debug=debug, port=port)

if __name__ == "__main__":
    # Load data
    data = pd.read_csv('nfl_prepared_data.csv')
    
    # Initialize and run dashboard
    dashboard = NFLDashboard(data)
    dashboard.run_server(debug=True)
