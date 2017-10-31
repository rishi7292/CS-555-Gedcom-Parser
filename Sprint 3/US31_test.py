# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 13:48:52 2017

@author: rishi
"""

import unittest
import US31

class Test_UserStory(unittest.TestCase):
    print ("Executing Test Case for UserStory 31")
    def test_isValid(self):
        self.assertTrue(US31.check(43))

if __name__ == '__main__':
    unittest.main()