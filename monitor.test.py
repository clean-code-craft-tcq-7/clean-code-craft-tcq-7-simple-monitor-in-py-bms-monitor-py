import unittest
from monitor import vitals_ok


class MonitorTest(unittest.TestCase):
    def test_not_ok_when_any_vital_out_of_range(self):
        self.assertTrue(vitals_ok(98.1, 70, 98,80,100,15))
        self.assertFalse(vitals_ok(103, 102, 70,80,100,15))
        self.assertFalse(vitals_ok(98,80,70,60,50,17))
        

if __name__ == '__main__':
  unittest.main()
