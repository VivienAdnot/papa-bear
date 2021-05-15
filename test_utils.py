import unittest
from numpy.testing import assert_array_equal

from utils import average, compute_percentage_gain, get_3_max_values

class TestUtils(unittest.TestCase):

  def test_average(self):
    self.assertEqual(average(1, 3, 5), 3.0)
    self.assertEqual(average(1, 3, 5, 8), 4.25)

  def test_compute_percentage_gain(self):
    value_current = 100
    value_previous = 50
    result = compute_percentage_gain(value_current, value_previous)
    self.assertEqual(result, 100.0)

  def test_get_3_winners(self):
    values = [-3.89, -59.99, 2.83, 7.53, 13.58, -9.29, 4.6, 10.48, 6.79, -5.8, 9.01]
    largest_indices, largest_values = get_3_max_values(values)
    assert_array_equal(largest_values, [9.01, 10.48, 13.58])
    assert_array_equal(largest_indices, [10, 7, 4])