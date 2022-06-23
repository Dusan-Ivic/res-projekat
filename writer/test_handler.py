import unittest
from handler import check_input_data_branching
from handler import check_input_data

class TestHandler(unittest.TestCase):   
    def test_wrong_input(self):
        self.assertRaises(TypeError, check_input_data,"11")
        self.assertRaises(TypeError, check_input_data,"openings")

    def test_right_input(self):
        self.assertEqual(check_input_data("open"),"open")
        self.assertEqual(check_input_data("close"),"close")
        self.assertEqual(check_input_data("choose"),"choose")

    def test_wrong_input_choice(self):
        self.assertRaises(TypeError, check_input_data_branching,-12)
        self.assertRaises(TypeError, check_input_data_branching,999)
        self.assertRaises(TypeError, check_input_data_branching,"a")
        self.assertRaises(TypeError, check_input_data_branching,"asdasd")
       
    def test_wrong_input_choice_ok(self):
        self.assertEqual(check_input_data_branching(0),0)
        self.assertEqual(check_input_data_branching(2),2)
   
if __name__ == '__main__':
    unittest.main()