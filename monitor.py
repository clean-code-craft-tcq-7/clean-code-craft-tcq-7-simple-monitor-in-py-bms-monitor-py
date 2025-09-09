
from time import sleep
import sys


from time import sleep
import sys

# Ask user for language input
LANGUAGE = input("Choose language (EN for English, DE for German): ").strip().upper()
if LANGUAGE not in ["EN", "DE"]:
    print("Invalid language selected. Defaulting to English.")
    LANGUAGE = "EN"

# Message translations
MESSAGES = {
    "Vitals OK": {
        "EN": "Vitals are OK!",
        "DE": "Vitalwerte sind in Ordnung!"
    },
    "Out of Range": {
        "EN": "{} is out of range!",
        "DE": "{} liegt außerhalb des Bereichs!"
    }
}

def blinkoutput():
    for i in range(6):
        print('\r* ', end='')
        sys.stdout.flush()
        sleep(1)
        print('\r *', end='')
        sys.stdout.flush()
        sleep(1)

def vitals_ok(temperature, pulseRate, spo2, bloodsugar, bloodpressure, respiratoryrate):
    RetOk = True
    vitals = {
        "Temperature": (temperature, 95, 102),
        "Pulse Rate": (pulseRate, 60, 100),
        "SpO2": (spo2, 90, 100),
        "Blood Sugar": (bloodsugar, 70, 110),
        "Blood Pressure": (bloodpressure, 90, 150),
        "Respiratory rate": (respiratoryrate, 12, 20)
    }

    for name, (value, min, max) in vitals.items():
        if not (min <= value <= max):
            print("\n" + MESSAGES["Out of Range"][LANGUAGE].format(name))
            RetOk = False

    if RetOk:
        print(MESSAGES["Vitals OK"][LANGUAGE])

    blinkoutput()
    return RetOk
