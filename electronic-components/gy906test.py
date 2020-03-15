import smbus
import time
from gy906 import GY906
if __name__ == '__main__':
    gy = GY906(1)
    try:
        while True:
            print(gy.getTemp())
            time.sleep(1)
    except KeyboardInterrupt:        
        print("Measurement stopped by User")