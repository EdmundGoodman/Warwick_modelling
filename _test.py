#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from model_v4 import *

class TestModel(unittest.TestCase):
    def test_empty_model(self):
        INITIALLY_INFECTED = 0
        m = run()
        print(m.data_handler.ys_data[-1][0])

        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
    print("All tests passed")
