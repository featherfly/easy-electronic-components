import RPi.GPIO as GPIO
import time
import sys

class Relay:
    def __init__(self, gpioPort, gpioMode=GPIO.BCM, activeMode=GPIO.LOW):
        self._gpioPort = gpioPort
        self._gpioMode = gpioMode
        self._activeMode = activeMode
        GPIO.setup(self._gpioPort, GPIO.OUT, initial= not activeMode)
    
    def open(self):
        GPIO.output(self._gpioPort, self._activeMode)

    def close(self):
        GPIO.output(self._gpioPort, not self._activeMode)

        
class MulitiChannelsRelay:
    def __init__(self, relays):
        self.relays = relays
        
    def open(self, channelNum):
        self.relays[channelNum].open()

    def close(self,channelNum):
        self.relays[channelNum].close()

    def close_all(self):
        for relay in self.relays:
            relay.close()

from pcf8574 import PCF8754

class PCF8754Relay:
    def __init__(self, busNo=1, activeMode=False, reversed = True):
        #Get I2C bus
        self.pcf8574 = PCF8754(busNo=busNo, reversed=reversed)
        self.activeMode = activeMode;

    def operate(self, channels, action):
        self.pcf8574.operate(self, channels, action)

    def open(self, *args):
        if self.activeMode:
            self.pcf8574.high(args, args)
        else:
            self.pcf8574.low(args, args)

    def close(self, *args):
        if self.activeMode:
            self.pcf8574.low(args, args)
        else:
            self.pcf8574.high(args, args)

    def closeAll(self):
        if self.activeMode:
            self.pcf8574.lowAll()
        else:
            self.pcf8574.highAll()

    def openAll(self):
        if self.activeMode:
            self.pcf8574.highAll()
        else:
            self.pcf8574.lowAll()