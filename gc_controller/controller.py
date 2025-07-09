import hid
from typing import Optional

from .buttons import Buttons
from .joystick import Joystick
from .dpad import Dpad

class GameCubeController:
    """
    Main controller class for a GameCube HID device.

    This class manages device discovery, connection, and state updates.
    It provides access to specialized sub-controllers for different
    hardware components (joysticks, buttons) using a hybrid composition pattern.

    It is designed to be used as a context manager with a 'with' statement
    to ensure that network resources are properly managed.
    """
    def __init__(self, vendor_id: int = 0x0079, product_id: int = 0x0006):
        """
        Initializes the controller.

        Args:
            vendor_id: The USB vendor ID of the controller/adapter.
            product_id: The USB product ID of the controller/adapter.
        """
        self._vendor_id = vendor_id
        self._product_id = product_id
        self._device_info: Optional[dict] = None
        self._hid_device: Optional[hid.device] = None

        # --- Hybrid Pattern Implementation ---
        # Expose specialized controllers as properties.
        self.main_stick = Joystick()
        self.c_stick = Joystick()
        self.buttons = Buttons()
        self.dpad = Dpad()
        self.l_trigger_analog: int = 0
        self.r_trigger_analog: int = 0
        # -----------------------------------

    def connect(self) -> None:
        """
        Finds and connects to the specified GameCube controller device.
        Raises ConnectionError if the device cannot be found or opened.
        """
        if self.is_connected:
            print("Controller is already connected.")
            return

        print(f"Searching for device with VID={self._vendor_id:04x} PID={self._product_id:04x}...")
        for device in hid.enumerate():
            if device['vendor_id'] == self._vendor_id and device['product_id'] == self._product_id:
                self._device_info = device
                break

        if not self._device_info:
            raise ConnectionError("GameCube controller not found.")

        device = None
        try:
            print(f"Found: {self._device_info.get('product_string', 'Unknown')}. Connecting...")
            device = hid.device()
            device.open_path(self._device_info['path'])
            device.set_nonblocking(1)

            # Only assign to the instance attribute on full success
            self._hid_device = device

            print("Connection successful.")
        except (IOError, ValueError) as e:
            # If `device` was successfully created, close it on failure.
            if device:
                device.close()

            self._hid_device = None # Ensure state is clean
            raise ConnectionError(f"Failed to open HID device: {e}") from e

    def close(self) -> None:
        """Closes the connection to the device."""
        if self._hid_device:
            self._hid_device.close()
            self._hid_device = None
            print("Controller connection closed.")

    @property
    def is_connected(self) -> bool:
        """Returns True if the controller is connected, False otherwise."""
        return self._hid_device is not None

    def read(self, timeout_ms: int = 100) -> bool:
        """
        Reads the latest data packet from the controller and updates its state.

        This method should be called repeatedly in a loop to get live updates.

        Args:
            timeout_ms: The time in milliseconds to wait for a packet.

        Returns:
            True if new data was received and the state was updated, False otherwise.
        """
        if not self.is_connected:
            return False

        try:
            assert self._hid_device is not None
            data = self._hid_device.read(64, timeout_ms=timeout_ms)
        except IOError as e:
            print(f"Error reading from device, disconnecting: {e}")
            self.close()
            return False

        if not data:
            return False # Read timed out, no new data

        # Based on a common controller data format.
        # This may need adjustment depending on the specific adapter.
        if len(data) >= 8:
            self.main_stick.update(x_val=data[0], y_val=data[1])
            self.c_stick.update(x_val=data[3], y_val=data[2])
            self.l_trigger_analog = data[4]
            self.buttons.update(byte5=data[5], byte6=data[6])
            self.dpad.update(byte_val=data[5])
            self.r_trigger_analog = data[7]
            return True

        return False # Data packet was too short

    def __enter__(self):
        """Context manager entry point: connects to the device."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point: closes the connection."""
        self.close()


if __name__ == '__main__':
    import time
    import sys

    print("--- GameCube Controller Test ---")
    print("Press Ctrl+C to exit.")

    try:
        # The 'with' statement handles connect() and close() automatically.
        with GameCubeController() as controller:
            while True:
                # Read the controller state.
                if controller.read():
                    main_stick_state = controller.main_stick.direction.name
                    c_stick_state = controller.c_stick.direction.name
                    dpad_state = controller.dpad.direction.name
                    buttons_state = controller.buttons.state

                    # Use carriage return to print on the same line.
                    # The extra spaces at the end clear the previous line.
                    output = (
                        f"Main: {main_stick_state:<10} "
                        f"C-Stick: {c_stick_state:<10} "
                        f"D-Pad: {dpad_state:<10} "
                        f"Buttons: {buttons_state}      \r"
                    )
                    sys.stdout.write(output)
                    sys.stdout.flush()

                # A small delay to prevent the loop from running too fast
                # and to be friendly to the CPU.
                time.sleep(1 / 60)  # Aim for a 60Hz refresh rate.

    except ConnectionError as e:
        print(f"\n[ERROR] Could not connect to controller: {e}")
    except KeyboardInterrupt:
        print("\nExiting.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
