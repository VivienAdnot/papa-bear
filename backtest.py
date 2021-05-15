import csv
import numpy as np
from logic import perform_main_logic

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

def main(cash_available):
  with open('papabear-15y-210510.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    rows = parseCsv(spamreader)
    print(rows)
    perform_main_logic(rows, cash_available)

start_cash = 1000 # dollars
main(start_cash)