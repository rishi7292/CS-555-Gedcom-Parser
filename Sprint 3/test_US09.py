# Author: Pranit Kulkarni
import unittest
import US09

class UserStoryTest(unittest.TestCase):

    def test_isInvalid(self):
        self.assertTrue(US09.hasInvalidBirth("@I8@"))



if __name__ == '__main__':
    unittest.main()