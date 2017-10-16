# import RPi.GPIO as GPIO
import time

# GPIO.setmode(GPIO.BOARD)
LED = 11            # LED 연결 핀번호
signal_LED = 10     # LED 동작여부 핀번호
FAN = 12            # FAN 연결 핀번호
signal_FAN = 13     # FAN 동작여부 핀번호
PWMA = 14           # PWM신호 발생 핀번호

import input1
a = input1.controller()

time_led = a.led(LED, signal_LED)
time_fan = a.fan(FAN, signal_FAN, PWMA)
time_device = a.device3()

print(time_led)
print(time_fan)
print(time_device)

import process
d = process.collectdata()
d.data()

import output
result = output.analysis()
result.analysis() 
