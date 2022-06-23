import unittest
import writer
from unittest.mock import patch
from unittest.mock import MagicMock




class TestWriter(unittest.TestCase):    
    def test_index_over(self):
        self.assertRaises(Exception, writer.Writer.get_code,self,11)
        self.assertRaises(Exception, writer.Writer.get_code,self,900)

    def test_index_under(self):
        self.assertRaises(Exception, writer.Writer.get_code,self,-2)
        self.assertRaises(Exception, writer.Writer.get_code,self,-4)

    def test_index_ok(self):
        self.assertEqual(writer.Writer.get_code(self, 0),"CODE_ANALOG")
        self.assertEqual(writer.Writer.get_code(self, 3),"CODE_LIMITSET")

if __name__ == '__main__':
    unittest.main()