import smbus
import logging
import threading

class PCF8754:
    # 打开 /dev/i2c 传入参数
    I2CADDR = 0x20
    I2CADDR2 = 0x21
    def __init__(self, busNo=1, reversed=False):
        #Get I2C bus
        self.bus = smbus.SMBus(busNo)
        self.reversed = reversed
        self.channels = [0b1,0b1,0b1,0b1,0b1,0b1,0b1,0b1]
        self.lock = threading.RLock()

    def checkChannel(self, channel:int):
        if channel > 7:
            channel = 7
        if channel < 0:
            channel = 0
        if self.reversed:
            return 7 - channel
        else:
            return channel

    def operate(self, channels, action):        
        self.lock.acquire()
        try:            
            for channel in channels:
                self.channels[self.checkChannel(channel)] = action
            writeValue = 0
            for index, channel in enumerate(self.channels):
                writeValue += channel << 7 - index
            self.bus.write_byte(self.I2CADDR, writeValue)
        except OSError:
            self.bus.write_byte(self.I2CADDR2, writeValue)
            logging.warn("self.I2CADDR2=",self.I2CADDR2)
        finally:
            self.lock.release()

    def high(self, *args):
        argslen = len(args)
        if argslen == 0:
            logging.warn("no arg, do nothing")
        else:
            self.operate(args, 1)
        

    def low(self, *args):
        argslen = len(args)
        if argslen == 0:
            logging.warn("no arg, do nothing")
        else:
            self.operate(args, 0)

    def highAll(self):
        self.bus.write_byte(self.I2CADDR, 255)

    def lowAll(self):
        self.bus.write_byte(self.I2CADDR, 0)