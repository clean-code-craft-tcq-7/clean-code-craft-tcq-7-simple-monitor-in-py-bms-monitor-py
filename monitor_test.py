import pytest
from unittest.mock import patch, call
import monitor
from monitor import vitals_ok, is_temperature_ok, is_pulse_rate_ok, is_spo2_ok, Vital, VITALS, check_vitals, Language


class TestTemperature:
    """Test cases for temperature validation"""

    def test_temperature_within_range(self):
        """Test temperature within valid range (95-102)"""
        assert is_temperature_ok(98.6) is True
        assert is_temperature_ok(95) is True
        assert is_temperature_ok(102) is True
        assert is_temperature_ok(100.5) is True

    def test_temperature_below_range(self):
        """Test temperature below minimum (95)"""
        with patch('monitor.__display_vital_alert') as mock_alert:
            assert is_temperature_ok(94.9) is False
            mock_alert.assert_called_once_with(6, 'Temperature is out of range!')

        with patch('monitor.__display_vital_alert'):
            assert is_temperature_ok(90) is False

    def test_temperature_above_range(self):
        """Test temperature above maximum (102)"""
        with patch('monitor.__display_vital_alert') as mock_alert:
            assert is_temperature_ok(102.1) is False
            mock_alert.assert_called_once_with(6, 'Temperature is out of range!')

        with patch('monitor.__display_vital_alert'):
            assert is_temperature_ok(105) is False

    def test_temperature_boundary_values(self):
        """Test boundary values"""
        assert is_temperature_ok(95.0) is True
        assert is_temperature_ok(102.0) is True

        with patch('monitor.__display_vital_alert'):
            assert is_temperature_ok(94.99999) is False
            assert is_temperature_ok(102.00001) is False

    def test_temperature_type_error(self):
        """Test type errors for temperature"""
        with pytest.raises(TypeError):
            is_temperature_ok("98.6")

        with pytest.raises(TypeError):
            is_temperature_ok(None)

        with pytest.raises(TypeError):
            is_temperature_ok([98.6])


class TestPulseRate:
    """Test cases for pulse rate validation"""

    def test_pulse_rate_within_range(self):
        """Test pulse rate within valid range (60-100)"""
        assert is_pulse_rate_ok(70) is True
        assert is_pulse_rate_ok(60) is True
        assert is_pulse_rate_ok(100) is True
        assert is_pulse_rate_ok(85) is True

    def test_pulse_rate_below_range(self):
        """Test pulse rate below minimum (60)"""
        with patch('monitor.__display_vital_alert') as mock_alert:
            assert is_pulse_rate_ok(59) is False
            mock_alert.assert_called_once_with(6, 'Pulse Rate is out of range!')

        with patch('monitor.__display_vital_alert'):
            assert is_pulse_rate_ok(45) is False

    def test_pulse_rate_above_range(self):
        """Test pulse rate above maximum (100)"""
        with patch('monitor.__display_vital_alert') as mock_alert:
            assert is_pulse_rate_ok(101) is False
            mock_alert.assert_called_once_with(6, 'Pulse Rate is out of range!')

        with patch('monitor.__display_vital_alert'):
            assert is_pulse_rate_ok(120) is False

    def test_pulse_rate_boundary_values(self):
        """Test boundary values"""
        assert is_pulse_rate_ok(60) is True
        assert is_pulse_rate_ok(100) is True

        with patch('monitor.__display_vital_alert'):
            assert is_pulse_rate_ok(59.9) is False
            assert is_pulse_rate_ok(100.1) is False

    def test_pulse_rate_type_error(self):
        """Test type errors for pulse rate"""
        with pytest.raises(TypeError):
            is_pulse_rate_ok("70")

        with pytest.raises(TypeError):
            is_pulse_rate_ok(None)

        with pytest.raises(TypeError):
            is_pulse_rate_ok([70])


class TestSpo2:
    """Test cases for SpO2 validation"""

    def test_spo2_within_range(self):
        """Test SpO2 within valid range (90 and above)"""
        assert is_spo2_ok(95) is True
        assert is_spo2_ok(90) is True
        assert is_spo2_ok(100) is True
        assert is_spo2_ok(99.5) is True
        assert is_spo2_ok(150) is True  # No upper limit

    def test_spo2_below_range(self):
        """Test SpO2 below minimum (90)"""
        with patch('monitor.__display_vital_alert') as mock_alert:
            assert is_spo2_ok(89) is False
            mock_alert.assert_called_once_with(6, 'Oxygen Saturation is out of range!')

        with patch('monitor.__display_vital_alert'):
            assert is_spo2_ok(85) is False

    def test_spo2_boundary_values(self):
        """Test boundary values"""
        assert is_spo2_ok(90.0) is True
        assert is_spo2_ok(90.1) is True

        with patch('monitor.__display_vital_alert'):
            assert is_spo2_ok(89.9) is False

    def test_spo2_type_error(self):
        """Test type errors for SpO2"""
        with pytest.raises(TypeError):
            is_spo2_ok("95")

        with pytest.raises(TypeError):
            is_spo2_ok(None)

        with pytest.raises(TypeError):
            is_spo2_ok([95])


class TestVitalsOk:
    """Test cases for overall vitals validation"""

    def test_all_vitals_ok(self):
        """Test when all vitals are within normal range"""
        assert vitals_ok(98.6, 70, 95) is True
        assert vitals_ok(95, 60, 90) is True
        assert vitals_ok(102, 100, 100) is True

    def test_temperature_not_ok(self):
        """Test when only temperature is out of range"""
        with patch('monitor.__display_vital_alert'):
            assert vitals_ok(94, 70, 95) is False
            assert vitals_ok(103, 70, 95) is False

    def test_pulse_rate_not_ok(self):
        """Test when only pulse rate is out of range"""
        with patch('monitor.__display_vital_alert'):
            assert vitals_ok(98.6, 59, 95) is False
            assert vitals_ok(98.6, 101, 95) is False

    def test_spo2_not_ok(self):
        """Test when only SpO2 is out of range"""
        with patch('monitor.__display_vital_alert'):
            assert vitals_ok(98.6, 70, 89) is False

    def test_multiple_vitals_not_ok(self):
        """Test when multiple vitals are out of range"""
        with patch('monitor.__display_vital_alert'):
            assert vitals_ok(94, 59, 89) is False
            assert vitals_ok(103, 101, 89) is False

    def test_vitals_ok_with_original_test_cases(self):
        """Test with original test cases from the file"""
        with patch('monitor.__display_vital_alert'):
            assert vitals_ok(99, 102, 70) is False  # pulse rate too high

        assert vitals_ok(98.1, 70, 98) is True

    def test_vitals_ok_type_errors(self):
        """Test type errors for vitals_ok function"""
        with pytest.raises(TypeError):
            vitals_ok("98.6", 70, 95)

        with pytest.raises(TypeError):
            vitals_ok(98.6, "70", 95)

        with pytest.raises(TypeError):
            vitals_ok(98.6, 70, "95")

        with pytest.raises(TypeError):
            vitals_ok(None, 70, 95)


class TestEdgeCases:
    """Test edge cases and special scenarios"""

    def test_zero_values(self):
        """Test with zero values"""
        with patch('monitor.__display_vital_alert'):
            assert is_temperature_ok(0) is False
            assert is_pulse_rate_ok(0) is False
            assert is_spo2_ok(0) is False

    def test_negative_values(self):
        """Test with negative values"""
        with patch('monitor.__display_vital_alert'):
            assert is_temperature_ok(-1) is False
            assert is_pulse_rate_ok(-1) is False
            assert is_spo2_ok(-1) is False

    def test_very_large_values(self):
        """Test with very large values"""
        with patch('monitor.__display_vital_alert'):
            assert is_temperature_ok(1000) is False
            assert is_pulse_rate_ok(1000) is False
            assert is_spo2_ok(1000) is False

    def test_float_precision(self):
        """Test with floating point precision"""
        assert is_temperature_ok(95.000001) is True
        assert is_pulse_rate_ok(60.000001) is True
        assert is_spo2_ok(90.000001) is True


# =========================================================
# Tests for the Refactored code with OOP approach
# =========================================================

class TestVital:
    """Test cases for the Vital class"""
    
    def test_vital_initialization(self):
        """Test Vital class initialization"""
        vital = Vital("Temperature", 95, 102)
        assert vital.name == "Temperature"
        assert vital.min_value == 95
        assert vital.max_value == 102
    
    def test_is_normal_within_range(self):
        """Test is_normal method with values within range"""
        vital = Vital("Temperature", 95, 102)
        assert vital.is_normal(98.6) is True
        assert vital.is_normal(95) is True  # boundary
        assert vital.is_normal(102) is True  # boundary
    
    def test_is_normal_outside_range(self):
        """Test is_normal method with values outside range"""
        vital = Vital("Temperature", 95, 102)
        assert vital.is_normal(94.9) is False
        assert vital.is_normal(102.1) is False
    
    @patch('builtins.print')
    def test_check_normal_value(self, mock_print):
        """Test check method with normal value"""
        vital = Vital("Temperature", 95, 102)
        vital.check(98.6)
        mock_print.assert_called_once_with("[OK] Temperature: 98.6")
    
    @patch('monitor.__display_vital_alert')
    def test_check_abnormal_value_english(self, mock_alert):
        """Test check method with abnormal value in English"""
        # Set language to English
        original_lang = monitor.language
        monitor.language = monitor.Language.ENGLISH
        
        vital = Vital("Temperature", 95, 102)
        vital.check(94)
        mock_alert.assert_called_once_with(1, 'Temperature is out of range!')
        
        # Restore original language
        monitor.language = original_lang
    
    @patch('monitor.__display_vital_alert')
    def test_check_abnormal_value_german(self, mock_alert):
        """Test check method with abnormal value in German"""
        # Set language to German
        original_lang = monitor.language
        monitor.language = monitor.Language.GERMAN
        
        vital = Vital("Temperature", 95, 102)
        vital.check(94)
        mock_alert.assert_called_once_with(1, 'Temperature liegt außerhalb des zulässigen Bereichs!')
        
        # Restore original language
        monitor.language = original_lang


class TestVitalsRegistry:
    """Test cases for the VITALS registry"""
    
    def test_vitals_registry_keys(self):
        """Test that all expected vitals are in the registry"""
        expected_vitals = [
            "temperature", "oxygen-rate", "pulse-rate", 
            "blood-sugar", "blood-pressure", "respiration-rate"
        ]
        
        for vital_name in expected_vitals:
            assert vital_name in VITALS
            assert isinstance(VITALS[vital_name], Vital)
    
    def test_vitals_registry_values(self):
        """Test the values in the vitals registry"""
        expected_values = {
            "temperature": ("temperature", 95, 102),
            "oxygen-rate": ("oxygen-rate", 90, 150),
            "pulse-rate": ("pulse-rate", 60, 100),
            "blood-sugar": ("blood-sugar", 70, 110),
            "blood-pressure": ("blood-pressure", 90, 150),
            "respiration-rate": ("respiration-rate", 12, 20)
        }
        
        for key, (name, min_val, max_val) in expected_values.items():
            vital = VITALS[key]
            assert vital.name == name
            assert vital.min_value == min_val
            assert vital.max_value == max_val


class TestCheckVitals:
    """Test cases for the check_vitals function"""
    
    @patch('builtins.print')
    def test_check_vitals_all_normal(self, mock_print):
        """Test check_vitals with all normal values"""
        user_values = {
            "temperature": 98.6,
            "pulse-rate": 70,
            "oxygen-rate": 95
        }
        
        check_vitals(user_values)
        
        expected_calls = [
            call("[OK] temperature: 98.6"),
            call("[OK] pulse-rate: 70"),
            call("[OK] oxygen-rate: 95")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=True)
        assert mock_print.call_count == 3
    
    @patch('builtins.print')
    @patch('monitor.__display_vital_alert')
    def test_check_vitals_some_abnormal(self, mock_alert, mock_print):
        """Test check_vitals with some abnormal values"""
        user_values = {
            "temperature": 98.6,  # normal
            "pulse-rate": 150,    # abnormal (too high)
        }
        
        check_vitals(user_values)
        
        # Check normal value output
        mock_print.assert_any_call("[OK] temperature: 98.6")
        
        # Check abnormal value alerts
        mock_alert.assert_called_once()
        assert mock_alert.call_count == 1
    
    @patch('builtins.print')
    def test_check_vitals_unknown_vital_english(self, mock_print):
        """Test check_vitals with unknown vital signs in English"""
        # Set language to English
        original_lang = monitor.language
        monitor.language = monitor.Language.ENGLISH
        
        user_values = {
            "temperature": 98.6,
            "unknown-vital": 50,
        }
        
        check_vitals(user_values)
        
        # Check that normal vital is processed
        mock_print.assert_any_call("[OK] temperature: 98.6")
        
        # Check that unknown vital generates error message
        mock_print.assert_any_call("[ERROR] Unknown vital: unknown-vital")
        
        # Restore original language
        monitor.language = original_lang
    
    @patch('builtins.print')
    def test_check_vitals_unknown_vital_german(self, mock_print):
        """Test check_vitals with unknown vital signs in German"""
        # Set language to German
        original_lang = monitor.language
        monitor.language = monitor.Language.GERMAN
        
        user_values = {
            "temperature": 98.6,
            "unknown-vital": 50,
        }
        
        check_vitals(user_values)
        
        # Check that normal vital is processed
        mock_print.assert_any_call("[OK] temperature: 98.6")
        
        # Check that unknown vital generates German error message
        mock_print.assert_any_call("[FEHLER] Unbekannte Vital: unknown-vital")
        
        # Restore original language
        monitor.language = original_lang
    
    @patch('builtins.print')
    def test_check_vitals_empty_dict(self, mock_print):
        """Test check_vitals with empty dictionary"""
        check_vitals({})
        mock_print.assert_not_called()
    
    @patch('builtins.print')
    def test_check_vitals_boundary_values(self, mock_print):
        """Test check_vitals with boundary values"""
        user_values = {
            "temperature": 95,          # minimum boundary
            "pulse-rate": 100,          # maximum boundary
            "blood-pressure": 90,       # minimum boundary
        }
        
        check_vitals(user_values)
        
        expected_calls = [
            call("[OK] temperature: 95"),
            call("[OK] pulse-rate: 100"),
            call("[OK] blood-pressure: 90")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=True)
        assert mock_print.call_count == 3


class TestLanguageFeatures:
    """Test cases for language switching functionality"""
    
    def test_language_enum_values(self):
        """Test Language enum has correct values"""
        assert hasattr(monitor.Language, 'ENGLISH')
        assert hasattr(monitor.Language, 'GERMAN')
        assert monitor.Language.ENGLISH != monitor.Language.GERMAN
    
    def test_default_language_is_german(self):
        """Test that default language is German"""
        assert monitor.language == monitor.Language.GERMAN
    
    @patch('builtins.print')
    def test_language_switching(self, mock_print):
        """Test switching between languages"""
        original_lang = monitor.language
        
        # Test German
        monitor.language = monitor.Language.GERMAN
        user_values = {"unknown-vital": 50}
        check_vitals(user_values)
        mock_print.assert_called_with("[FEHLER] Unbekannte Vital: unknown-vital")
        
        mock_print.reset_mock()
        
        # Test English
        monitor.language = monitor.Language.ENGLISH
        check_vitals(user_values)
        mock_print.assert_called_with("[ERROR] Unknown vital: unknown-vital")
        
        # Restore original language
        monitor.language = original_lang


class TestMainExecution:
    """Test cases for main execution block"""
    
    @patch('builtins.print')
    @patch('monitor.__display_vital_alert')
    def test_main_execution_scenario(self, mock_alert, mock_print):
        """Test main execution scenario with expected data"""
        # Test the same data that would be used in main execution
        expected_vitals = {
            "temperature": 104,      # abnormal (too high)
            "oxygen-rate": 85,       # abnormal (too low)
            "pulse-rate": 120,       # abnormal (too high)
            "blood-sugar": 90,       # normal
            "blood-pressure": 160,   # abnormal (too high)
            "respiration-rate": 15   # normal
        }
        
        check_vitals(expected_vitals)
        
        # Check that normal values generate OK messages
        mock_print.assert_any_call("[OK] blood-sugar: 90")
        mock_print.assert_any_call("[OK] respiration-rate: 15")
        
        # Check that abnormal values trigger alerts
        # Should have 4 alerts for abnormal values
        assert mock_alert.call_count == 4
        
        # Total print calls should be 2 (for OK messages)
        assert mock_print.call_count == 2


class TestIntegration:
    """Integration tests combining multiple features"""
    
    @patch('builtins.print')
    @patch('monitor.__display_vital_alert')
    def test_mixed_scenario_with_language(self, mock_alert, mock_print):
        """Test mixed normal/abnormal values with language features"""
        original_lang = monitor.language
        monitor.language = monitor.Language.GERMAN
        
        user_values = {
            "temperature": 98.6,        # normal
            "pulse-rate": 150,          # abnormal
            "unknown-vital": 100,       # unknown
        }
        
        check_vitals(user_values)
        
        # Check normal value
        mock_print.assert_any_call("[OK] temperature: 98.6")
        
        # Check German error message for unknown vital
        mock_print.assert_any_call("[FEHLER] Unbekannte Vital: unknown-vital")
        
        # Check that alert was called for abnormal value
        assert mock_alert.call_count == 1
        
        # Restore original language
        monitor.language = original_lang
    
    def test_vital_registry_consistency(self):
        """Test that all registry vitals work correctly"""
        for vital_name, vital in VITALS.items():
            # Test that each vital can be used
            assert isinstance(vital, Vital)
            assert vital.name == vital_name
            
            # Test boundary values
            assert vital.is_normal(vital.min_value) is True
            assert vital.is_normal(vital.max_value) is True
            assert vital.is_normal(vital.min_value - 0.1) is False
            assert vital.is_normal(vital.max_value + 0.1) is False


if __name__ == '__main__':
    pytest.main([__file__])
