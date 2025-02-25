# Test for calculator module
"""
Tests for the odds calculator module.
"""

import unittest
from src.calculators.odds_calculator import invsum, find_optimal_odds, calculate_bet_distribution


class TestOddsCalculator(unittest.TestCase):
    def test_invsum(self):
        """Test calculation of inverse sum."""
        # Test with integer odds
        result = invsum(2, 3, 4)
        expected = 1/2 + 1/3 + 1/4
        self.assertAlmostEqual(result, expected)
        
        # Test with string odds
        result = invsum("2.5", "3.0", "4.2")
        expected = 1/2.5 + 1/3.0 + 1/4.2
        self.assertAlmostEqual(result, expected)
    
    def test_calculate_bet_distribution(self):
        """Test calculation of bet distribution."""
        # Test with total amount 600
        odds = ["2.5", "3.0", "4.2"]
        total_amount = 600
        base_unit, bet_amounts, is_sure_bet = calculate_bet_distribution(odds, total_amount)
        
        # Check sum of bet amounts is close to total amount
        self.assertAlmostEqual(sum(bet_amounts), total_amount, delta=0.01)
        
        # Check individual bet amounts
        expected_amounts = [
            base_unit / float(odds[0]),
            base_unit / float(odds[1]),
            base_unit / float(odds[2])
        ]
        for calc, expected in zip(bet_amounts, expected_amounts):
            self.assertAlmostEqual(calc, expected, delta=0.01)


if __name__ == '__main__':
    unittest.main()