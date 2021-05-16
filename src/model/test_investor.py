import unittest
from investor import Portfolio, PortfolioLine, Investor

class TestPortfolioLine(unittest.TestCase):
  def test_latent_gain(self):
    line = PortfolioLine(
      ticker="SPY",
      units=10,
      book_price=50.00,
    )
    line.market_price=52.00

    self.assertEqual(line.latent_gain(), 20.00)

class TestPorfolio(unittest.TestCase):
  def test_latent_gain_positive(self):
    portfolio = Portfolio(lines=[
      PortfolioLine(ticker="SPY",units=10,book_price=50.00),
      PortfolioLine(ticker="GLD",units=5,book_price=80.00)
    ])

    portfolio.lines[0].market_price = 52.00
    portfolio.lines[1].market_price = 85.00

    self.assertEqual(portfolio.latent_gain(), 45.00)

  def test_latent_gain_negative(self):
    portfolio = Portfolio(lines=[
      PortfolioLine(ticker="SPY",units=10,book_price=50.00),
      PortfolioLine(ticker="GLD",units=5,book_price=80.00)
    ])

    portfolio.lines[0].market_price = 52.00
    portfolio.lines[1].market_price = 75.00

    self.assertEqual(portfolio.latent_gain(), -5.00)

  def test_add_line(self):
    portfolio = Portfolio()
    portfolio.add_line(ticker="SPY",units=10,book_price=50.00)

    self.assertEqual(len(portfolio.lines), 1)
    portfolio.lines[0].market_price = 60.00
    self.assertEqual(portfolio.latent_gain(), 100.00)

class TestInvestor(unittest.TestCase):
  def test_buy_should_be_ok(self):
    investor = Investor(cash=1000.00)
    self.assertEqual(len(investor.portfolio.lines), 0)
    
    investor.buy(units=10, ticker='SPY', book_price=10.00)
    self.assertEqual(len(investor.portfolio.lines), 1)
    self.assertEqual(investor.cash, 900.00)

  def test_buy_should_be_raise(self):
    investor = Investor(cash=10.00)
    try:
      investor.buy(units=10, ticker='SPY', book_price=10.00)
    except ValueError as err:
      self.assertEqual(err.args[0], '10.0€ cash available is insufficient to buy 10 units of SPY at 10.0€')
      self.assertEqual(len(investor.portfolio.lines), 0)
      self.assertEqual(investor.cash, 10.00)