# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 15:03:10 2017

@author: rishi
"""

import unittest
import US39

class Test_UserStory(unittest.TestCase):
    print ("Executing Test Case for UserStory 39")
    def test_isValid(self):
        self.assertTrue(US39.check('30 NOV 2017'))

if __name__ == '__main__':
    unittest.main()