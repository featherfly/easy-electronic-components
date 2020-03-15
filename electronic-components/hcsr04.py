#导入 GPIO库
#from dataclasses import dataclass
import time
import RPi.GPIO as GPIO

#@dataclass
class HCSR04:
    def __init__(self, gpioTrigger:int, gpioEcho:int, gpioMode:int = GPIO.BCM, triggerTime:float=0.00001):
        self.gpioTrigger =  gpioTrigger
        self.gpioEcho = gpioEcho
        self.gpioMode = gpioMode
        self.triggerTime = triggerTime
        #设置 GPIO 模式
        GPIO.setmode(gpioMode)
        #设置 GPIO 的工作方式 (IN / OUT)
        GPIO.setup(gpioTrigger, GPIO.OUT)
        GPIO.setup(gpioEcho, GPIO.IN)
    
    def checkDist(self):
        # 发出触发信号
        # 发送高电平信号到 Trig 引脚
        GPIO.output(self.gpioTrigger, GPIO.HIGH)
        # 持续 10 us 
        time.sleep(self.triggerTime)
        GPIO.output(self.gpioTrigger, GPIO.LOW)
        while not GPIO.input(self.gpioEcho):
            pass
        # 发现高电平时开时计时
        t1 = time.time()
        while GPIO.input(self.gpioEcho):
            pass
        # 高电平结束停止计时
        t2 = time.time()
        #返回距离，单位为厘米
        return (t2-t1) * 34300 / 2    