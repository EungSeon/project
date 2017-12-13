import bluetooth
import threading
import math
import time
import datetime
import Tkinter
import RPi.GPIO as GPIO
import subprocess

blport = 3
server_addr = "B8:27:EB:15:09:34"
# Amount of energy
energy_amount = 5000
energy_amount_str = str(energy_amount)
money = 35690

# Device Name
DeviceName1 = "LED"
DeviceName2 = "FAN"
DeviceName3 = "CAR"

device1_signal = 0
device2_signal = 0
device3_signal = 0

contract_signal = 0

data_lst = ['0', '0', '0']
 
operating_lst = []
time_lst = []
energy_lst = []

device1_start_time = 0.0
device1_dp_start_time = ""
device2_start_time = 0.0
device2_dp_start_time = ""
device3_start_time = 0.0
device3_dp_start_time = ""


# collect data function collects data of devices and returns the energy consumption
def collectdata(DeviceName, start, end, op_time):
    global operating_lst        # Collect data at list
    global time_lst             # Collect operating time at list
    global energy_lst           # Collect amount of energy at list
    
    if DeviceName == "LED":
        energy_amount = round(op_time, 1) * 30
    elif DeviceName == "FAN":
        energy_amount = round(op_time, 1) * 60
    else:
        energy_amount = round(op_time, 1) * 300
    
    k = "ON : " + start + ", OFF : " + end + ", Operating time : %.1f seconds, Energy consumption : %d, Device = %s" %(op_time, int(energy_amount), DeviceName)
    time = round(op_time, 1)

    # Save data, the type is list
    operating_lst.append(k)
    time_lst.append(time)
    energy_lst.append(energy_amount)

    length = len(operating_lst)
    i = 0
    
    while i<length:
        print operating_lst[i]
        i = i+1
        

    return energy_amount

def information_led():
    global operating_lst
    global time_lst
    global energy_lst

    print ''
    length = len(operating_lst)
    i = 0
    time = 0.0
    energy = 0.0
    while i<length:
        data = operating_lst[i]
        device = data[-3] + data[-2] + data[-1]
        if device == 'LED':
            print operating_lst[i]
            time = time + time_lst[i]
            energy = energy + energy_lst[i]
            
        i = i+1
    print 'Total operating time of LED : %.2f seconds' %time
    print 'Total energy consumption of LED : %d' %int(energy)
    print ''

def information_fan():
    global operating_lst
    global time_lst
    global energy_lst

    print ''
    length = len(operating_lst)
    i = 0
    time = 0.0
    energy = 0.0
    while i<length:
        data = operating_lst[i]
        device = data[-3] + data[-2] + data[-1]
        if device == 'FAN':
            print operating_lst[i]
            time = time + time_lst[i]
            energy = energy + energy_lst[i]
        i = i+1
    print 'Total operating time of FAN : %.2f seconds' %time
    print 'Total energy consumption of FAN : %d' %int(energy)
    print ''

def information_car():
    global operating_lst
    global time_lst
    global energy_lst

    print ''
    length = len(operating_lst)
    i = 0
    time = 0.0
    energy = 0.0
    while i<length:
        data = operating_lst[i]
        device = data[-3] + data[-2] + data[-1]
        if device == 'CAR':
            print operating_lst[i]
            time = time + time_lst[i]
            energy = energy + energy_lst[i]
        i = i+1
    print 'Total operating time of CAR : %.2f seconds' %time
    print 'Total energy consumption of CAR : %d' %int(energy)
    print ''




def push_device1():
    global device1_signal
    global data_lst                 # Datalist to send client via bluetooth
    global device1_start_time       # Start time of Device1
    global device1_dp_start_time    # Start time of Device1(Display)
    global energy_amount
    global energy_amount_str
    global contract_signal
    global conn
    global addr
    global money
    
    if device1_signal == 0:
        # Device1 ON
        label1.config(text = 'ON')
        data_lst[0] = '1'
        device1_signal = 1
        print '-'*30
        print DeviceName1 + ' is ON'

        # Send data of current device state
        data = data_lst[0]+data_lst[1]+data_lst[2]
        print "Data : " + data

        conn.send(data)
        print 'Data transfer completed'
        words = conn.recv(1024)
        
        conn.send(energy_amount_str)
        words = conn.recv(1024)

        # Start time
        device1_start_time = time.time()
        device1_dp_start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    elif device1_signal == 1:
        # Device1 OFF
        label1.config(text = 'OFF')
        data_lst[0] = '0'
        device1_signal = 0
        print '-'*30
        print DeviceName1 + ' is OFF'
    
        # Send data of current device state
        data = data_lst[0]+data_lst[1]+data_lst[2]
        print "Data : " + data
    
        conn.send(data)      
        print 'Data transfer completed'
        words = conn.recv(1024)
        print '-'*30

        # End time
        device1_end_time = time.time()
        operating_time = device1_end_time - device1_start_time
        device1_dp_end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        energy = collectdata(DeviceName1, device1_dp_start_time, device1_dp_end_time, operating_time)

        energy_amount = energy_amount - int(energy)
        
        if contract_signal == 0 and energy_amount <0:
            print ''
            print 'There is no energy'
            print 'You need energy trading'
            print "You can't drive devices"
            print ''
            
            # Run energy transaction file
            pipe = subprocess.Popen("node trans.js", shell = True, stdout = subprocess.PIPE).stdout

            while True:
                f = open("nodetopython.txt", 'r')
                line = f.readline()
                if line == '0\n':
                    f.close()
                else:
                    print 'Energy trading completed'
                    f = open("nodetopython.txt", 'r')
                    lines = f.readlines()
                    add_energy = lines[0]
                    money_paid = lines[1]
                    add_energy = int(add_energy)
                    money_paid = int(money_paid)
                    energy_amount = energy_amount + add_energy
                    print 'Money before payment : %d$' %money
                    money = money - money_paid
                    print 'Money after payment : %d$' %money
                    f.close()

                    # Reset txt file is used to next energy trading
                    f = open("nodetopython.txt", 'w')
                    f.write('0\n')
                    f.write('0')
                    f.close()
                    break
                
        elif contract_signal == 0 and energy_amount < 2000 and energy_amount >= 0:
            contract_signal = 1
            print ''
            print 'There is not enough energy'
            print 'You need energy trading'
            print ''
            
            # Run energy transaction file
            pipe = subprocess.Popen("node trans.js", shell = True, stdout = subprocess.PIPE).stdout

            f = open("nodetopython.txt", 'r')
            line = f.readline()
            if line == '0\n':
                f.close()
            else:
                print 'Energy trading completed'
                contract_signal = 0
                f = open("nodetopython.txt", 'r')
                lines = f.readlines()
                add_energy = lines[0]
                money_paid = lines[1]
                add_energy = int(add_energy)
                money_paid = int(money_paid)
                energy_amount = energy_amount + add_energy
                print 'Money before payment : %d$' %money
                money = money - money_paid
                print 'Money after payment : %d$' %money
                f.close()
                
                # Reset txt file is used to next energy trading
                f = open("nodetopython.txt", 'w')
                f.write('0\n')
                f.write('0')
                f.close()
                
        elif contract_signal == 1 and energy_amount < 2000 and energy_amount >= 0:
            print ''
            print 'There is not enough energy'
            print 'You need energy trading'
            print ''

            f = open("nodetopython.txt", 'r')
            line = f.readline()
            if line == '0\n':
                f.close()
            else:
                print 'Energy trading completed'
                contract_signal = 0
                f = open("nodetopython.txt", 'r')
                lines = f.readlines()
                add_energy = lines[0]
                money_paid = lines[1]
                add_energy = int(add_energy)
                money_paid = int(money_paid)
                energy_amount = energy_amount + add_energy
                print 'Money before payment : %d$' %money
                money = money - money_paid
                print 'Money after payment : %d$' %money
                f.close()
                
                # Reset txt file is used to next energy trading
                f = open("nodetopython.txt", 'w')
                f.write('0\n')
                f.write('0')
                f.close()
                
        elif contract_signal == 1 and energy_amount < 0:
            print ''
            print 'There is no energy'
            print 'You need energy trading'
            print "You can't drive devices"
            print ''

            while True:
                f = open("nodetopython.txt", 'r')
                line = f.readline()
                if line == '0\n':
                    f.close()
                else:
                    print 'Energy trading completed'
                    contract_signal = 0
                    f = open("nodetopython.txt", 'r')
                    lines = f.readlines()
                    add_energy = lines[0]
                    money_paid = lines[1]
                    add_energy = int(add_energy)
                    money_paid = int(money_paid)
                    energy_amount = energy_amount + add_energy
                    print 'Money before payment : %d$' %money
                    money = money - money_paid
                    print 'Money after payment : %d$' %money
                    f.close()

                    # Reset txt file is used to next energy trading
                    f = open("nodetopython.txt", 'w')
                    f.write('0\n')
                    f.write('0')
                    f.close()
                    break

        energy_amount_str = str(energy_amount)
        conn.send(energy_amount_str)
        words = conn.recv(1024)
        
        # Energy display
        print 'Amount of Energy : %d' %energy_amount
        
def push_device2():
    global device2_signal
    global data_lst                 # Datalist to send client via bluetooth
    global device2_start_time       # Start time of Device2
    global device2_dp_start_time    # Start time of Device2(Display)
    global energy_amount
    global energy_amount_str
    global contract_signal
    global conn
    global addr
    global money
    
    if device2_signal == 0:
        # Device2 ON
        label2.config(text = 'ON')
        data_lst[1] = '1'
        device2_signal = 1
        print '-'*30
        print DeviceName2 + ' is ON'

        # Send data of current device state
        data = data_lst[0]+data_lst[1]+data_lst[2]
        print "Data : " + data
    
        conn.send(data)
        print 'Data transfer completed'
        words = conn.recv(1024)
        
        conn.send(energy_amount_str)
        words = conn.recv(1024)

        # Start time
        device2_start_time = time.time()
        device2_dp_start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    elif device2_signal == 1:
        # Device2 OFF
        label2.config(text = 'OFF')
        data_lst[1] = '0'
        device2_signal = 0
        print '-'*30
        print DeviceName2 + ' is OFF'
    
        # Send data of current device state
        data = data_lst[0]+data_lst[1]+data_lst[2]
        print "Data : " + data
    
        conn.send(data)
        print 'Data transfer completed'
        words = conn.recv(1024)
        print '-'*30

        # End time
        device2_end_time = time.time()
        operating_time = device2_end_time - device2_start_time
        device2_dp_end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        energy = collectdata(DeviceName2, device2_dp_start_time, device2_dp_end_time, operating_time)
        energy_amount = energy_amount - int(energy)
        if contract_signal == 0 and energy_amount <0:
            print ''
            print 'There is no energy'
            print 'You need energy trading'
            print "You can't drive devices"
            print ''
            
            # Run energy transaction file
            pipe = subprocess.Popen("node trans.js", shell = True, stdout = subprocess.PIPE).stdout

            while True:
                f = open("nodetopython.txt", 'r')
                line = f.readline()
                if line == '0\n':
                    f.close()
                else:
                    print 'Energy trading completed'
                    f = open("nodetopython.txt", 'r')
                    lines = f.readlines()
                    add_energy = lines[0]
                    money_paid = lines[1]
                    add_energy = int(add_energy)
                    money_paid = int(money_paid)
                    energy_amount = energy_amount + add_energy
                    print 'Money before payment : %d$' %money
                    money = money - money_paid
                    print 'Money after payment : %d$' %money
                    f.close()

                    # Reset txt file is used to next energy trading
                    f = open("nodetopython.txt", 'w')
                    f.write('0\n')
                    f.write('0')
                    f.close()
                    break
                
        elif contract_signal == 0 and energy_amount < 2000 and energy_amount >= 0:
            contract_signal = 1
            print ''
            print 'There is not enough energy'
            print 'You need energy trading'
            print ''

            # Run energy transaction file
            pipe = subprocess.Popen("node trans.js", shell = True, stdout = subprocess.PIPE).stdout

            f = open("nodetopython.txt", 'r')
            line = f.readline()
            if line == '0\n':
                f.close()
            else:
                print 'Energy trading completed'
                contract_signal = 0
                f = open("nodetopython.txt", 'r')
                lines = f.readlines()
                add_energy = lines[0]
                money_paid = lines[1]
                add_energy = int(add_energy)
                money_paid = int(money_paid)
                energy_amount = energy_amount + add_energy
                print 'Money before payment : %d$' %money
                money = money - money_paid
                print 'Money after payment : %d$' %money
                f.close()

                # Reset txt file is used to next energy trading
                f = open("nodetopython.txt", 'w')
                f.write('0\n')
                f.write('0')
                f.close()
                
        elif contract_signal == 1 and energy_amount < 2000 and energy_amount >= 0:
            print ''
            print 'There is not enough energy'
            print 'You need energy trading'
            print ''

            f = open("nodetopython.txt", 'r')
            line = f.readline()
            if line == '0\n':
                f.close()
            else:
                print 'Energy trading completed'
                contract_signal = 0
                f = open("nodetopython.txt", 'r')
                lines = f.readlines()
                add_energy = lines[0]
                money_paid = lines[1]
                add_energy = int(add_energy)
                money_paid = int(money_paid)
                energy_amount = energy_amount + add_energy
                print 'Money before payment : %d$' %money
                money = money - money_paid
                print 'Money after payment : %d$' %money
                f.close()

                # Reset txt file is used to next energy trading
                f = open("nodetopython.txt", 'w')
                f.write('0\n')
                f.write('0')
                f.close()
                
        elif contract_signal == 1 and energy_amount < 0:
            print ''
            print 'There is no energy'
            print 'You need energy trading'
            print "You can't drive device"
            print ''
            
            while True:
                f = open("nodetopython.txt", 'r')
                line = f.readline()
                if line == '0\n':
                    f.close()
                else:
                    print 'Energy trading completed'
                    contract_signal = 0
                    f = open("nodetopython.txt", 'r')
                    lines = f.readlines()
                    add_energy = lines[0]
                    money_paid = lines[1]
                    add_energy = int(add_energy)
                    money_paid = int(money_paid)
                    energy_amount = energy_amount + add_energy
                    print 'Money before payment : %d$' %money
                    money = money - money_paid
                    print 'Money after payment : %d$' %money
                    f.close()

                    # Reset txt file is used to next energy trading
                    f = open("nodetopython.txt", 'w')
                    f.write('0\n')
                    f.write('0')
                    f.close()
                    break
                
        energy_amount_str = str(energy_amount)
        conn.send(energy_amount_str)
        words = conn.recv(1024)
        
        # Energy display
        print 'Amount of Energy : %d' %energy_amount

def push_device3():
    global device3_signal
    global data_lst                 # Datalist to send client via bluetooth
    global device3_start_time       # Start time of Device3
    global device3_dp_start_time    # Start time of Device3(Display)
    global energy_amount
    global energy_amount_str
    global contract_signal
    global conn
    global addr
    global money
    
    if device3_signal == 0:
        # Device3 ON
        label3.config(text = 'ON')
        data_lst[2] = '1'
        device3_signal = 1
        print '-'*30
        print DeviceName3 + ' is ON'

        # Send data of current device state
        data = data_lst[0]+data_lst[1]+data_lst[2]
        print "Data : " + data
    
        conn.send(data)
        print 'Data transfer completed'
        words = conn.recv(1024)
        
        conn.send(energy_amount_str)
        words = conn.recv(1024)

        # Start time
        device3_start_time = time.time()
        device3_dp_start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    elif device3_signal == 1:
        # Device3 OFF
        label3.config(text = 'OFF')
        data_lst[2] = '0'
        device3_signal = 0
        print '-'*30
        print DeviceName3 + ' is OFF'
    
        # Send data of current device state
        data = data_lst[0]+data_lst[1]+data_lst[2]
        print "Data : " + data
    
        conn.send(data)
        print 'Data transfer completed'
        words = conn.recv(1024)
        print '-'*30

        # End time
        device3_end_time = time.time()
        operating_time = device3_end_time - device3_start_time
        device3_dp_end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        energy = collectdata(DeviceName3, device3_dp_start_time, device3_dp_end_time, operating_time)
        energy_amount = energy_amount - int(energy)

        if contract_signal == 0 and energy_amount <0:
            print ''
            print 'There is no energy'
            print 'You need energy trading'
            print "You can't drive devices"
            print ''
            
            # Run energy transaction file
            pipe = subprocess.Popen("node trans.js", shell = True, stdout = subprocess.PIPE).stdout

            while True:
                f = open("nodetopython.txt", 'r')
                line = f.readline()
                if line == '0\n':
                    f.close()
                else:
                    print 'Energy trading completed'
                    f = open("nodetopython.txt", 'r')
                    lines = f.readlines()
                    add_energy = lines[0]
                    money_paid = lines[1]
                    add_energy = int(add_energy)
                    money_paid = int(money_paid)
                    energy_amount = energy_amount + add_energy
                    print 'Money before payment : %d$' %money
                    money = money - money_paid
                    print 'Money after payment : %d$' %money
                    f.close()

                    # Reset txt file is used to next energy trading
                    f = open("nodetopython.txt", 'w')
                    f.write('0\n')
                    f.write('0')
                    f.close()
                    break
                
        elif contract_signal == 0 and energy_amount < 2000 and energy_amount >= 0:
            contract_signal = 1
            print ''
            print 'There is not enough energy'
            print 'You need energy trading'
            print ''

            # Run energy transaction file
            pipe = subprocess.Popen("node trans.js", shell = True, stdout = subprocess.PIPE).stdout

            f = open("nodetopython.txt", 'r')
            line = f.readline()
            if line == '0\n':
                f.close()
            else:
                print 'Energy trading completed'
                contract_signal = 0
                f = open("nodetopython.txt", 'r')
                lines = f.readlines()
                add_energy = lines[0]
                money_paid = lines[1]
                add_energy = int(add_energy)
                money_paid = int(money_paid)
                energy_amount = energy_amount + add_energy
                print 'Money before payment : %d$' %money
                money = money - money_paid
                print 'Money after payment : %d$' %money
                f.close()
                
                # Reset txt file is used to next energy trading
                f = open("nodetopython.txt", 'w')
                f.write('0\n')
                f.write('0')
                f.close()
                
        elif contract_signal == 1 and energy_amount < 2000 and energy_amount >= 0:
            print ''
            print 'There is not enough energy'
            print 'You need energy trading'
            print ''

            f = open("nodetopython.txt", 'r')
            line = f.readline()
            if line == '0\n':
                f.close()
            else:
                print 'Energy trading completed'
                contract_signal = 0
                f = open("nodetopython.txt", 'r')
                lines = f.readlines()
                add_energy = lines[0]
                money_paid = lines[1]
                add_energy = int(add_energy)
                money_paid = int(money_paid)
                energy_amount = energy_amount + add_energy
                print 'Money before payment : %d$' %money
                money = money - money_paid
                print 'Money after payment : %d$' %money
                f.close()

                # Reset txt file is used to next energy trading
                f = open("nodetopython.txt", 'w')
                f.write('0\n')
                f.write('0')
                f.close()
                
        elif contract_signal == 1 and energy_amount < 0:
            print ''
            print 'There is no energy'
            print 'You need energy trading'
            print "You can't drive device"
            print ''
            
            while True:
                f = open("nodetopython.txt", 'r')
                line = f.readline()
                if line == '0\n':
                    f.close()
                else:
                    print 'Energy trading completed'
                    contract_signal = 0
                    f = open("nodetopython.txt", 'r')
                    lines = f.readlines()
                    add_energy = lines[0]
                    money_paid = lines[1]
                    add_energy = int(add_energy)
                    money_paid = int(money_paid)
                    energy_amount = energy_amount + add_energy
                    print 'Money before payment : %d$' %money
                    money = money - money_paid
                    print 'Money after payment : %d$' %money
                    f.close()

                    # Reset txt file is used to next energy trading
                    f = open("nodetopython.txt", 'w')
                    f.write('0\n')
                    f.write('0')
                    f.close()
                    break

        energy_amount_str = str(energy_amount)
        conn.send(energy_amount_str)
        words = conn.recv(1024)
        
        # Energy display
        print 'Amount of Energy : %d' %energy_amount

if __name__ == '__main__':
    # Bluetooth Connection
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    server_sock.bind(("", blport))
    server_sock.listen(100)
    
    print 'Waiting for connection with the client'
    print ''
    conn, addr = server_sock.accept()
    conn.send('The connection with the server succeeded')
    start = conn.recv(1024)
    print start

    print '-'*30
    print 'Server addr :', server_addr
    print 'Client addr :', addr[0]
    print 'Port Number :', addr[1]
    print '-'*30
    print ''
    print ''
    
    # Make txt file that is used to energy trading
    f = open("nodetopython.txt", 'w')
    f.write('0\n')
    f.write('0')
    f.close()
    
    # Send data and energy(Initial data is "000", Initial energy is 5000)
    data = "000"
    conn.send(data)
    words = conn.recv(1024)

    conn.send(energy_amount_str)
    words = conn.recv(1024)
    
    # GuI
    root = Tkinter.Tk()
    root.title('Device Controller')
    
    label1 = Tkinter.Label(root, padx = 10, pady = 10, font = 20, foreground = 'red', text = 'OFF')
    label2 = Tkinter.Label(root, padx = 10, pady = 10, font = 20, foreground = 'red', text = 'OFF')
    label3 = Tkinter.Label(root, padx = 10, pady = 10, font = 20, foreground = 'red', text = 'OFF')
    
    button1 = Tkinter.Button(root, height = 1, width = 30, padx = 20, pady = 10, text = DeviceName1, command = push_device1)
    button2 = Tkinter.Button(root, height = 1, width = 30, padx = 20, pady = 10, text = DeviceName2, command = push_device2)
    button3 = Tkinter.Button(root, height = 1, width = 30, padx = 20, pady = 10, text = DeviceName3, command = push_device3)
    button4 = Tkinter.Button(root, height = 1, width = 30, padx = 20, pady = 10, text = 'LED information', command = information_led)
    button5 = Tkinter.Button(root, height = 1, width = 30, padx = 20, pady = 10, text = 'FAN information', command = information_fan)
    button6 = Tkinter.Button(root, height = 1, width = 30, padx = 20, pady = 10, text = 'CAR information', command = information_car)
    
    label1.grid(row = 1, column = 1)
    label2.grid(row = 2, column = 1)
    label3.grid(row = 3, column = 1)
    
    button1.grid(row = 1, column = 0)
    button2.grid(row = 2, column = 0)
    button3.grid(row = 3, column = 0)
    button4.grid(row = 4, column = 0)
    button5.grid(row = 5, column = 0)
    button6.grid(row = 6, column = 0)

    root.mainloop()
    
    

    
 
    

    

    
