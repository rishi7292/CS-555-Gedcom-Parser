import unittest
import US37


class US37Test(unittest.TestCase):

    def test_recent_deaths(self):

        
        self.assertTrue(US37.deadRecently('@I30@'))

        

if __name__ == '__main__':
    unittest.main()