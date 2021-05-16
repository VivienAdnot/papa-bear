import numpy as np

def get_3_max_values(arr):
  np_array = np.array(arr)
  sorted_index_array = np.argsort(np_array)
  sorted_array = np_array[sorted_index_array]

  indices = sorted_index_array[-3:]
  result = sorted_array[-3:]
  return indices, result

# compute arithmetic average of array
def average(*args):
  return round(sum(args) / len(args), 2)

# compute variation between 2 prices
# https://www.schoolmouv.fr/formules/taux-de-variation/formule-ses
def compute_percentage_gain(value_current, value_previous):
  return round((value_current - value_previous) / value_previous * 100, 2)
