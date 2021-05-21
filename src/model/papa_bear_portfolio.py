# from portfolio import Portfolio
from model.portfolio import Portfolio
import math

class PapaBearPortfolio(Portfolio):
  def sell_losers(self, tickers):
    for loser_ticker in tickers:
      self.sell_at_market(loser_ticker)
    pass

  def compute_ticker_units_to_buy(self, tickers_with_price):
    results = []
    number_assets = len(tickers_with_price)
    max_cash_per_asset = self.cash / number_assets

    for (ticker, price) in tickers_with_price:
      units = math.floor(max_cash_per_asset / price)
      results.append((ticker, units, price))
    return results

  def buy_winners(self, tickers_with_price):
    computed_values = self.compute_ticker_units_to_buy(tickers_with_price)
    for (ticker, units, price) in computed_values:
      self.buy_at_market(units=units, ticker=ticker, price=price)