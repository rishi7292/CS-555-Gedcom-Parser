# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 14:47:15 2017

@author: rishi
"""

import unittest
import US04

class Test_UserStory(unittest.TestCase):
    print ("Executing Test Case for UserStory 04")
    def test_isValid(self):
        self.assertTrue(US04.check('10 JUL 2006','20 MAY 2005'))

if __name__ == '__main__':
    unittest.main()