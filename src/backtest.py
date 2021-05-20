import csv
import numpy as np
from logic import perform_main_logic
from model.portfolio import Portfolio

def parseCsv(spamreader):
  result = []
  for index, row in enumerate(spamreader):
    if index >= 10 and index < 18:
    # if index >= 10:
      values = row[0].split(',')
      values.pop(0)
      x = np.asfarray(values, float)
      result.append(x)
  result.reverse()
  return result

def main(investor):
  with open('data/papabear-15y-210510.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    rows = parseCsv(spamreader)
    print(rows)
    perform_main_logic(rows, investor)

start_cash = 1000 # dollars
portfolio = Portfolio(cash=start_cash)
main(portfolio)