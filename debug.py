import serial

PORT = "/dev/ttyACM0"
BAUD = 115200

def write(msg: str):
    with serial.Serial(PORT,BAUD) as ser:
        ser.write(msg.encode('ascii'))

def read():
    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        rep = ' '
        res = []
        while not rep == '':
            rep = ser.readline()
            print(rep)
            res.append(rep)
        return res         
