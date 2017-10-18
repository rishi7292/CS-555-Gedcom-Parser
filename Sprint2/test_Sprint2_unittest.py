import unittest
import US10
import US11


class TestSprint2(unittest.TestCase):

    def test_notinlist(self):
        self.assertNotIn('@I29@',US11.check_list)
        self.assertNotIn('@I14@',US10.under_age)
    def test_inlist(self):
        self.assertIn('@I4@',US10.under_age)
        self.assertIn('@I27@',US11.check_list)

if __name__ == 'main':
    unittest.main()
