import sys
sys.path.append("..")
from sounder import Speaker
import RPi.GPIO as GPIO
import time
import sys

if __name__ == '__main__':
    s = Speaker()
    sound = s.vocalize("十九八七六五四三二一")    
    if len(sys.argv) == 2:
        gap = int(sys.argv[1])
        s.set_wordgap(gap)
    try:
        for i in range(10000):
            time.sleep(1)
            if i == 5:
                sound.stop()
                print("sound stop")
                break
    finally:
        sound.stop()