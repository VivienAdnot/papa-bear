from typing import List
# from asset import Asset

class PortfolioLine:
  # asset: Asset
  ticker: str
  units: int
  book_price: float # euros ?
  market_price: float # euros ?

  def __init__(self, ticker, units, book_price):
    self.ticker = ticker
    self.units = units
    self.book_price = book_price
    self.market_price = book_price

  def __repr__(self):
    return f'line: {self.units} units of {self.ticker} bought at {self.book_price}€, currently worth {self.market_price}€. It is an unrealized gain of {self.latent_gain()}€'

  def latent_gain(self):
    total_book_value = self.units * self.book_price
    total_market_value = self.units * self.market_price
    return total_market_value - total_book_value


class Portfolio:
  lines: List[PortfolioLine] = []

  def __init__(self, lines = None):
    self.lines = lines if lines else []

  def latent_gain(self):
    cumulated_latent_gain = 0.00
    for line in self.lines:
      cumulated_latent_gain = cumulated_latent_gain + line.latent_gain()
    return cumulated_latent_gain

  def add_line(self, units, ticker, book_price):
    self.lines.append(PortfolioLine(
      ticker=ticker,
      units=units,
      book_price=book_price
    ))


class Investor:
  cash: float # euros ?
  portfolio: Portfolio

  def __init__(self, cash = 0.00, portfolio = None):
    self.cash = cash
    self.portfolio = portfolio if portfolio else Portfolio()

  def buy(self, units, ticker, book_price):
    cost = units * book_price
    if self.cash < cost:
      raise ValueError(f'{self.cash}€ cash available is insufficient to buy {units} units of {ticker} at {book_price}€')
    self.cash = self.cash - cost
    self.portfolio.add_line(units=units, ticker=ticker, book_price=book_price)