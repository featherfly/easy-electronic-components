import smbus
import time

class GY906:
    I2CADDR = 0x5a
    MLX90614TOBJ1 = 0x07
    readWaitTime = 0.1
    def __init__(self, busNo):
        #Get I2C bus
        self.bus = smbus.SMBus(busNo)
    
    def getTemp(self):
        self.bus.write_byte(self.I2CADDR, self.MLX90614TOBJ1)
        time.sleep(self.readWaitTime)
        data = self.bus.read_word_data(self.I2CADDR, self.MLX90614TOBJ1)
        temp = data * 0.02
        temp -= 273.15
        return temp