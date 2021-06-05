from typing import List

class Portfolio:
  cash: float # euros ?
  lines = {}
  value: float # euros ?
  value_history = []
  month = 0
  year=0
  taxes_profit_loss_year_history = []
  taxes_to_pay = 0
  paid_tax_history = {}

  def __init__(self, cash = 0.00, lines = None):
    self.value = 0.00
    self.value_history = []
    self.cash = cash
    self.lines = lines if lines else {}
    self.update_value()

  def pay_taxes(self):
    self.paid_tax_history[self.year] = {
      'paid': False,
      'amount': 0
    }
    total_year_profit_loss = round(sum(self.taxes_profit_loss_year_history), 2)
    # print(f'{self.year}: total_year_profit_loss: {total_year_profit_loss}')

    if total_year_profit_loss < 0:
      self.paid_tax_history[self.year]['paid'] = True
      self.paid_tax_history[self.year]['amount'] = 0
      # print(f'no need to pay taxes this year')
      return

    # in case we didn't finish to pay last year taxes
    self.taxes_to_pay = round(self.taxes_to_pay + total_year_profit_loss * 0.3, 2)
    # print(f'{self.year}: taxes_to_pay: {self.taxes_to_pay}')

    # print(f'try pay {self.taxes_to_pay}€ taxes with {self.cash}€ cash.')
    self.taxes_profit_loss_year_history.clear()
    # if portfolio has enough cash
    if self.cash > self.taxes_to_pay:
      self.cash = round(self.cash - self.taxes_to_pay, 2)
      # print(f'paid whole taxes. cash is now {self.cash}')
      self.paid_tax_history[self.year]['paid'] = True
      self.paid_tax_history[self.year]['amount'] = self.taxes_to_pay
      self.taxes_to_pay = 0
    # if we do not have enough cash
    else:
      self.taxes_to_pay = self.taxes_to_pay - self.cash
      # print(f'partially paid taxes. {self.taxes_to_pay} left to pay')
      self.cash = 0
    self.update_value()

  def compute_pending_taxes(self, new_profit_or_loss):
    self.taxes_profit_loss_year_history.append(new_profit_or_loss)

  def update_value(self):
    value = self.cash
    for ticker, book in self.lines.items():
      market_price = book['market_price']
      units = len(book['book'])
      line_value = round(market_price * units, 2)
      value = round(value + line_value, 2)
    # no need to update if value has not changed
    if self.value != value:
      self.value = value
      self.value_history.append(self.value)

  def update_market_price(self, ticker, market_price):
    if ticker not in self.lines:
      self.lines[ticker] = { 'book': [] }
    self.lines[ticker]['market_price'] = market_price
    self.update_value()

  def buy_at_market(self, units, ticker, price):
    # this method also updates inner book value
    self.update_market_price(ticker=ticker, market_price=price)
    cost = round(units * price, 2)
    if self.cash < cost:
      raise ValueError(f'{self.cash}€ cash available is insufficient to buy {units} units of {ticker} at {price}€')
    self.cash = round(self.cash - cost, 2)
    # print(f'buy at market {units} units of {ticker} at {price}$. cash is now {self.cash}')
    if ticker not in self.lines:
      self.lines[ticker] = { 'book': [] }
    
    for _ in range(units):
      self.lines[ticker]['book'].append(price)

  def should_pay_tax(self):
    return self.month == 1 and self.year not in self.paid_tax_history
    # or self.paid_tax_history[self.year]['paid'] == False)

  # units None means sell all
  # update_market_price is called outside of the method
  def sell_at_market(self, ticker, units = None):
    if ticker not in self.lines:
      raise ValueError(f'ticker {ticker} not found in lines. Cannot sell')
    units_count = len(self.lines[ticker]['book'])
    if units and units_count < units:
      raise ValueError(f'line has {units_count} units but we want to sell {units}. Sell only {units_count}')
    units_to_remove = units if units and units < units_count else units_count
    market_price = self.lines[ticker]['market_price']

    for _ in range(units_to_remove):
      book_price = self.lines[ticker]['book'].pop()
      # print(f'sell_at_market:: {self.cash} + {market_price} => {round(self.cash + market_price, 2)}')
      profit_or_loss = market_price - book_price
      self.cash = round(self.cash + market_price, 2)
      self.compute_pending_taxes(profit_or_loss)
    
    # january: time to pay our taxes
    if self.should_pay_tax():
      self.pay_taxes()

  def sell_all_at_market(self):
    for ticker in self.lines:
      market_price = self.lines[ticker]['market_price']
      for _ in range(len(self.lines[ticker]['book'])):
        self.lines[ticker]['book'].pop()
        self.cash = round(self.cash + market_price, 2)

  def get_average_book_price(self, ticker):
    if ticker not in self.lines:
      raise ValueError(f'ticker {ticker} not found in lines.')
    book = self.lines[ticker]['book']
    if len(book) == 0:
      return 0
    return round(sum(book) / len(book), 2)

  def get_latent_profit(self, ticker):
    if ticker not in self.lines:
      raise ValueError(f'ticker {ticker} not found in lines.')
    average_book_price = self.get_average_book_price(ticker)
    units = len(self.lines[ticker]['book'])
    market_price = self.lines[ticker]['market_price']
    return round((market_price * units) - (average_book_price * units), 2)