import unittest
import US35

class UsesStoryTest(unittest.TestCase):
    def test_bornRecently(self):
        self.assertTrue(US35.bornRecently("Pranit Stark"))

if __name__ == '__main__':
    unittest.main()