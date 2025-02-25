# Main application entry point
"""
Main script for the Best-Odds-Calculator application.
"""

import os
import yaml
from src.scrapers.odds_scraper import OddsScraper
from src.calculators.odds_calculator import (
    find_optimal_odds, calculate_bet_distribution, calculate_profit_loss
)


def load_config(config_path):
    """
    Load configuration from a YAML file.
    
    Args:
        config_path (str): Path to the configuration file
    
    Returns:
        dict: Configuration dictionary
    """
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def main():
    """Main function that runs the application."""
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    config = load_config(config_path)
    
    # Initialize scraper
    scraper = OddsScraper(webdriver_path=config['webdriver_path'])
    
    # Use selected league configuration
    league_config = config['leagues'][config['selected_league']]
    
    print(f"Scraping odds for {config['selected_league']}...")
    
    # Get odds data
    odds_data = scraper.get_odds(
        site_urls=league_config['urls'],
        container_classes=league_config['container_classes'],
        match_classes=league_config['match_classes'],
        odds_classes=league_config['odds_classes']
    )
    
    # Extract odds lists and match names
    odds_lists = [odds_data[i]["odds"] for i in range(len(league_config['urls']))]
    match_names = odds_data[0]["teams"]
    
    # Find optimal odds
    optimal_odds, inv_sum, best_match = find_optimal_odds(
        odds_lists[0], odds_lists[1], odds_lists[2],
        match_names, len(match_names)
    )
    
    total_amount = config['betting']['total_amount']
    
    # Calculate bet distribution
    base_unit, bet_amounts, is_sure_bet = calculate_bet_distribution(optimal_odds, total_amount)
    
    # Calculate potential profits/losses
    profits = calculate_profit_loss(optimal_odds, bet_amounts, is_sure_bet)
    
    # Display results
    print("\n=== OPTIMAL BETTING STRATEGY ===")
    print(f"Best match: {best_match}")
    print(f"Optimal odds: {optimal_odds}")
    print(f"Inverse sum: {inv_sum:.4f}")
    print(f"Sure bet opportunity: {'Yes' if is_sure_bet else 'No'}")
    
    print("\n=== BET DISTRIBUTION ===")
    outcome_labels = ["Home win", "Draw", "Away win"]
    for i in range(3):
        print(f"{outcome_labels[i]}: ${bet_amounts[i]:.2f} at odds {optimal_odds[i]}")
    
    print("\n=== POTENTIAL RESULTS ===")
    for i in range(3):
        result = "Profit" if profits[i] > 0 else "Loss"
        print(f"If {outcome_labels[i].lower()}: {result} of ${abs(profits[i]):.2f}")
    
    print(f"\nTotal Bet: ${sum(bet_amounts):.2f}")


if __name__ == "__main__":
    main()