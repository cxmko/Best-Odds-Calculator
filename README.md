# Best-Odds-Calculator

This code is designed to help you take advantage of betting bonuses across three different sports betting websites using web scraping. The idea is to place equal bets on a match across the three sites to trigger the welcome bonus, which often requires placing a second bet after the first. While the code could still be polished and improved, I have tested it successfully and achieved net gains.

## How it works:

1. **Identify welcome bonuses**:
   You select three different betting websites (unlike in the code which is a test version) that offer a welcome bonus (e.g., if you lose or win, you get your money back). The code identifies the odds for a specific football match (although the code can be easily adapted to other sports).

2. **Place Your Bets**:
   The strategy first requires you to place an equal amount of money on all three websites. The code then calculates the best first bet by identifying the odds that are closest to 3 on each website (for 3 outcomes), which minimizes risk and ensures a constant gain across all outcomes.

3. **Second Bet**:
   After the first bet, the websites usually force you to place a second bet before releasing the bonus. The code uses a mathematical formula (the sum of the inverse of the odds) to calculate the optimal second bet (it tells you the amount to be betted on each website for each outcome of the "best match") , which will most likely result in a loss (unless it detects sure-bets that are very rare) which is also constant across all outcomes (the code will also return a loss coefficient). However, the code minimizes this loss to ensure that the overall result after both bets is a net gain.

4. **Result**:
   Over the course of the two bets, the strategy has been tested and proven to generate a net gain.


