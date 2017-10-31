# Author: Pranit Kulkarni
import unittest
import US18

class UserStoryTest(unittest.TestCase):

    def test_isInvalid(self):
        self.assertTrue(US18.isMarriedToASibbling("@I5@"))



if __name__ == '__main__':
    unittest.main()