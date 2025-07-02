import socket

from time import sleep
from enum import Enum
from dataclasses import dataclass
HOST_2 = "192.168.1.12"
PORT = 8888

cc2_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



@dataclass
class HBridge:
    drive: socket.socket
    ch_a: int
    ch_b: int
    output: int | None = None
    timeout: int | float | None = None

class HBChannel(Enum):
    CH_A = 1
    CH_B = 2

class OP(Enum):
    OPEN = 32000
    CLOSE = -32000 

@dataclass
class FeedbackActuator:
    drive: socket.socket
    h_bridge: int
    relay: int | None = None

actuators = [
        FeedbackActuator(cc2_sock,4,2),
        FeedbackActuator(cc2_sock,5,3)
        ]

def connect(): 
    cc2_sock.connect((HOST_2, PORT))

def read(sock: socket.socket) -> bytes:
    return sock.recv(1024)


def write(sock: socket.socket, msg: str) -> str:
    sock.sendall(msg.encode())
    return read(sock).decode()    

def which_channel(channel: HBChannel) -> str:
        match channel:
            case HBChannel.CH_A:
                return "255\x13"
            case HBChannel.CH_B:
                return "0\x13"
    

def close(actuator: FeedbackActuator, channel: HBChannel):
    channel_cmd = f"\x02O{actuator.relay}"
    print(write(actuator.drive, channel_cmd + which_channel(channel)))
    h_bridge_cmd = f"\x02O{actuator.h_bridge}-32700\x13"
    print(write(actuator.drive, h_bridge_cmd))
    sleep(3)
    h_bridge_off = f"\x02O{actuator.h_bridge}0\x13"
    print(write(actuator.drive, h_bridge_off))

def close_all():
    for actuator in actuators:
        close(actuator, HBChannel.CH_A)
        close(actuator, HBChannel.CH_B)

def open(actuator: FeedbackActuator, channel: HBChannel):
    channel_cmd = f"\x02O{actuator.relay}"
    print(write(actuator.drive, channel_cmd + which_channel(channel)))
    h_bridge_cmd = f"\x02O{actuator.h_bridge}32700\x13"
    print(write(actuator.drive, h_bridge_cmd))
    sleep(3)
    h_bridge_off = f"\x02O{actuator.h_bridge}0\x13"
    print(write(actuator.drive, h_bridge_off))


def open_all():
    for actuator in actuators:
        open(actuator, HBChannel.CH_A)
        open(actuator, HBChannel.CH_B)



def h_bridge_actuate(bridge: HBridge, channel: HBChannel, op: OP):
    ch_a_on = f"\x02O{bridge.ch_a}255\x13"
    ch_a_off = f"\x02O{bridge.ch_a}0\x13"
    ch_b_on = f"\x02O{bridge.ch_b}255\x13"
    ch_b_off = f"\x02O{bridge.ch_b}0\x13"
    if channel == HBChannel.CH_A:
        print(ch_b_off)
        write(bridge.drive, ch_b_off)
        print(ch_a_on)
        write(bridge.drive, ch_a_on)

    if channel == HBChannel.CH_B:
        write(bridge.drive, ch_a_off)
        write(bridge.drive, ch_b_on)

    if bridge.output:
        out_msg = f"\x02O{bridge.output} {op}\x13"
        write(bridge.drive, out_msg)

    if bridge.timeout:
        print("Waiting for  timeout..")
        sleep(bridge.timeout)
        if bridge.output:
            out_off = f"\x02O{bridge.output} 0\x13"
            write(bridge.drive, out_off)
        write(bridge.drive, ch_a_off)
        write(bridge.drive, ch_b_off)

def test_ch_a(drive: socket.socket, rly: int):
    ch_a_on = f"\x02O{rly}16000\x13"
    print(ch_a_on)
    write(drive, ch_a_on)
    sleep(3)
    ch_a_off = f"\x02O{rly}0\x13"
    write(drive, ch_a_off)
    print("Off")

if __name__ == "__main__":
    connect()
    print(write(cc2_sock, "\x02M2EN\x13"))
    sleep(2)
    #print(write(cc2_sock, "\x02O40\x13"))
    #print("socks: cc1_sock, cc2_sock\n ops: connect(), h_bridge_actuate()\n")
#sealer = HBridge(drive=cc1_sock,ch_a=2,ch_b=3,output=4 ,timeout=2)
#connect()
