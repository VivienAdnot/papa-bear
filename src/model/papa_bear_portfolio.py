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
    # print(number_assets, max_cash_per_asset)

    idx = -1
    sorted_tickers_by_gain_desc = sorted(tickers_with_price, key=lambda tup: tup[2], reverse=True)
    sorted_tickers_by_price_asc = sorted(tickers_with_price, key=lambda tup: tup[1], reverse=False)
    amount = 0
    minimum_price = sorted_tickers_by_price_asc[0][1]

    for (ticker, price, average_gain) in sorted_tickers_by_gain_desc:
      idx = idx + 1
      units = math.floor(max_cash_per_asset / price)
      amount = amount + (units * price)
      # print(idx, ticker, units, price)
      results.append((ticker, units, price))
    
    # second round for filling the rest
    rest = self.cash - amount
    # print('rest', rest, 'minimum price', minimum_price)
    while rest > 0 and minimum_price < rest:
      for (ticker, price, average_gain) in sorted_tickers_by_gain_desc:
        if rest > 0 and price < rest:
          amount = amount + price
          rest = self.cash - amount
          # print(f'buy 1 more unit of {ticker} at {price}€')
          results.append((ticker, 1, price))

    return results

  def buy_winners(self, tickers_with_price):
    tickers_with_price_and_units = self.compute_ticker_units_to_buy(tickers_with_price)
    for (ticker, units, price) in tickers_with_price_and_units:
      self.buy_at_market(units=units, ticker=ticker, price=price)
    return tickers_with_price_and_units