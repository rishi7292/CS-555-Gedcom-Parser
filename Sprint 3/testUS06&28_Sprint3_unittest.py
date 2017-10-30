import unittest
import US06
import US28
def list(id_check):
    if id_check in US28.final_sib_list:
        return US28.final_sib_dict[id_check]
    else:
        return -1

class TestSprint3(unittest.TestCase):

    def test_notinlist(self):
        self.assertNotIn('@I29@',US06.check_list)

    def test_inlist(self):
        self.assertIn('@I38@',US06.check_list)

    def test_equal(self):
        self.assertEqual(list('@I5@'),25)
        self.assertEqual(list('@I12@'),30)

    def test_notequal(self):
        self.assertNotEqual(list("@I7@"),100)

if __name__ == 'main':
    unittest.main()
