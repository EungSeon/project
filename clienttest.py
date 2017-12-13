import bluetooth
import thread
import time
import RPi.GPIO as GPIO
import threading

# Device Name
DeviceName1 = "LED"
DeviceName2 = "FAN"
DeviceName3 = "CAR"

# Port Setting
LED = 7
FAN_EN = 31
FAN_Input1 = 33
FAN_Input2 = 35
CAR_Front_EN = 29
CAR_Front_Input1 = 23
CAR_Front_Input2 = 21
CAR_Behind_EN = 13
CAR_Behind_Input1 = 19
CAR_Behind_Input2 = 15
charging_station = 5

# sortdata function converts string about bluetooth data to list 
def sortdata(data):
    global device_signal_list
    global i
    a = 0
    deviceNum = len(data)   # Length of data variable is the number of device

    if i == 0:
        print "The Number of Device is %d" %deviceNum
        while a < deviceNum:
            k = int(data[a])
            device_signal_list.append(k)
            a += 1
        i += 1
    else:
        while a < deviceNum:
            k = int(data[a])
            device_signal_list[a] = k
            a += 1

# controller class sets devices in motion
class Controller():
    def led(self, deviceName, led_port, signal_led):
        self.deviceName = deviceName
        self.led_port = led_port
        self.signal_led = signal_led

        if self.signal_led == 1:
            GPIO.output(self.led_port, GPIO.HIGH)
        else:
            GPIO.output(self.led_port, GPIO.LOW)
        return

    def fan(self, deviceName, fan_en_port, fan_input1_port, fan_input2_port, signal_fan):
        self.deviceName = deviceName
        self.fan_en_port = fan_en_port
        self.fan_input1_port = fan_input1_port
        self.fan_input2_port = fan_input2_port
        self.signal_fan = signal_fan

        if self.signal_fan == 1:
            GPIO.output(self.fan_en_port, GPIO.HIGH)
            GPIO.output(self.fan_input1_port, GPIO.LOW)
            GPIO.output(self.fan_input2_port, GPIO.HIGH)
        else:
            GPIO.output(self.fan_en_port, GPIO.LOW)
            GPIO.output(self.fan_input1_port, GPIO.LOW)
            GPIO.output(self.fan_input2_port, GPIO.HIGH)
        return

    def car(self, deviceName, car_front_en_port, car_front_input1_port, car_front_input2_port, car_behind_en_port, car_behind_input1_port, car_behind_input2_port, charging_station_port, signal_car):
        self.deviceName = deviceName
        self.car_front_en_port = car_front_en_port
        self.car_front_input1_port = car_front_input1_port
        self.car_front_input2_port = car_front_input2_port
        self.car_behind_en_port = car_behind_en_port
        self.car_behind_input1_port = car_behind_input1_port
        self.car_behind_input2_port = car_behind_input2_port
        self.charging_station_port = charging_station_port
        self.signal_car = signal_car

        if self.signal_car == 1:
            GPIO.output(self.car_front_en_port, GPIO.HIGH)
            GPIO.output(self.car_front_input1_port, GPIO.LOW)
            GPIO.output(self.car_front_input2_port, GPIO.HIGH)
            GPIO.output(self.car_behind_en_port, GPIO.HIGH)
            GPIO.output(self.car_behind_input1_port, GPIO.LOW)
            GPIO.output(self.car_behind_input2_port, GPIO.HIGH)
            GPIO.output(self.charging_station_port, GPIO.LOW)
        else:
            GPIO.output(self.car_front_en_port, GPIO.LOW)
            GPIO.output(self.car_front_input1_port, GPIO.LOW)
            GPIO.output(self.car_front_input2_port, GPIO.HIGH)
            GPIO.output(self.car_behind_en_port, GPIO.LOW)
            GPIO.output(self.car_behind_input1_port, GPIO.LOW)
            GPIO.output(self.car_behind_input2_port, GPIO.HIGH)
            GPIO.output(self.charging_station_port, GPIO.HIGH)
    
# FND class controls 7-segment
class FND():
    # Port setting(7-segment)
    def __init__(self):
        self.fndc0 = 40
        self.fndc1 = 24
        self.fndc2 = 22
        self.fndc3 = 12
        self.fnda = 16
        self.fndb = 26
        self.fndc = 37
        self.fndd = 36
        self.fnde = 32
        self.fndf = 18
        self.fndg = 38
        self.position = 0
        self.c0 = 0
        self.c1 = 0
        self.c2 = 0
        self.c3 = 0

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.fndc0, GPIO.OUT)
        GPIO.setup(self.fndc1, GPIO.OUT)
        GPIO.setup(self.fndc2, GPIO.OUT)
        GPIO.setup(self.fndc3, GPIO.OUT)
        GPIO.setup(self.fnda, GPIO.OUT)
        GPIO.setup(self.fndb, GPIO.OUT)
        GPIO.setup(self.fndc, GPIO.OUT)
        GPIO.setup(self.fndd, GPIO.OUT)
        GPIO.setup(self.fnde, GPIO.OUT)
        GPIO.setup(self.fndf, GPIO.OUT)
        GPIO.setup(self.fndg, GPIO.OUT)
        
    # Clear 7-segment - display 0000
    def Clear(self):
        GPIO.output(self.fnda, GPIO.LOW)
        GPIO.output(self.fndb, GPIO.LOW)
        GPIO.output(self.fndc, GPIO.LOW)
        GPIO.output(self.fndd, GPIO.LOW)
        GPIO.output(self.fnde, GPIO.LOW)
        GPIO.output(self.fndf, GPIO.LOW)
        GPIO.output(self.fndg, GPIO.LOW)

    # Display Number
    def Val_0(self):
        GPIO.output(self.fnda, GPIO.HIGH)
        GPIO.output(self.fndb, GPIO.HIGH)
        GPIO.output(self.fndc, GPIO.HIGH)
        GPIO.output(self.fndd, GPIO.HIGH)
        GPIO.output(self.fnde, GPIO.HIGH)
        GPIO.output(self.fndf, GPIO.HIGH)
        GPIO.output(self.fndg, GPIO.LOW)
    def Val_1(self):
        GPIO.output(self.fnda, GPIO.LOW)
        GPIO.output(self.fndb, GPIO.HIGH)
        GPIO.output(self.fndc, GPIO.HIGH)
        GPIO.output(self.fndd, GPIO.LOW)
        GPIO.output(self.fnde, GPIO.LOW)
        GPIO.output(self.fndf, GPIO.LOW)
        GPIO.output(self.fndg, GPIO.LOW)
    def Val_2(self):
        GPIO.output(self.fnda, GPIO.HIGH)
        GPIO.output(self.fndb, GPIO.HIGH)
        GPIO.output(self.fndc, GPIO.LOW)
        GPIO.output(self.fndd, GPIO.HIGH)
        GPIO.output(self.fnde, GPIO.HIGH)
        GPIO.output(self.fndf, GPIO.LOW)
        GPIO.output(self.fndg, GPIO.HIGH)
    def Val_3(self):
        GPIO.output(self.fnda, GPIO.HIGH)
        GPIO.output(self.fndb, GPIO.HIGH)
        GPIO.output(self.fndc, GPIO.HIGH)
        GPIO.output(self.fndd, GPIO.HIGH)
        GPIO.output(self.fnde, GPIO.LOW)
        GPIO.output(self.fndf, GPIO.LOW)
        GPIO.output(self.fndg, GPIO.HIGH)
    def Val_4(self):
        GPIO.output(self.fnda, GPIO.LOW)
        GPIO.output(self.fndb, GPIO.HIGH)
        GPIO.output(self.fndc, GPIO.HIGH)
        GPIO.output(self.fndd, GPIO.LOW)
        GPIO.output(self.fnde, GPIO.LOW)
        GPIO.output(self.fndf, GPIO.HIGH)
        GPIO.output(self.fndg, GPIO.HIGH)
    def Val_5(self):
        GPIO.output(self.fnda, GPIO.HIGH)
        GPIO.output(self.fndb, GPIO.LOW)
        GPIO.output(self.fndc, GPIO.HIGH)
        GPIO.output(self.fndd, GPIO.HIGH)
        GPIO.output(self.fnde, GPIO.LOW)
        GPIO.output(self.fndf, GPIO.HIGH)
        GPIO.output(self.fndg, GPIO.HIGH)
    def Val_6(self):
        GPIO.output(self.fnda, GPIO.HIGH)
        GPIO.output(self.fndb, GPIO.LOW)
        GPIO.output(self.fndc, GPIO.HIGH)
        GPIO.output(self.fndd, GPIO.HIGH)
        GPIO.output(self.fnde, GPIO.HIGH)
        GPIO.output(self.fndf, GPIO.HIGH)
        GPIO.output(self.fndg, GPIO.HIGH)
    def Val_7(self):
        GPIO.output(self.fnda, GPIO.HIGH)
        GPIO.output(self.fndb, GPIO.HIGH)
        GPIO.output(self.fndc, GPIO.HIGH)
        GPIO.output(self.fndd, GPIO.LOW)
        GPIO.output(self.fnde, GPIO.LOW)
        GPIO.output(self.fndf, GPIO.LOW)
        GPIO.output(self.fndg, GPIO.LOW)
    def Val_8(self):
        GPIO.output(self.fnda, GPIO.HIGH)
        GPIO.output(self.fndb, GPIO.HIGH)
        GPIO.output(self.fndc, GPIO.HIGH)
        GPIO.output(self.fndd, GPIO.HIGH)
        GPIO.output(self.fnde, GPIO.HIGH)
        GPIO.output(self.fndf, GPIO.HIGH)
        GPIO.output(self.fndg, GPIO.HIGH)
    def Val_9(self):
        GPIO.output(self.fnda, GPIO.HIGH)
        GPIO.output(self.fndb, GPIO.HIGH)
        GPIO.output(self.fndc, GPIO.HIGH)
        GPIO.output(self.fndd, GPIO.HIGH)
        GPIO.output(self.fnde, GPIO.LOW)
        GPIO.output(self.fndf, GPIO.HIGH)
        GPIO.output(self.fndg, GPIO.HIGH)

    # Clear 7-segment - display nothing
    def Clear_C(self):
        GPIO.output(self.fndc0, GPIO.HIGH)
        GPIO.output(self.fndc1, GPIO.HIGH)
        GPIO.output(self.fndc2, GPIO.HIGH)
        GPIO.output(self.fndc3, GPIO.HIGH)

    # ON each digit
    def View(self, position):
        if position == 0:
            GPIO.output(self.fndc0, GPIO.LOW)
        elif position == 1:
            GPIO.output(self.fndc1, GPIO.LOW)
        elif position == 2:
            GPIO.output(self.fndc2, GPIO.LOW)
        elif position == 3:
            GPIO.output(self.fndc3, GPIO.LOW)

    def Value(self, position, val):
        self.Clear_C()
        if val == 0:
            self.Val_0()
        elif val == 1:
            self.Val_1()
        elif val == 2:
            self.Val_2()
        elif val == 3:
            self.Val_3()
        elif val == 4:
            self.Val_4()
        elif val == 5:
            self.Val_5()
        elif val == 6:
            self.Val_6()
        elif val == 7:
            self.Val_7()
        elif val == 8:
            self.Val_8()
        elif val == 9:
            self.Val_9()
        self.View(position)

    def fndview(self):
        if self.position == 0:
            self.Value(0, self.c0)
        elif self.position == 1:
            self.Value(1, self.c1)
        elif self.position == 2:
            self.Value(2, self.c2)
        else:
            self.Value(3, self.c3)
            self.position = 0
            return
        self.position = self.position + 1

def thread_segment(aa):
    segment = FND()
    while True:
        global digit0
        global digit1
        global digit2
        global digit3

        segment.c0 = digit0
        segment.c1 = digit1
        segment.c2 = digit2
        segment.c3 = digit3

        segment.fndview()
        time.sleep(0.001)
        
# Main 
if __name__ == '__main__':
    digit0 = 0
    digit1 = 0
    digit2 = 0
    digit3 = 0
    
    GPIO.setmode(GPIO.BOARD)
    device_signal_list = []
    i = 0
    aa = 10
    
    # Bluetooth Connection
    client_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    blport = 3
    bd_addr = "B8:27:EB:15:09:34"       # Server's address
    client_sock.connect((bd_addr, blport))
    
    start = client_sock.recv(1024)
    print start
    client_sock.send('The connection with the client succeeded')
    
    # Device set
    Device1 = Controller()
    Device2 = Controller()
    Device3 = Controller()

    # GPIO setup
    GPIO.setwarnings(False)
    GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(FAN_EN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(FAN_Input1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(FAN_Input2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(CAR_Front_EN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(CAR_Front_Input1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(CAR_Front_Input2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(CAR_Behind_EN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(CAR_Behind_Input1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(CAR_Behind_Input2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(charging_station, GPIO.OUT, initial=GPIO.HIGH)
    
    th = threading.Thread(target=thread_segment, args=(aa,))
    th.start()
    
    while True:
        data = client_sock.recv(1024)
        client_sock.send('Get data')
        sortdata(data)
        
        print '-'*30
        print 'string data :', data
        print 'list data :', device_signal_list
        print "Device's State"
        if device_signal_list[0] == 1:
            print '%s : ON' %DeviceName1
        else:
            print '%s : OFF' %DeviceName1

        if device_signal_list[1] == 1:
            print '%s : ON' %DeviceName2
        else:
            print '%s : OFF' %DeviceName2

        if device_signal_list[2] == 1:
            print '%s : ON' %DeviceName3
        else:
            print '%s : OFF' %DeviceName3
            
        # energy sort
        energy_str = client_sock.recv(1024)
        client_sock.send('Get energy')
        energy = int(energy_str)

        
        if energy >= 1000:
            digit0 = int(energy_str[3])
            digit1 = int(energy_str[2])
            digit2 = int(energy_str[1])
            digit3 = int(energy_str[0])
        elif energy < 1000 and energy >= 100:
            digit0 = int(energy_str[2])
            digit1 = int(energy_str[1])
            digit2 = int(energy_str[0])
            digit3 = 0
        elif energy < 100 and energy >= 10:
            digit0 = int(energy_str[1])
            digit1 = int(energy_str[0])
            digit2 = 0
            digit3 = 0
        elif energy <= 0:
            digit0 = 0
            digit1 = 0
            digit2 = 0
            digit3 = 0
            print 'There is no energy'

        print 'Amount of energy :', energy_str 
        
        Device1.led(DeviceName1, LED, device_signal_list[0])
        Device2.fan(DeviceName2, FAN_EN, FAN_Input1, FAN_Input2, device_signal_list[1])
        Device3.car(DeviceName3, CAR_Front_EN, CAR_Front_Input1, CAR_Front_Input2, CAR_Behind_EN, CAR_Behind_Input1, CAR_Behind_Input2, charging_station, device_signal_list[2])

