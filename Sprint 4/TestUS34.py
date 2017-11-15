import unittest
import US34


class US34Test(unittest.TestCase):

    def test_large_age_differnce(self):

        
        self.assertIn('Brandon Stark',US34.largeDiff)

        

if __name__ == '__main__':
    unittest.main()