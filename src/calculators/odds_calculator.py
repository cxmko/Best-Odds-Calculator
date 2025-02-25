# Odds calculator module
"""
Calculator for analyzing betting odds and determining optimal betting strategies.
"""


def invsum(x, y, z):
    """
    Calculates the sum of inverses of odds.
    
    Args:
        x (str/float): First odds value
        y (str/float): Second odds value
        z (str/float): Third odds value
    
    Returns:
        float: Sum of inverses
    """
    return 1 / float(x) + 1 / float(y) + 1 / float(z)


def find_optimal_odds(odds_list_a, odds_list_b, odds_list_c, match_names, num_matches):
    """
    Finds the optimal odds and the corresponding bet distribution.
    
    Args:
        odds_list_a (list): List of odds from first site
        odds_list_b (list): List of odds from second site
        odds_list_c (list): List of odds from third site
        match_names (list): List of match names
        num_matches (int): Number of matches to consider
    
    Returns:
        tuple: (optimal_odds, inverse_sum, best_match_name)
    """
    optimal_odds = [odds_list_a[0][0], odds_list_b[0][1], odds_list_c[0][2]]
    best_match = match_names[0]
    best_inv_sum = invsum(optimal_odds[0], optimal_odds[1], optimal_odds[2])
    
    for i in range(num_matches):
        for j in range(3):  # Three possible outcomes: home win, draw, away win
            k1 = (j + 1) % 3  # Next outcome
            k2 = (j + 2) % 3  # Third outcome
            
            # Potential new set of odds
            current_odds = [odds_list_a[i][j], odds_list_b[i][k1], odds_list_c[i][k2]]
            current_inv_sum = invsum(current_odds[0], current_odds[1], current_odds[2])
            
            # Check if this is better than our current best
            if current_inv_sum < best_inv_sum:
                optimal_odds = current_odds
                best_inv_sum = current_inv_sum
                best_match = match_names[i]
    
    return optimal_odds, best_inv_sum, best_match


def calculate_bet_distribution(optimal_odds, total_amount):
    """
    Calculates how to distribute bets across different outcomes.
    
    Args:
        optimal_odds (list): List of optimal odds [home, draw, away]
        total_amount (float): Total amount to bet
    
    Returns:
        tuple: (base_unit, [amount_on_home, amount_on_draw, amount_on_away])
    """
    inverse_sum = invsum(optimal_odds[0], optimal_odds[1], optimal_odds[2])
    
    # If inverse_sum < 1, we have a sure bet (arbitrage opportunity)
    is_sure_bet = inverse_sum < 1
    
    # Base unit for bet distribution
    base_unit = total_amount / inverse_sum
    
    # Calculate amounts to bet on each outcome
    bet_amounts = [
        base_unit / float(optimal_odds[0]),
        base_unit / float(optimal_odds[1]),
        base_unit / float(optimal_odds[2])
    ]
    
    return base_unit, bet_amounts, is_sure_bet


def calculate_profit_loss(odds, bet_amounts, is_sure_bet):
    """
    Calculates profit or loss for each outcome.
    
    Args:
        odds (list): List of odds
        bet_amounts (list): List of bet amounts
        is_sure_bet (bool): Whether this is a sure bet
    
    Returns:
        list: Profit for each outcome
    """
    total_bet = sum(bet_amounts)
    profits = []
    
    for i in range(3):
        # Potential winnings
        winnings = bet_amounts[i] * float(odds[i])
        # Profit is winnings minus total bet
        profit = winnings - total_bet
        profits.append(profit)
    
    return profits