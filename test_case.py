import simplex
import unittest


class TestOfMaximumFunction(unittest.TestCase):
    def maximum_profit(self):
        self.assertEqual(simplex.simplex([6, 6], [[2, 0], [1, 2], [1, 4]], [20, 37, 30])[1], 90.0)

    def variant_4(self):
        self.assertEqual(simplex.simplex([11, 9], [[2, 3], [3, 1], [0, 1]], [20, 37, 30])[1], 110.0)


if __name__ == '__main__':
    unittest.main()
