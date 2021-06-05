from datetime import date
import csv
from typing import Any
from utils import convert_to_year, convert_to_month, convert_month_index_to_string, convert_to_year_15_years_ago
from ticker_informations import get_ticker_from_indice

class Logger:
  file_name = 'papa_bear.csv'
  file_writer: Any

  def __init__(self):
    papa_bear_file = open(self.file_name, mode='w')
    self.file_writer = csv.writer(papa_bear_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    self.file_writer.writerow([
      '',
      'Y idx',
      'year',
      'month',
      'curr winners idx',
      '$ before',
      'value',
      'hold',
      'sell',
      'buy',
      '$ after',
      '$ value change'
    ])

  def log(
    self,
    portfolio,
    round,
    current_winners_indices,
    cash_before,
    value,
    keep_previous_winners,
    losers_to_sell,
    winners_to_buy,
    cash_after,
    value_variation_absolute):
    year_index = convert_to_year(round)
    year_date_years_ago = convert_to_year_15_years_ago(round)

    keep_previous_winners_infos = []

    for winner_index in keep_previous_winners:
      ticker = get_ticker_from_indice(winner_index)
      latent_profit = f'{portfolio.get_latent_profit(ticker)}€'
      units = len(portfolio.lines[ticker]['book'])
      market_price = portfolio.lines[ticker]['market_price']
      keep_previous_winners_infos.append((ticker, latent_profit, f'{units} at {market_price}€'))

    month = convert_month_index_to_string(convert_to_month(round) + 1)
    self.file_writer.writerow([
      round,
      year_index,
      year_date_years_ago,
      month,
      current_winners_indices,
      cash_before,
      value,
      keep_previous_winners_infos,
      losers_to_sell,
      winners_to_buy,
      cash_after,
      value_variation_absolute
    ])
