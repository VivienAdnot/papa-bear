import csv
from typing import Any
from utils import convert_to_year, convert_to_month

class Logger:
  file_name = 'papa_bear.csv'
  file_writer: Any # todo define type

  def __init__(self):
    papa_bear_file = open(self.file_name, mode='w')
    self.file_writer = csv.writer(papa_bear_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    self.file_writer.writerow(['round', 'year', 'month', 'current_winners_indices', 'cash_before', 'value', 'keep_previous_winners', 'losers_to_sell' ,'winners_to_buy', 'tickers_with_price', 'cash_after', 'value_variation_absolute'])

  def log(self, round, current_winners_indices, cash_before, value, keep_previous_winners, losers_to_sell, winners_to_buy, tickers_with_price, cash_after, value_variation_absolute):
    year = convert_to_year(round)
    month = convert_to_month(round)
    self.file_writer.writerow([round, year, month, current_winners_indices, cash_before, value, keep_previous_winners, losers_to_sell ,winners_to_buy, tickers_with_price, cash_after, value_variation_absolute])
