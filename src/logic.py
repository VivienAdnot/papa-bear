import numpy as np
from utils import get_3_max_values, average, compute_percentage_gain
from logger import Logger

tickers_informations = {
  0: {
    'exchange': 'NASDAQ',
    'ticker': 'IEF',
    'full_name': '7-10 Year Treasury Bond',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  1: {
    'exchange': 'NASDAQ',
    'ticker': 'VNQ',
    'full_name': 'Real Estate',
    'etf_provider': 'Vanguard',
    'etf_brand': 'Vanguard'
  },
  2: {
    'exchange': 'NYSEARCA',
    'ticker': 'EEM',
    'full_name': 'MSCI Emerging Markets',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  3: {
    'exchange': 'NYSEARCA',
    'ticker': 'IWF',
    'full_name': 'Russell 1000 Growth',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  4: {
    'exchange': 'NYSEARCA',
    'ticker': 'IWN',
    'full_name': 'Russell 2000 Value',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  5: {
    'exchange': 'NASDAQ',
    'ticker': 'TLT',
    'full_name': '20+ Year Treasury Bond',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  6: {
    'exchange': 'NYSEARCA',
    'ticker': 'IWO',
    'full_name': 'Russell 2000 Growth',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  7: {
    'exchange': 'NYSEARCA',
    'ticker': 'IWD',
    'full_name': 'Russell 1000 Value',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  8: {
    'exchange': 'NYSEARCA',
    'ticker': 'EFA',
    'full_name': 'Diversified Europe, Australia, Asia, and the Far East',
    'etf_provider': 'iShares',
    'etf_brand': 'BlackRock'
  },
  9: {
    'exchange': 'NYSEARCA',
    'ticker': 'GLD',
    'full_name': 'Gold',
    'etf_provider': 'State Street Global Advisors',
    'etf_brand': 'State Street Global Advisors'
  },
  10: {
    'exchange': 'NYSEARCA',
    'ticker': 'DBC',
    'full_name': 'Commodities',
    'etf_provider': 'PowerShares',
    'etf_brand': 'PowerShares'
  }
}

# average of current price, 1 month ago, 3 month ago, 6 month ago
def compute_average_gains(rows):
  average_gains = []
  for row_index, row in enumerate(rows):
    average_gains.append([])
    # we need at least 6 month of data
    if row_index >= 6:
      # print('row_index:', row_index)
      for cell_idx, cell in enumerate(row):
        # print( 'cell_idx:', cell_idx, 'cell:', cell)
        current_value = cell
        value_1_month_ago = rows[row_index - 1][cell_idx]
        value_3_month_ago = rows[row_index - 3][cell_idx]
        value_6_month_ago = rows[row_index - 6][cell_idx]

        # print('current_value: ', current_value)
        # print('value_1_month_ago: ', value_1_month_ago)
        # print('value_3_month_ago: ', value_3_month_ago)
        # print('value_6_month_ago: ', value_6_month_ago)

        percentage_gain_1_month = compute_percentage_gain(
          value_current=current_value,
          value_previous=value_1_month_ago
        )
        percentage_gain_3_month = compute_percentage_gain(
          value_current=current_value,
          value_previous=value_3_month_ago
        )
        percentage_gain_6_month = compute_percentage_gain(
          value_current=current_value,
          value_previous=value_6_month_ago  
        )

        # print('percentage_gain_1_month: ', percentage_gain_1_month)
        # print('percentage_gain_3_month: ', percentage_gain_3_month)
        # print('percentage_gain_6_month: ', percentage_gain_6_month)

        average_gain = average(percentage_gain_1_month, percentage_gain_3_month, percentage_gain_6_month)
        # print('average_gain: ', average_gain)
        average_gains[row_index].append(average_gain)
  return average_gains

# determines losers and new winners
def compute_winners_losers(
  current_winners_indices,
  new_winners_indices):

  winners_to_buy = []
  losers_to_sell = []
  keep_previous_winners = []
  
  for index, item in enumerate(current_winners_indices):
    # item_index, shares_amount = item
    if item not in new_winners_indices:
      # losers_to_sell.append((index, item))
      losers_to_sell.append(item)
    else:
      keep_previous_winners.append(item)

  for index, item in enumerate(new_winners_indices):
    if item not in current_winners_indices:
      # winners_to_buy.append((index, item))
      winners_to_buy.append(item)

  return (losers_to_sell, winners_to_buy, keep_previous_winners)

def perform_main_logic(rows, portfolio):
  logger = Logger()
  average_gains = compute_average_gains(rows)
  print('average_gains', average_gains)

  current_winners_indices = []

  print('------ loop avg_gain_rows ------')
  for row_index, row in enumerate(average_gains):
    if (row_index >= 6):
      cash_before = portfolio.cash
      value_before = portfolio.value

      print('avg_gains_row_idx', row_index)
      # print('current_winners_indices before arbitrage', current_winners_indices)
      # print(result[0])

      new_winners_indices, new_average_gains = get_3_max_values(row)
      print('new_winners_indices', new_winners_indices)
      # print('new_average_gains', new_average_gains)
      
      losers_to_sell, winners_to_buy, keep_previous_winners = compute_winners_losers(current_winners_indices, new_winners_indices)
      print('keep_previous_winners', keep_previous_winners)
      for keep_ticker_indice in keep_previous_winners:
        ticker = tickers_informations[keep_ticker_indice]['ticker']
        new_price = rows[row_index][keep_ticker_indice]
        print(keep_ticker_indice, ticker, new_price)
        portfolio.update_market_price(ticker=ticker, market_price=new_price)

      print('losers_to_sell', losers_to_sell)
      for loser_ticker_indice in losers_to_sell:
        ticker = tickers_informations[loser_ticker_indice]['ticker']
        new_price = rows[row_index][loser_ticker_indice]
        print(loser_ticker_indice, ticker, new_price)
        portfolio.update_market_price(ticker=ticker, market_price=new_price)
        portfolio.sell_at_market(ticker=ticker)

      print('cash after sell', portfolio.cash)

      print('winners_to_buy', winners_to_buy)
      winners_tickers_with_price = []
      for winner_ticker_indice in winners_to_buy:
        ticker = tickers_informations[winner_ticker_indice]['ticker']
        price = rows[row_index][winner_ticker_indice]
        winners_tickers_with_price.append((ticker, price))
      if len(winners_tickers_with_price):
        portfolio.buy_winners(winners_tickers_with_price)
        print('cash after buy', portfolio.cash)

      logger.log(
        round=row_index,
        current_winners_indices=current_winners_indices,
        cash_before=cash_before,
        value=portfolio.value,
        keep_previous_winners=keep_previous_winners,
        losers_to_sell=losers_to_sell,
        winners_to_buy=winners_to_buy,
        tickers_with_price='',
        cash_after=portfolio.cash,
        value_variation_absolute=portfolio.value-value_before
      )

      current_winners_indices[:] = new_winners_indices
      print('current_winners_indices after arbitrage', current_winners_indices)
  print('------ end loop avg_gain_rows ------')