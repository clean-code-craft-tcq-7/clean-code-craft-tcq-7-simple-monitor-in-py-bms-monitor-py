
import sys

from time import sleep
from enum import Enum, auto


class Language(Enum):
   ENGLISH = auto()
   GERMAN = auto()


language = Language.GERMAN


def __display_vital_alert(val, msg):
  print(msg)
  for _ in range(val):
      print('\r* ', end='')
      sys.stdout.flush()
      sleep(1)
      print('\r *', end='')
      sys.stdout.flush()
      sleep(1)


def __is_vital_ok(name, value, min_val, max_val):
  if value < min_val or value > max_val:
    __display_vital_alert(6, f'{name} is out of range!')
    return False
  return True


def is_temperature_ok(temperature):
  return __is_vital_ok('Temperature', temperature, 95, 102)


def is_pulse_rate_ok(pulse_rate):
  return __is_vital_ok('Pulse Rate', pulse_rate, 60, 100)


def is_spo2_ok(spo2):
  return __is_vital_ok('Oxygen Saturation', spo2, 90, 150)


# this api will get deprecated in next few releases
def vitals_ok(temperature, pulse_rate, spo2):
  return (
    is_temperature_ok(temperature) and
    is_pulse_rate_ok(pulse_rate) and
    is_spo2_ok(spo2)
  )


# =========================================================
# Refactored code with OOP approach
# =========================================================

class Vital:
    def __init__(self, name, min_value, max_value):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value

    def is_normal(self, value: float) -> bool:
        return self.min_value <= value <= self.max_value

    def check(self, value: float):
        global language
        if self.is_normal(value):
            print(f"[OK] {self.name}: {value}")
        else:
            # Import at module level to avoid name mangling issues
            import sys
            module = sys.modules[__name__]
            display_alert = getattr(module, '__display_vital_alert')
            msg = "is out of range"
            if language == Language.GERMAN:
               msg = "liegt außerhalb des zulässigen Bereichs"
            display_alert(1, f'{self.name} {msg}!')


# Registry of vitals (so user doesn’t need to know min/max)
VITALS = {
  "temperature": Vital("temperature", 95, 102),
  "oxygen-rate": Vital("oxygen-rate", 90, 150),
  "pulse-rate": Vital("pulse-rate", 60, 100),
  "blood-sugar": Vital("blood-sugar", 70, 110),
  "blood-pressure": Vital("blood-pressure", 90, 150),
  "respiration-rate": Vital("respiration-rate", 12, 20)
}


def check_vitals(user_values: dict):
    for vital_name, value in user_values.items():
        vital = VITALS.get(vital_name)
        if not vital:
            msg = "[ERROR] Unknown vital"
            if language == Language.GERMAN:
                msg = "[FEHLER] Unbekannte Vital"
            print(f"{msg}: {vital_name}")
            continue
        vital.check(value)


if __name__ == "__main__":  # pragma: no cover
    user_vitals = {
        "temperature": 104,
        "oxygen-rate": 85,
        "pulse-rate": 120,
        "blood-sugar": 90,
        "blood-pressure": 160,
        "respiration-rate": 15
    }
    check_vitals(user_vitals)
