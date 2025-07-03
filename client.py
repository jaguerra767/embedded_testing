import socket

from time import sleep
from dataclasses import dataclass
HOST_2 = "192.168.1.12"
PORT = 8888


@dataclass
class ClearCore:
    sock: socket.socket


def read(sock: socket.socket) -> bytes:
    return sock.recv(1024)


def write(sock: socket.socket, msg: str) -> str:
    sock.sendall(msg.encode())
    return read(sock).decode()

def enable(controller: ClearCore, motor: int):
    msg = f"\x02M{motor}EN\x13"
    result = write(controller.sock, msg)
    return result

def disable(controller: ClearCore, motor: int):
    msg = f"\x02M{motor}DE\x13"
    result = write(controller.sock, msg)
    return result

def absolute_move(controller: ClearCore, motor: int, steps: int):
    msg = f"\x02M{motor}AM{steps}\x13"
    result = write(controller.sock, msg)
    return result

def relative_move(controller: ClearCore, motor: int, steps: int):
    msg = f"\x02M{motor}RM{steps}\x13"
    result = write(controller.sock, msg)
    return result



if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST_2, PORT))
    controller = ClearCore(sock)
    try:
        sleep(2)
    except KeyboardInterrupt:
        sock.close()
