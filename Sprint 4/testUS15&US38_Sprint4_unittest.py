import unittest
import US15
import US38
def list(id_check):
    if id_check in US15.err:
        return True
    else:
        return False

class TestSprint4(unittest.TestCase):

    def test_notinlist(self):
        self.assertNotIn('Sansa Stark',US38.check_list)

    def test_inlist(self):
        self.assertIn('Lisa Stark',US38.check_list)

    def test_true(self):
        self.assertTrue(list('@F3@'))

    def test_false(self):
        self.assertFalse(list("@F5@"))

if __name__ == 'main':
    unittest.main()
