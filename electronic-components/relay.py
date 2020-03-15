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

import smbus
import warnings
import threading

class PCF8754Relay:
    # 打开 /dev/i2c-传入参数
    I2CADDR = 0x20
    I2CADDR2 = 0x21
    def __init__(self, busNo):
        #Get I2C bus
        self.bus = smbus.SMBus(busNo)
        self.channels = [0b1,0b1,0b1,0b1,0b1,0b1,0b1,0b1]
        self.lock = threading.RLock()

    def checkChannel(self, channel:int):
        if channel > 7:
            channel = 7
        if channel < 0:
            channel = 0
        return 7 - channel

    def operate(self, channels, action):        
        self.lock.acquire()
        try:            
            for channel in channels:
                self.channels[self.checkChannel(channel)] = action
            # strValue = "%d%d%d%d%d%d%d%d"%(self.channels[0],self.channels[1],self.channels[2],self.channels[3],self.channels[4],self.channels[5],self.channels[6],self.channels[7])
            # writeValue = int(strValue, 2)
            writeValue = 0
            for index, channel in enumerate(self.channels):
                writeValue += channel << 7 - index
            self.bus.write_byte(self.I2CADDR, writeValue)
        except OSError:
            self.bus.write_byte(self.I2CADDR2, writeValue)
            warnings.warn("self.I2CADDR2=",self.I2CADDR2)
        finally:
            self.lock.release()

    def open(self, *args):
        argslen = len(args)
        if argslen == 0:
            warnings.warn("no arg, do nothing")
        else:
            self.operate(args, 0)
        

    def close(self, *args):
        argslen = len(args)
        if argslen == 0:
            warnings.warn("no arg, do nothing")
        else:
            self.operate(args, 1)

    def closeAll(self):
        self.bus.write_byte(self.I2CADDR, 255)

    def openAll(self):
        self.bus.write_byte(self.I2CADDR, 0)