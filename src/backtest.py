import csv
import numpy as np
from logic import perform_main_logic
from model.papa_bear_portfolio import PapaBearPortfolio

def parseCsv(spamreader):
  result = []
  for index, row in enumerate(spamreader):
    # if index >= 10 and index < 18:
    if index >= 10:
      values = row[0].split(',')
      values.pop(0)
      x = np.asfarray(values, float)
      result.append(x)
  result.reverse()
  return result

def main(portfolio):
  with open('data/papabear-15y-210510.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    rows = parseCsv(spamreader)
    print(rows)
    perform_main_logic(rows, portfolio)
    portfolio.sell_all_at_market()
    print('final cash', portfolio.cash)

start_cash = 1000 # dollars
portfolio = PapaBearPortfolio(cash=start_cash)
main(portfolio)