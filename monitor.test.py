import unittest
from monitor import vitals_ok

class MonitorTest(unittest.TestCase):
    def setUp(self):
        self.normal_vitals = {
            'temperature': 98.6,
            'pulseRate': 75,
            'spo2': 95,
            'blood_sugar': 90,
            'blood_pressure': 120,
            'respiratory_rate': 16
        }

    def assertVitals(self, expected, **overrides):
        vitals = self.normal_vitals.copy()
        vitals.update(overrides)
        self.assertEqual(vitals_ok(**vitals), expected)

    def test_all_vitals_ok(self):
        self.assertVitals(True)

    def test_temperature_critical(self):
        self.assertVitals(False, temperature=103)
        self.assertVitals(False, temperature=94)

    def test_pulse_rate_out_of_range(self):
        self.assertVitals(False, pulseRate=50)
        self.assertVitals(False, pulseRate=110)

    def test_spo2_out_of_range(self):
        self.assertVitals(False, spo2=85)

    def test_blood_sugar_out_of_range(self):
        self.assertVitals(False, blood_sugar=60)
        self.assertVitals(False, blood_sugar=115)

    def test_blood_pressure_out_of_range(self):
        self.assertVitals(False, blood_pressure=85)
        self.assertVitals(False, blood_pressure=160)

    def test_respiratory_rate_out_of_range(self):
        self.assertVitals(False, respiratory_rate=10)
        self.assertVitals(False, respiratory_rate=25)

if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()

