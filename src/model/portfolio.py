from typing import List

class Portfolio:
  cash: float # euros ?
  lines = {}
  value: float # euros ?

  def __init__(self, cash = 0.00, lines = None):
    self.value = 0.00
    self.cash = cash
    self.lines = lines if lines else {}
    self.update_value()

  def update_value(self):
    value = self.cash
    for ticker, book in self.lines.items():
      market_price = book['market_price']
      units = len(book['book'])
      line_value = market_price * units
      value = value + line_value
    self.value = value

  def add_line(self, units, ticker, price):
    if ticker not in self.lines:
      self.lines[ticker] = { 'book': [] }
    
    self.lines[ticker]['market_price'] = price
    for _ in range(units):
      self.lines[ticker]['book'].append(price)

  def buy_at_market(self, units, ticker, price):
    cost = units * price
    if self.cash < cost:
      raise ValueError(f'{self.cash}€ cash available is insufficient to buy {units} units of {ticker} at {price}€')
    self.cash = self.cash - cost
    self.add_line(units=units, ticker=ticker, price=price)

  # units None means sell all
  def sell_at_market(self, ticker, units = None):
    if ticker not in self.lines:
      raise ValueError(f'ticker {ticker} not found in lines. Cannot sell')
    units_count = len(self.lines[ticker]['book'])
    if units and units_count < units:
      raise ValueError(f'line has {units_count} units but we want to sell {units}. Sell only {units_count}')
    units_to_remove = units if units and units < units_count else units_count
    market_price = self.lines[ticker]['market_price']

    for _ in range(units_to_remove):
      self.lines[ticker]['book'].pop()
      self.cash = self.cash + market_price

  def sell_all_at_market(self):
    for ticker in self.lines:
      market_price = self.lines[ticker]['market_price']
      for _ in range(len(self.lines[ticker]['book'])):
        self.lines[ticker]['book'].pop()
        self.cash = self.cash + market_price

  def update_market_price(self, ticker, market_price):
    if ticker not in self.lines:
      self.lines[ticker] = { 'book': [] }
    self.lines[ticker]['market_price'] = market_price