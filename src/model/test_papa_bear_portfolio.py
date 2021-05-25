import unittest
from papa_bear_portfolio import PapaBearPortfolio

class TestPapaBearPorfolio(unittest.TestCase):
  def xtest_compute_ticker_units_to_buy(self):
    portfolio = PapaBearPortfolio(cash=600.00)
    tickers_with_price = [('SPY', 60.00), ('TLT', 40.00), ('GLD', 20.00)]
    expected_result = [
      ('SPY',  3, 60.00),
      ('TLT', 5, 40.00),
      ('GLD', 10, 20.00)
    ]
    self.assertEqual(
      portfolio.compute_ticker_units_to_buy(tickers_with_price),
      expected_result
    )

  # [('IWD', 4, 81.95), ('EFA', 4, 72.38), ('EEM', 8, 37.32)]
  def test_compute_ticker_units_to_buy_2(self):
    portfolio = PapaBearPortfolio(cash=1000.00)
    tickers_with_price = [('IWD', 81.95), ('EFA', 72.38), ('EEM', 37.32)]
    expected_result = [
      ('IWD', 4, 81.95), # 327.8 => rest 5.53
      ('EFA', 4, 72.38), # 289.52 => rest 43.81
      ('EEM', 8, 37.32)  # 298.56 => rest 34.77
    ]
    self.assertEqual(
      portfolio.compute_ticker_units_to_buy(tickers_with_price),
      expected_result
    )

  def xtest_buy_winners(self):
    portfolio = PapaBearPortfolio(cash=600.00)
    self.assertEqual(len(portfolio.lines), 0)

    tickers_with_price = [('SPY', 60.00), ('TLT', 40.00), ('GLD', 20.00)]
    portfolio.buy_winners(tickers_with_price)
    self.assertEqual(len(portfolio.lines), 3)
    self.assertEqual(portfolio.cash, 20.00)

  def xtest_sell_then_buy_winners(self):
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
    portfolio = PapaBearPortfolio(cash=500.00, lines=lines)

    portfolio.sell_at_market(ticker='SPY')
    portfolio.sell_at_market(ticker='GLD')

    self.assertEqual(portfolio.cash, 815.00)

    tickers_with_price = [('SPY', 20.00), ('GLD', 90.00), ('TLT', 40.00)]
    portfolio.buy_winners(tickers_with_price)

    self.assertEqual(len(portfolio.lines), 3)
    self.assertEqual(portfolio.cash, 45.00)
    self.assertEqual(portfolio.value, 815.00)
    self.assertEqual(portfolio.value_history, [815.00])

