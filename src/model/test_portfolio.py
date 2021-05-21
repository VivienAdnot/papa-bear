import unittest
from portfolio import Portfolio

class TestPorfolio(unittest.TestCase):
  def build_portfolio(self, cash=None):
    _cash = cash if cash else 500.00
    lines = {
      'SPY': {
        'book': [10.00, 10.00, 10.00, 10.00, 10.00, 15.00, 15.00],
        'market_price': 15.00
      },
      'GLD': {
        'book': [70.00, 70.00, 70.00],
        'market_price': 70.00
      }
    }
    default_portfolio = Portfolio(cash=_cash, lines=lines)
    return default_portfolio

  def test_lines(self):
    portfolio = self.build_portfolio()
    self.assertEqual(list(portfolio.lines.keys()), ['SPY', 'GLD'])

  def test_value(self):
    portfolio = self.build_portfolio()
    self.assertEqual(portfolio.value, 815.00)
    self.assertEqual(portfolio.value_history, [815.00])

  def test_update_market_price(self):
    portfolio = self.build_portfolio()
    self.assertEqual(portfolio.value, 815.00)
    self.assertEqual(portfolio.value_history, [815.00])

    portfolio.update_market_price(ticker='SPY', market_price=20.00)
    self.assertEqual(portfolio.lines['SPY']['market_price'], 20.00)
    self.assertEqual(portfolio.value, 850.00)
    self.assertEqual(portfolio.value_history, [815.00, 850.00])

    portfolio.update_market_price(ticker='GLD', market_price=90.00)
    self.assertEqual(portfolio.lines['GLD']['market_price'], 90.00)
    self.assertEqual(portfolio.value, 910.00)
    self.assertEqual(portfolio.value_history, [815.00, 850, 910.00])

  def test_buy_should_be_ok(self):
    portfolio = self.build_portfolio()
    self.assertEqual(len(portfolio.lines['SPY']['book']), 7)
    
    portfolio.buy_at_market(units=10, ticker='SPY', price=10.00)
    self.assertEqual(len(portfolio.lines['SPY']['book']), 17)
    self.assertEqual(portfolio.cash, 400.00)
    # the value has decreased becaue SPY value is back at 10, not 15
    self.assertEqual(portfolio.value, 780.0)
    self.assertEqual(portfolio.value_history, [815.00, 780.00])

  def test_buy_should_raise_error(self):
    portfolio = Portfolio(cash=10.00)
    try:
      portfolio.buy_at_market(units=10, ticker='SPY', price=10.00)
    except ValueError as err:
      self.assertEqual(err.args[0], '10.0€ cash available is insufficient to buy 10 units of SPY at 10.0€')
      self.assertEqual(portfolio.cash, 10.00)

  def test_sell_high_should_increase_value(self):
    portfolio = self.build_portfolio()
    portfolio.update_market_price(ticker='GLD', market_price=90.00)
    self.assertEqual(portfolio.value_history, [815.00, 875.00])

    portfolio.sell_at_market(ticker='GLD', units=2)
    self.assertEqual(portfolio.cash, 680.00)
    self.assertEqual(portfolio.value, 875.00)
    # the value has not changed, we just transformed stocks into cash
    self.assertEqual(portfolio.value_history, [815.00, 875.00])

  def test_sell_all(self):
    portfolio = self.build_portfolio()
    portfolio.sell_all_at_market()
    self.assertEqual(portfolio.cash, 815.00)
    self.assertEqual(len(portfolio.lines['SPY']['book']), 0)
    self.assertEqual(len(portfolio.lines['GLD']['book']), 0)

