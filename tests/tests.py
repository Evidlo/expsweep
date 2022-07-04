#!/usr/bin/env python3

import unittest
import expsweep
import pandas as pd

class Tests(unittest.TestCase):

    def test_experiment(self):

        global exp
        def exp(a, b, c):
            return {'sum': a + b + c}

        mc = expsweep.experiment(
            exp,
            a=[1, 2, 3, 4],
            b=[1, 2, 3, 4],
            c=[1, 2, 3, 4]
        )

        # check that the number of rows is right and that summation is correct
        self.assertEqual(len(mc), 64)
        summed_equal = mc[['a', 'b', 'c']].sum(axis=1) == mc['sum']
        self.assertTrue(summed_equal.all())

    def test_experiment_merging(self):
        global exp
        def exp(a, b, c):
            return {'sum1': a + b + c, 'sum2': a + b}

        mc = expsweep.experiment(
            exp,
            a=[1, 2, 3, 4],
            b=[1, 2, 3, 4],
            c=[1, 2, 3, 4],
            # category_name='method',
            # value_name='sum'
            merge=True,
        )

        # check for added category column
        self.assertTrue('experiment' in mc.columns)

        # check that the number of rows is right and that summation is correct
        self.assertEqual(len(mc), 2 * 64)

        sum1_rows = mc[mc['experiment'] == 'sum1']
        summed_equal = sum1_rows[['a', 'b', 'c']].sum(axis=1) == sum1_rows['result']
        self.assertTrue(summed_equal.all())

        sum2_rows = mc[mc['experiment'] == 'sum2']
        summed_equal = sum2_rows[['a', 'b']].sum(axis=1) == sum2_rows['result']
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
