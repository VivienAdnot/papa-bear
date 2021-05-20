from typing import List

class Portfolio:
  cash: float # euros ?
  lines = {}

  def __init__(self, cash = 0.00, lines = None):
    self.cash = cash
    self.lines = lines if lines else {}

  def add_line(self, units, ticker, book_price):
    if ticker not in self.lines:
      self.lines[ticker] = { 'book': [] }
    
    self.lines[ticker]['market_price'] = book_price
    for _ in range(units):
      self.lines[ticker]['book'].append(book_price)

  def buy_at_market(self, units, ticker, book_price):
    cost = units * book_price
    if self.cash < cost:
      raise ValueError(f'{self.cash}€ cash available is insufficient to buy {units} units of {ticker} at {book_price}€')
    self.cash = self.cash - cost
    self.add_line(units=units, ticker=ticker, book_price=book_price)

  # units None means sell all
  def sell_at_market(self, ticker, units = None):
    if ticker not in self.lines:
      raise ValueError(f'ticker {ticker} not found in lines. Cannot sell')
    units_count = len(self.lines[ticker]['book'])
    if units and units_count < units:
      raise ValueError(f'line has {units_count} units but we want to sell {units}. Sell only {units_count}')
    units_to_remove = units if units < units_count else units_count
    market_price = self.lines[ticker]['market_price']

    for _ in range(units_to_remove):
      book_price = self.lines[ticker]['book'].pop()
      self.cash = self.cash + market_price - book_price

  def update_market_price(self, ticker, market_price):
    if ticker not in self.lines:
      self.lines[ticker] = { 'book': [] }
    self.lines[ticker]['market_price'] = market_price