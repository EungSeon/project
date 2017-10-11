import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
LED = 11            # LED 연결 핀번호
signal_LED = 10     # LED 동작여부 핀번호
FAN = 12            # FAN 연결 핀번호
signal_FAN = 13     # FAN 동작여부 핀번호
PWMA = 14           # PWM신호 발생 핀번호

import input1

input1.controller_led(LED, signal_LED)
input1.controller_fan(FAN, signal_FAN, PWMA)
input1.controller_device3()

import process

process.collectdata()

import output

output.analysis()
