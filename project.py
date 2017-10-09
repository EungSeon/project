import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
LED = 11            # LED 연결 핀번호
signal_LED = 10     # LED 동작여부 핀번호
FAN = 12            # FAN 연결 핀번호
signal_FAN = 13     # FAN 동작여부 핀번호
PWMA = 14           # PWM신호 발생 핀번호

# 가상화된 디바이스 LED를 동작시키고 동작시간(데이터)을 반환
def controller_led(LED, signal_LED):
    GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(signal_LED, GPIO.IN)
    
    signal = GPIO.input(signal_LED)
    start_time = time.time()
    
    while(signal == 1):
        GPIO.output(LED, GPIO.HIGH)
        signal = GPIO.input(signal_LED)        
    end_time = time.time()
    GPIO.output(LED, GPIO.LOW)

    time = end_time - start_time

    return time

# 가상화된 디바이스 선풍기(모터를 이용한)를 동작시키고 동작시간(데이터)을 반환
def controller_fan(FAN, signal_FAN, PWMA):
    GPIO.setup(FAN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(PWMA, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(signal_FAN, GPIO.IN)

    duty_ratio = 10
    
    signal = GPIO.input(signal_FAN)
    p = GPIO.PWM(PWMA, 100)
    p.start(0)
    start_time = time.time()

    while(signal == 1):
        GPIO.output(FAN, GPIO.HIGH)
        
        for pw in range(0, 101, duty_ratio):
            p.ChangeDutyCycle(pw)

        signal = GPIO.input(signal_FAN)
    end_time = time.time()
    GPIO.output(FAN, GPIO.LOW)

    time = end_time - start_time

    return time
    

# 다른 디바이스 - 아직 미정
def controller_device3:


# 반환된 데이터를 리스트에 저장 - 분석은 차후 배울 간단한 머신 러닝을 사용할 예정
def collectdata:
    LED_data = []
    FAN_data = []
    device_data = []

# 분석하고 그에 따른 필요한 output을 return
def analysis:

    
    
    
    
    
