
import requests
import socket
import time

FIREBASE_URL = "https://ryo-backend-default-rtdb.firebaseio.com"





CC_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CC_1_IP = "192.168.1.11"


CC_1_PORT = 8888


CC_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CC_2_IP = "192.168.1.12"
CC_2_PORT = 8888

class Output:
    def __init__(self, cc, id_red, id_green):
        self.cc : socket.socket = cc
        self.id_red : int  = id_red
        self.id_green : int = id_green

    def turn_on_green(self):
        turn_off(self.cc, self.id_red)
        turn_on(self.cc, self.id_green)

    def turn_on_red(self):
        turn_off(self.cc, self.id_green)
        turn_on(self.cc, self.id_red)

    def turn_off_green(self):
        turn_off(self.cc, self.id_green)




def read(sock: socket.socket) -> bytes:
    return sock.recv(1024)

def write(sock: socket.socket, msg: str) -> str:
    sock.sendall(msg.encode())
    return read(sock).decode()    

def turn_on(sock ,output_id):
    msg = f"\x02O{output_id}1\x13"
    write(sock, msg)

def turn_off(sock, output_id):
    msg = f"\x02O{output_id}0\x13"
    write(sock, msg)

def connect():
    CC_1.connect((CC_1_IP, CC_1_PORT))
    CC_2.connect((CC_2_IP, CC_2_PORT))


def get_node_states():
    url = f"{FIREBASE_URL}/ryo0001/NodeLevels.json"
    resp = requests.get(url)
    print(resp.json())

def go_wild():
    outputs = [Output(CC_1, 1,2), Output(CC_1, 3,4), Output(CC_2, 0,1), Output(CC_2, 2,3), Output(CC_2, 4,5)]
    while True:
        for output in outputs:
            output.turn_on_green()
        
        time.sleep(0.5)
        for output in outputs:
            output.turn_off_green()
        time.sleep(0.5)

if __name__ == "__main__":
    connect()
    go_wild()

