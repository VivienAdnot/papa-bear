import unittest
from papa_bear_portfolio import PapaBearPortfolio

class TestPapaBearPorfolio(unittest.TestCase):
  def test_compute_ticker_units_to_buy(self):
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

  def test_buy_winners(self):
    portfolio = PapaBearPortfolio(cash=600.00)
    self.assertEqual(len(portfolio.lines), 0)

    tickers_with_price = [('SPY', 60.00), ('TLT', 40.00), ('GLD', 20.00)]
    portfolio.buy_winners(tickers_with_price)
    self.assertEqual(len(portfolio.lines), 3)
    self.assertEqual(portfolio.cash, 20.00)

  def test_sell_then_buy_winners(self):
    portfolio = PapaBearPortfolio(cash=0.00)

    portfolio.add_line(units=10, ticker='SPY', price=10.00)
    portfolio.add_line(units=2, ticker='TLT', price=250.00)

    portfolio.sell_at_market(ticker='SPY')
    portfolio.sell_at_market(ticker='TLT')

    self.assertEqual(portfolio.cash, 600.00)

    tickers_with_price = [('SPY', 60.00), ('TLT', 40.00), ('GLD', 20.00)]
    portfolio.buy_winners(tickers_with_price)
    self.assertEqual(len(portfolio.lines), 3)
    self.assertEqual(portfolio.cash, 20.00)
