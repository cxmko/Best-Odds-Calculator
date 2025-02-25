# Best-Odds-Calculator

A Python tool for analyzing betting odds across multiple sports betting websites to find arbitrage betting strategies, particularly for taking advantage of welcome bonuses.

## Overview

This tool helps you:
1. Scrape betting odds from multiple sports betting websites
2. Identify the best betting opportunities
3. Calculate optimal bet distribution to minimize risk
4. Maximize returns from welcome bonuses offered by betting sites

## Features

- Web scraping of betting odds from multiple sites
- Automatic matching of teams across different sites
- Calculation of optimal bet distribution
- Detection of arbitrage opportunities (sure bets)
- Support for multiple sports leagues

## Installation

```bash
# Clone the repository
git clone https://github.com/cxmko/Best-Odds-Calculator.git
cd Best-Odds-Calculator

# Install dependencies
pip install -r requirements.txt

# Download Chrome WebDriver
# Visit: https://chromedriver.chromium.org/downloads
# Download the version that matches your Chrome browser
# Extract and update the path in config/config.yaml
```

## Configuration

Update the `config/config.yaml` file with:

1. Path to your ChromeDriver
2. Betting websites you want to use
3. Total amount you want to bet
4. League you want to analyze

```yaml
webdriver_path: "/path/to/your/chromedriver"
selected_league: "premier_league"
betting:
  total_amount: 300
```

## Usage

```bash
# Run the main script
python -m src.main
```

## How It Works

1. **Scrape Odds**: The tool scrapes betting odds from configured websites for a selected league.
2. **Find Best Opportunity**: It analyzes all possible combinations of bets across the sites.
3. **Calculate Bet Distribution**: For the best opportunity, it calculates how much to bet on each outcome.
4. **Display Results**: It shows the optimal betting strategy and potential profits/losses.

### Betting Strategy

The strategy works in two phases:

1. **First Bet**:
   - Place bets across multiple betting sites to trigger welcome bonuses
   - The tool calculates the optimal distribution to minimize risk

2. **Second Bet**:
   - After receiving bonuses, place a second bet as required by the sites
   - The tool minimizes potential losses on this bet
   - The overall result should be a net gain due to the bonuses

## Directory Structure

```
Best-Odds-Calculator/
├── config/               # Configuration files
│   └── config.yaml
├── src/                  # Source code
│   ├── calculators/      # Betting calculation modules
│   ├── scrapers/         # Web scraping modules
│   ├── utils/            # Utility functions
│   └── main.py           # Main application script
├── tests/                # Test cases
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

## Results

Over the course of the two bets, the strategy has been tested and proven to generate a net gain.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

