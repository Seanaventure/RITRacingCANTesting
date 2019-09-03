
import serial
import time


arduinoData = serial.Serial("COM6", 9600)


def led_on():
    arduinoData.write(b'1')  # write(b"1")


def led_off():
    arduinoData.write(b'0')


time.sleep(2)
"""
t = 0
while t < 500000:
    if(t % 10 == 0):
        print(t)
    t += 1
"""

while 1:
    led_on()
    time.sleep(1)
    print("sleep")
    led_off()
    print("on")
    time.sleep(1)