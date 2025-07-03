import hid
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any


# Define a type alias for the device info dictionary for clarity
DeviceInfo = Dict[str, Any]

def find_controller(vid: int = 0x0079, pid: int = 0x0006) -> Optional[DeviceInfo]:
    """
    Finds a HID device by vendor and product ID.
    Returns the device info dictionary if found, otherwise None.
    """
    for device in hid.enumerate():
        if device['vendor_id'] == vid and device['product_id'] == pid:
            return device
    return None

def read_from_controller(controller_device: hid.device, timeout: int = 1000) -> Optional[bytes]:
    """
    Reads a report from an open HID device.
    Returns the data as bytes if successful, otherwise None.
    """
    BYTES_TO_READ = 64
    try:
        # The read method for the 'hid' library wrapper returns a list of integers.
        # The timeout parameter is specified in milliseconds.
        data = controller_device.read(BYTES_TO_READ, timeout_ms=timeout)
        if data:
            return bytes(data)
        return None
    except IOError as e:
        # Catch I/O errors that can occur during the read operation.
        print(f"Error reading from device: {e}")
        return None

class JoystickState(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    CENTER = 4

def get_joystick_state(data: bytes)->JoystickState:
    if len(data) < 2:
        return JoystickState.CENTER
    x, y = data[0], data[1]
    if x == 0x80 and y == 0x80:
        return JoystickState.CENTER
    elif x == 0x80:
        return JoystickState.UP if y < 0xff else JoystickState.DOWN
    elif y == 0x80:
        return JoystickState.LEFT if x < 0xff else JoystickState.RIGHT
    else:
        return JoystickState.CENTER

@dataclass
class Buttons:
    A: bool = False
    B: bool = False
    X: bool = False
    Y: bool = False
    L: bool = False
    Z: bool = False
    R: bool = False

def get_buttons_state(data:bytes) -> Optional[Buttons]:
    if len(data) < 2:
        return None
    print(hex(data[5]))
    return Buttons(
        A=bool(data[5] & 0x8f),
        B=bool(data[5] & 0x02),
        X=bool(data[5] & 0x04),
        Y=bool(data[5] & 0x08),
        L=bool(data[6] & 0x10),
        Z=bool(data[6] & 0x20),
        R=bool(data[6] & 0x40)
    )



if __name__ == "__main__":
    controller_info = find_controller()

    if not controller_info:
        print("Controller not found.")
    else:
        # Use .get() for safer dictionary access
        product_string = controller_info.get('product_string', 'Unknown Device')
        print(f"Found controller: {product_string}")

        # The hid.device object is our handle for communicating with the device.
        hid_device = hid.device()
        try:
            # The 'path' key in the device info dictionary is needed to open the device.
            device_path = controller_info.get('path')
            if not device_path:
                print("Device path not found in device info.")
            else:
                hid_device.open_path(device_path)
                print("Device opened.")

                # Set non-blocking mode. This is often necessary for timeouts to work correctly.
                hid_device.set_nonblocking(1)

                print("Attempting to read from controller...")
                received_data = read_from_controller(hid_device, timeout=2000)
                if received_data:
                    print(get_joystick_state(received_data))
                    print(get_buttons_state(received_data))
                else:
                    print("No data received. The read may have timed out or an error occurred.")

        except (IOError, ValueError) as e:
            # Catch common exceptions for HID device communication.
            print(f"An error occurred: {e}")
        finally:
            hid_device.close()
            print("Device closed.")
