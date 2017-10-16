# import RPi.GPIO as GPIO
import time

class controller():
    def led(self, LED, signal_LED):
        self.LED = LED
        self.signal_LED = signal_LED
        t = time.time()
        print("controller class에서 LED를 동작하는 함수 입니다.")

        return t

        """
        GPIO.setup(self.LED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.signal_LED, GPIO.IN)

        signal = GPIO.input(self.signal_LED)
        start_time = time.time()

        while(signal == 1):
            GPIO.output(self.LED, GPIO.HIGH)
            signal = GPIO.input(self.signal_LED)
        end_time = time.time()
        GPIO.output(self.LED, GPIO.LOW)

        time = end_time - srart_time
        return time
        """

    def fan(self, FAN, signal_FAN, PWMA):
        self.FAN = FAN
        self.signal_FAN = signal_FAN
        self.PWMA = PWMA

        t = time.time()
        print("controller class에서 FAN을 동작하는 함수 입니다.")

        return t

        """
        GPIO.setup(self.FAN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.PWMA, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.signal_FAN, GPIO.IN)

        duty_ratio = 10
    
        signal = GPIO.input(signal_FAN)
        p = GPIO.PWM(self.PWMA, 100)
        p.start(0)
        start_time = time.time()

        while(signal == 1):
            GPIO.output(self.FAN, GPIO.HIGH)
        
            for pw in range(0, 101, duty_ratio):
                p.ChangeDutyCycle(pw)

            signal = GPIO.input(self.signal_FAN)
        end_time = time.time()
        GPIO.output(self.FAN, GPIO.LOW)

        time = end_time - start_time
        return time
        """

    def device3(self):
        t = time.time()
        print("controller class에서 device를 동작하는 함수 입니다.")

        return t

"""
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
def controller_device3():
"""
