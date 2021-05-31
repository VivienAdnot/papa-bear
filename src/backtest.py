import csv
import numpy as np
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from logic import perform_main_logic
from model.papa_bear_portfolio import PapaBearPortfolio

def create_date_array(start, length):
  return [start + datetime.timedelta(days=(30.4 * i)) for i in range(length)]

start = datetime.date(2007, 1, 1)
dates = create_date_array(start, 176)

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

def main(portfolio, portfolio_value):
  with open('data/papabear-15y-210510.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    rows = parseCsv(spamreader)
    perform_main_logic(rows, portfolio, portfolio_value)
    portfolio.sell_all_at_market()

start_cash = 1000 # dollars
portfolio = PapaBearPortfolio(cash=start_cash)
portfolio_value = []
main(portfolio, portfolio_value)

# plt.figure(figsize=(12,5))
# plt.axhline(start_cash, color="gray") # horizontal gray line

fig, ax = plt.subplots()
locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
ax.grid(True)

ax.plot(dates, portfolio_value)
plt.show()