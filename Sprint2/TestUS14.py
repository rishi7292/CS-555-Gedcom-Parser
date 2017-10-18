import unittest
import US14
import sqlite3

class US14Test(unittest.TestCase):

    def test_noOfSiblings(self):

        siblings = US14.noOfSiblings("@F2@")
        self.assertGreaterEqual(siblings,5)

        

if __name__ == '__main__':
    unittest.main()