# Author: Pranit Kulkarni
import unittest
import US08

class UserStoryTest(unittest.TestCase):

    def test_isBirthInvalid(self):
        self.assertTrue(US08.isBirthInvalid("@I8@"))

if __name__ == '__main__':
    unittest.main()