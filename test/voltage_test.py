# def main():
#     mcp = MCP3008()
#     mcp.setup()
#     time.sleep(2)
#     print("will detect voltage")
#     while True:
#         ad_value = mcp.readadc(0)
#         print("***********")
#         print(" ad_value is: {0}".format(ad_value))
#         print("***********")
#         print(' ')
#         time.sleep(0.5)

# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         pass
# GPIO.cleanup()
import sys
sys.path.append("..")
from electronic_modules.voltage import VoltageDetector
from electronic_modules.adc import MCP3008
import RPi.GPIO as GPIO
import time
import sys

def get_ad_num():
    try:
        print("输入模拟输入针脚号（0-7）")
        adNum=int(input())
        if adNum > 7:
            adNum = 7
        if adNum < 0:
            adNum = 0
        return adNum
    except ValueError:
        return get_ad_num()
def get_voltage():
    try:
        print("输入电压值,不超过24")
        voltage=int(input())
        if voltage > 24:
            voltage = 24
        if voltage < 0:
            voltage = 0
        return voltage
    except ValueError:
        return get_voltage()

arglen = len(sys.argv) - 1
inputVoltage = 5
if arglen == 1:
    inputVoltage = float(sys.argv[1])

def main():
    mcp = MCP3008()
    v = VoltageDetector(mcp, inputVoltage)
    mcp.setup()
    time.sleep(2)
    print("will detect voltage")
    while True:
        voltage = v.read_voltage(get_ad_num())
        print("***********")
        print(" Voltage is: " + str("%.2f"%voltage)+"V")
        print("***********")
        print(' ')
        time.sleep(0.5)

if __name__ =='__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()