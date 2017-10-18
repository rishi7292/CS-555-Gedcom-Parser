import unittest
import US19
import sqlite3

class US19Test(unittest.TestCase):

    def test_firstCousins(self):

        
        self.assertIn('@I14@',US19.chk)

        

if __name__ == '__main__':
    unittest.main()