import unittest
from unittest import mock 
from unittest.mock import patch
import replicator_receiver
from replicator_receiver import ReplicatorReceiver
from data.delta_cd import DeltaCD


class TestReceiver(unittest.TestCase):
    
    def test_dataset_fetch_bad(self):
        self.assertRaises(TypeError, replicator_receiver.ReplicatorReceiver.get_dataset,self,"klsjldsjkf")
        self.assertRaises(TypeError, replicator_receiver.ReplicatorReceiver.get_dataset,self,"eees")
        self.assertRaises(TypeError, replicator_receiver.ReplicatorReceiver.get_dataset,self,1)

    def test_dataset_fetch_good(self):
        self.assertEqual(replicator_receiver.ReplicatorReceiver.get_dataset(self,"CODE_ANALOG"),1)
        self.assertEqual(replicator_receiver.ReplicatorReceiver.get_dataset(self,"CODE_DIGITAL"),1)
        self.assertEqual(replicator_receiver.ReplicatorReceiver.get_dataset(self,"CODE_CUSTOM"),2)
        self.assertEqual(replicator_receiver.ReplicatorReceiver.get_dataset(self,"CODE_LIMITSET"),2)
        self.assertEqual(replicator_receiver.ReplicatorReceiver.get_dataset(self,"CODE_SINGLENODE"),3)
        self.assertEqual(replicator_receiver.ReplicatorReceiver.get_dataset(self,"CODE_MULTIPLENODE"),3)
        self.assertEqual(replicator_receiver.ReplicatorReceiver.get_dataset(self,"CODE_CONSUMER"),4)
        self.assertEqual(replicator_receiver.ReplicatorReceiver.get_dataset(self,"CODE_SOURCE"),4)
   
    
if __name__ == '__main__':
    unittest.main()