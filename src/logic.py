import numpy as np
from utils import get_3_max_values, average, compute_percentage_gain

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
  
  for index, item in enumerate(current_winners_indices):
    # item_index, shares_amount = item
    if item not in new_winners_indices:
      # losers_to_sell.append((index, item))
      losers_to_sell.append(item)

  for index, item in enumerate(new_winners_indices):
    if item not in current_winners_indices:
      # winners_to_buy.append((index, item))
      winners_to_buy.append(item)

  return (losers_to_sell, winners_to_buy)

def buy(cash_available):
  pass

def perform_main_logic(rows, cash_available):
  # record all the history of cash, so we can plot it at the end
  # cash_history = []
  # record all the winners, so we can compute statistics later
  # winners_history = []

  # record all the price history, so we can compute statistics later
  # average_gains_history = []

  # transform prices in gain
  average_gains = compute_average_gains(rows)
  print('average_gains', average_gains)

  current_winners_indices = []

  print('------ loop avg_gain_rows ------')
  for index, row in enumerate(average_gains):
    if (index >= 6):
      print('avg_gains_row_idx', index)
      # print('current_winners_indices before arbitrage', current_winners_indices)
      # print(result[0])
      new_winners_indices, new_average_gains = get_3_max_values(row)
      print('new_winners_indices', new_winners_indices)
      # print('new_average_gains', new_average_gains)
      
      losers_to_sell, winners_to_buy = compute_winners_losers(current_winners_indices, new_winners_indices)
      print('losers_to_sell', losers_to_sell)
      print('winners_to_buy', winners_to_buy)

      current_winners_indices[:] = new_winners_indices
      print('current_winners_indices after arbitrage', current_winners_indices)
  print('------ end loop avg_gain_rows ------')
  # print('winners_history: ', winners_history)