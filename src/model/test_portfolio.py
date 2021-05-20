import unittest
from portfolio import Portfolio

class TestPorfolio(unittest.TestCase):
  def setUp(self):
    self.portfolio1 = Portfolio(cash=500.00)
    self.portfolio1.add_line(units=5, ticker='SPY', price=10.00)
    self.portfolio1.add_line(units=2, ticker='SPY', price=15.00)
    self.portfolio1.add_line(units=3, ticker='GLD', price=70.00)

    self.portfolio1.update_market_price(ticker='SPY', market_price=20.00)
    self.portfolio1.update_market_price(ticker='GLD', market_price=90.00)

  def test_lines(self):
    self.assertEqual(list(self.portfolio1.lines.keys()), ['SPY', 'GLD'])

  def test_update_market_price(self):
    self.assertEqual(self.portfolio1.lines['SPY']['market_price'], 20.00)
    self.assertEqual(self.portfolio1.lines['GLD']['market_price'], 90.00)

  def test_buy_should_be_ok(self):
    portfolio = Portfolio(cash=1000.00)
    self.assertEqual(len(portfolio.lines), 0)
    
    portfolio.buy_at_market(units=10, ticker='SPY', price=10.00)
    self.assertEqual(len(portfolio.lines), 1)
    self.assertEqual(portfolio.cash, 900.00)

  def test_buy_should_raise_error(self):
    portfolio = Portfolio(cash=1000.00)
    try:
      portfolio.buy_at_market(units=10, ticker='SPY', price=10.00)
    except ValueError as err:
      self.assertEqual(err.args[0], '10.0€ cash available is insufficient to buy 10 units of SPY at 10.0€')
      self.assertEqual(len(portfolio.lines), 0)
      self.assertEqual(portfolio.cash, 10.00)

  def test_sell(self):
    self.portfolio1.sell_at_market(ticker='GLD', units=2)
    self.assertEqual(self.portfolio1.cash, 680.00)