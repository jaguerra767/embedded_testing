import socket

HOST = "192.168.1.11"
PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    sock.connect((HOST, PORT))

def read():
    data = sock.recv(1024)
    print(f"Received {data!r}")


def write(msg: str):
    sock.sendall(msg.encode())
    read()    


    
