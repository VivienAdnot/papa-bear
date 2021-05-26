import unittest
from papa_bear_portfolio import PapaBearPortfolio

class TestPapaBearPorfolio(unittest.TestCase):
  def xtest_compute_ticker_units_to_buy_2(self):
    portfolio = PapaBearPortfolio(cash=1000.00)
    tickers_with_price = [('IWD', 81.95, 14.42), ('EFA', 72.38, 8.72), ('EEM', 37.32, 26.13)]
    expected_result = [
      ('EEM', 8, 37.32),
      ('IWD', 4, 81.95),
      ('EFA', 4, 72.38),
      ('EEM', 1, 37.32), # buy one more
      ('EEM', 1, 37.32), # buy one more
    ]

    self.assertEqual(
      portfolio.compute_ticker_units_to_buy(tickers_with_price),
      expected_result
    )

  def test_buy_winners(self):
    portfolio = PapaBearPortfolio(cash=600.00)
    self.assertEqual(len(portfolio.lines), 0)

    tickers_with_price = [('IWD', 81.95, 14.42), ('EFA', 72.38, 8.72), ('EEM', 37.32, 26.13)]
    portfolio.buy_winners(tickers_with_price)
    self.assertEqual(len(portfolio.lines), 3)
    self.assertEqual(portfolio.cash, 30.1)

  def test_sell_then_buy_winners(self):
    lines = {
      'IWD': {
        'book': [70.0],
        'market_price': 70.0
      },
      'EFA': {
        'book': [60.0],
        'market_price': 60.00
      }
    }
    portfolio = PapaBearPortfolio(cash=500.00, lines=lines)

    portfolio.sell_at_market(ticker='IWD')
    portfolio.sell_at_market(ticker='EFA')

    self.assertEqual(portfolio.cash, 630.00)

    tickers_with_price = [('IWD', 81.95, 14.42), ('EFA', 72.38, 8.72), ('EEM', 37.32, 26.13)]
    portfolio.buy_winners(tickers_with_price)

    self.assertEqual(len(portfolio.lines), 3)
    self.assertEqual(portfolio.cash, 15.47)
    self.assertEqual(portfolio.value, 630.00)
    self.assertEqual(portfolio.value_history, [630.00])

