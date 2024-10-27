# kaggle-nfl-2025
An attempt at creating history

# NFL Game Analysis Dashboard

## Overview
This dashboard application provides interactive visualizations of NFL game statistics, designed to analyze historical game data and team performance metrics. Built using Python, Dash, and Plotly, it offers various analytical views including team comparisons, seasonal trends, and weather impact analysis.

## Features
- Interactive team selection for head-to-head comparisons
- Multiple visualization types:
  - Team Performance Comparison
  - Season Trends Analysis
  - Weather Impact Analysis
- Detailed metrics including:
  - Scoring trends
  - Point differentials
  - Offensive yards (passing/rushing)
  - Weather conditions impact
  - Historical performance patterns

## Data Source
The data used in this dashboard is collected from the nflfastR database, which provides play-by-play NFL game data. The data is publicly available through the nflverse-data repository.

## Prerequisites
- Python 3.8+
- Required Python packages:
  ```
  pandas
  dash
  dash-bootstrap-components
  plotly
  numpy
  requests
  tqdm
  ```

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/dsmflow/nfl-analysis-dashboard.git
   cd nfl-analysis-dashboard
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. First, collect and prepare the data:
   ```bash
   python data_collector_updated.py
   ```

2. Run the dashboard:
   ```bash
   python dashboard_app.py
   ```

3. Open your web browser and navigate to:
   ```
   http://localhost:8050
   ```

## Project Structure
```
nfl-analysis-dashboard/
├── data_collector_updated.py  # Data collection and preparation
├── dashboard_app.py           # Main dashboard application
├── requirements.txt           # Package dependencies
└── README.md                 # This file
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 dsmflow

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments
- Data provided by [nflfastR](https://www.nflfastr.com/)
- Part of the [NFLverse](https://github.com/nflverse) project
- Created for Kaggle NFL competition analysis

## Notes for Kaggle Competition Use
This dashboard is designed to work with public NFL data and complies with Kaggle competition rules regarding public data usage. When using this tool for competition analysis:

1. Ensure you're complying with competition-specific rules about data usage
2. Validate that any insights derived are allowed to be shared publicly
3. Cite this tool appropriately if used in your competition submissions

## Support
For issues, questions, or contributions, please open an issue in the GitHub repository.
