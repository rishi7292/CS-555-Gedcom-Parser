# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 13:51:50 2017

@author: rishi
"""

import unittest
import US23

class Test_UserStory(unittest.TestCase):
    print ("Executing Test Case for UserStory 23")
    def test_isValid(self):
        self.assertFalse(US23.check("Rishi Targaryen"))

if __name__ == '__main__':
    unittest.main()