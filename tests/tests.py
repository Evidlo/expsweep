#!/usr/bin/env python3

import unittest
import expsweep
import pandas as pd

class Tests(unittest.TestCase):

    def test_combination_experiment(self):

        global exp
        def exp(a, b, c):
            return {'sum': a + b + c}

        result = expsweep.combination_experiment(
            exp,
            a=[1, 2, 3, 4],
            b=[1, 2, 3, 4],
            c=[1, 2, 3, 4]
        )

        # check that the number of rows is right and that summation is correct
        self.assertEqual(len(result), 64)
        summed_equal = result[['a', 'b', 'c']].sum(axis=1) == result['sum']
        self.assertTrue(summed_equal.all())

    def test_combination_merging(self):
        global exp
        def exp(a, b, c):
            return {'sum1': a + b + c, 'sum2': a + b}

        result = expsweep.combination_experiment(
            exp,
            a=[1, 2, 3, 4],
            b=[1, 2, 3, 4],
            c=[1, 2, 3, 4],
            category_name='method',
            value_name='sum'
        )

        # check for added category column
        self.assertTrue('method' in result.columns)

        # check that the number of rows is right and that summation is correct
        self.assertEqual(len(result), 2 * 64)

        sum1_rows = result[result['method'] == 'sum1']
        summed_equal = sum1_rows[['a', 'b', 'c']].sum(axis=1) == sum1_rows['sum']
        self.assertTrue(summed_equal.all())

        sum2_rows = result[result['method'] == 'sum2']
        summed_equal = sum2_rows[['a', 'b']].sum(axis=1) == sum2_rows['sum']
        self.assertTrue(summed_equal.all())

    def test_merge_columns(self):
        table = pd.DataFrame({
            'method1': [18.748, 20.657, 19.405, 19.793, 18.116],
            'method2': [23.263, 24.003, 22.212, 22.463, 22.382]
        })

        table2 = expsweep.merge_columns(table, ['method1', 'method2'], 'method', 'snr')

        self.assertEqual(len(table2), 10)

if __name__ == '__main__':
    unittest.main()
