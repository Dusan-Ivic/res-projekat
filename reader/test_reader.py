import unittest
import reader

class TestReader(unittest.TestCase):    
    def test_deadband(self):
        self.assertEqual(reader.Reader.calculate_deadband(self,11,7),36.36363636363637)
        self.assertEqual(reader.Reader.calculate_deadband(self,4,20),400.0)
        self.assertEqual(reader.Reader.calculate_deadband(self,9,2),77.77777777777779)
        self.assertEqual(reader.Reader.calculate_deadband(self,-9,2),-122.22222222222223)

    
if __name__ == '__main__':
    unittest.main()