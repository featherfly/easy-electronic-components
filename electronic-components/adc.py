from electronic_modules.base import ElectronicModule

class AnalogToDigital(ElectronicModule):

    def read_number(self, adcnum):
        return -1

import RPi.GPIO as GPIO

class MCP3008(AnalogToDigital):
    def __init__(self, spiclk = 11, spimiso = 9, spimosi = 10, spics = 8, gpioMode = GPIO.BCM):
        self.spiclk = spiclk
        self.spimiso = spimiso
        self.spimosi = spimosi
        self.spics = spics
        self.gpioMode = gpioMode

    def setup(self): # port init
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # set up the SPI interface pins
        GPIO.setup(self.spimosi, GPIO.OUT)
        GPIO.setup(self.spimiso, GPIO.IN)
        GPIO.setup(self.spiclk, GPIO.OUT)
        GPIO.setup(self.spics, GPIO.OUT)
        pass
    
    def cleanup(self): #port cleanup
        GPIO.cleanup(self.spimosi, self.spimiso, self.spiclk, self.spics)

    # read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
    def read_number(self, adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        GPIO.output(self.spics, True)

        GPIO.output(self.spiclk, False)  # start clock low
        GPIO.output(self.spics, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
            if (commandout & 0x80):
                GPIO.output(self.spimosi, True)
            else:
                GPIO.output(self.spimosi, False)
            commandout <<= 1
            GPIO.output(self.spiclk, True)
            GPIO.output(self.spiclk, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
            GPIO.output(self.spiclk, True)
            GPIO.output(self.spiclk, False)
            adcout <<= 1
            if (GPIO.input(self.spimiso)):
                adcout |= 0x1

        GPIO.output(self.spics, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout