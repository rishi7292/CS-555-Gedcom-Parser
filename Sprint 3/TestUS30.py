import unittest
import US30


class US30Test(unittest.TestCase):

    def test_livingMarried(self):

        
        self.assertIn('@I22@',US30.livingMarried)

        

if __name__ == '__main__':
    unittest.main()