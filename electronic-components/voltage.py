import RPi.GPIO as GPIO
from adc import AnalogToDigital


class VoltageDetector:

    def __init__(self, adc: AnalogToDigital, inputVoltage:float):
        self.adc = adc
        self.inputVoltage = inputVoltage

    def read_voltage(self, adnum):
        voltage = self.adc.read_number(adnum)
        return voltage * (self.inputVoltage / 1024) * 5
